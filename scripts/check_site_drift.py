#!/usr/bin/env python3
"""Check synthetic-mind site drift across skills inventory and generated docs."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / 'skills'
DOCS_SKILLS_DIR = ROOT / 'docs' / 'skills'
CATALOG_SOURCE = DOCS_SKILLS_DIR / 'catalog-source.json'
CATALOG_INDEX = DOCS_SKILLS_DIR / 'index.html'
MANIFEST_JS = DOCS_SKILLS_DIR / 'manifest.js'
HOME_INDEX = ROOT / 'docs' / 'index.html'


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    raise SystemExit(1)


def load_catalog_source() -> dict:
    return json.loads(CATALOG_SOURCE.read_text())


def parse_manifest_names() -> list[str]:
    text = MANIFEST_JS.read_text()
    match = re.search(r'window\.DETAILED_SKILL_PAGES\s*=\s*(\[[\s\S]*\])\s*;', text)
    if not match:
        fail('manifest.js does not contain DETAILED_SKILL_PAGES array')
    return json.loads(match.group(1))


def parse_catalog_names() -> list[str]:
    text = CATALOG_INDEX.read_text()
    return re.findall(r'<div class="skill-name">([^<]+)</div>', text)


def list_skill_dirs() -> list[str]:
    return sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and not p.name.startswith('.'))


def list_detail_pages() -> list[str]:
    return sorted(p.stem for p in DOCS_SKILLS_DIR.glob('*.html') if p.name != 'index.html')


def ensure_homepage_counts() -> None:
    text = HOME_INDEX.read_text()
    required = [
        '100 public agent skills',
        '100 public AI agent skills',
        '<div class="impact-num">100</div>',
    ]
    for snippet in required:
        if snippet not in text:
            fail(f'homepage missing expected snippet: {snippet}')


def ensure_unique(label: str, names: list[str]) -> None:
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        fail(f'{label} contains duplicate names: {duplicates}')


def main() -> None:
    skills = list_skill_dirs()
    catalog = load_catalog_source()
    catalog_source_names = [item['name'] for item in catalog['skills']]
    catalog_index_names = parse_catalog_names()
    manifest_names = parse_manifest_names()
    detail_pages = list_detail_pages()

    ensure_unique('catalog-source.json', catalog_source_names)
    ensure_unique('catalog index', catalog_index_names)
    ensure_unique('manifest.js', manifest_names)
    ensure_unique('detail pages', detail_pages)

    if sorted(catalog_source_names) != skills:
        fail('catalog-source.json skill names do not match skills/ directories')

    if sorted(catalog_index_names) != skills:
        fail('docs/skills/index.html skill cards do not match skills/ directories')

    if sorted(manifest_names) != skills:
        fail('docs/skills/manifest.js does not match skills/ directories')

    if sorted(detail_pages) != skills:
        fail('docs/skills/*.html detail pages do not match skills/ directories')

    if len(catalog['skills']) != len(skills):
        fail('catalog-source.json count does not match number of skill directories')

    ensure_homepage_counts()

    print('OK: skills inventory, catalog source, generated catalog, detail pages, manifest, and homepage counts are in sync')


if __name__ == '__main__':
    main()
