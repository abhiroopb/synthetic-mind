#!/usr/bin/env python3
"""Generate individual HTML skill detail pages from skill markdown files."""

import json
import os
import re
import html as html_mod

SKILLS_SRC = os.path.join(os.path.dirname(__file__), '..', 'skills')
SKILLS_OUT = os.path.join(os.path.dirname(__file__), 'skills')
CATALOG_SOURCE = os.path.join(SKILLS_OUT, 'catalog-source.json')
CATALOG_INDEX_OUT = os.path.join(SKILLS_OUT, 'index.html')
MANIFEST_OUT = os.path.join(SKILLS_OUT, 'manifest.js')

TEMPLATE = '''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title} — Skills — synthetic-mind</title>
  <meta name="description" content="{meta_description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  <style>
    .article-meta {{
      display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;
      color: var(--text-dim); font-size: 0.85rem;
    }}
    .article-tag {{
      display: inline-block; font-size: 0.7rem; font-weight: 500; padding: 0.15rem 0.5rem;
      border-radius: 100px; background: var(--accent-dim); color: var(--accent);
    }}
    .gh-link {{
      display: inline-flex; align-items: center; gap: 0.4rem;
      color: var(--text-muted); text-decoration: none; font-size: 0.85rem;
      font-weight: 500; padding: 0.5rem 1rem; border-radius: var(--radius-sm);
      border: 1px solid var(--border); background: var(--surface); transition: all 0.15s;
    }}
    .gh-link:hover {{ color: var(--text); border-color: var(--text-dim); }}
    .gh-link svg {{ width: 16px; height: 16px; fill: currentColor; }}
    @media (max-width: 768px) {{
      .page-content h1 {{ font-size: 1.8rem; }}
    }}
  </style>
</head>
<body>

<nav>
  <div class="nav-inner">
    <a href="../" class="nav-brand">🧠 synthetic-mind</a>
    <div class="nav-links">
      <a href="../#about">About</a>
      <a href="../ai-pm-os/">AI PM OS</a>
      <a href="../thoughts/">Thoughts</a>
      <a href="./" class="active">Skills</a>
      <a href="../setup/">Setup</a>
    </div>
    <a href="https://github.com/abhiroopb/synthetic-mind" class="nav-gh" target="_blank">
      <svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
      GitHub
    </a>
  </div>
</nav>

<div class="page-content">
  <a href="./" class="back-link">All skills</a>

  <h1>{h1_title}</h1>
  <div class="article-meta">
    <span class="article-tag">skill</span>
    <a href="https://github.com/abhiroopb/synthetic-mind/tree/main/skills/{skill_name}" class="gh-link" target="_blank">
      <svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
      View on GitHub
    </a>
  </div>

{body_html}
</div>

<footer>
  <p>Built by <a href="https://github.com/abhiroopb">Abhi Basu</a> · <a href="https://github.com/abhiroopb/synthetic-mind">View on GitHub</a> · Powered by <a href="https://ampcode.com">Amp</a></p>
</footer>

</body>
</html>'''

CATALOG_TEMPLATE = '''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title} — synthetic-mind</title>
  <meta name="description" content="{meta_description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  <style>
    .page-header {{
      padding: 8rem 2rem 3rem; text-align: center; max-width: 800px; margin: 0 auto;
    }}
    .page-header h1 {{
      font-size: 2.5rem; font-weight: 800; letter-spacing: -0.04em; margin-bottom: 0.5rem;
      background: linear-gradient(135deg, #fff 0%, #a3a3a3 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .page-header p {{ font-size: 1.1rem; color: var(--text-muted); }}
    .skills-section {{ padding: 0 0 4rem; }}
    .skill-count {{
      text-align: center; font-size: 0.8rem; color: var(--text-dim);
      margin-top: 1.5rem; font-family: 'JetBrains Mono', monospace;
    }}
    @media (max-width: 768px) {{
      .page-header h1 {{ font-size: 1.8rem; }}
    }}
  </style>
</head>
<body>

<nav>
  <div class="nav-inner">
    <a href="../" class="nav-brand">🧠 synthetic-mind</a>
    <div class="nav-links">
      <a href="../#about">About</a>
      <a href="../ai-pm-os/">AI PM OS</a>
      <a href="../thoughts/">Thoughts</a>
      <a href="../skills/" class="active">Skills</a>
      <a href="../setup/">Setup</a>
    </div>
    <a href="https://github.com/abhiroopb/synthetic-mind" class="nav-gh" target="_blank">
      <svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
      GitHub
    </a>
  </div>
</nav>

<div class="page-header">
  <h1>{page_title}</h1>
  <p>{intro_html}</p>
  <p style="font-size:0.9rem;color:var(--text-dim);margin-top:0.75rem;">{subintro_html}</p>
</div>

<section class="skills-section">
  <div class="container">
    <div class="search-wrap">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>
      <input type="text" id="skill-search" placeholder="Search skills...">
    </div>

    <div class="tabs" id="category-tabs">
{tabs_html}
    </div>

    <div class="skills-page-grid" id="skills-grid">
{cards_html}
    </div>

    <div class="skill-count" id="skill-count"></div>
  </div>
</section>

<footer>
  <p>Built by <a href="https://github.com/abhiroopb">Abhi Basu</a> · <a href="https://github.com/abhiroopb/synthetic-mind">View on GitHub</a> · Powered by <a href="https://ampcode.com">Amp</a></p>
</footer>

<script src="./manifest.js"></script>
<script>
const tabs = document.querySelectorAll('.tab');
const cards = document.querySelectorAll('.skill-card');
const searchInput = document.getElementById('skill-search');
const countEl = document.getElementById('skill-count');
let activeCat = 'all';
const detailedSkillPages = new Set(window.DETAILED_SKILL_PAGES || []);

function resolveSkillHref(name) {{
  if (detailedSkillPages.has(name)) {{
    return `./${{name}}.html`;
  }}

  return `https://github.com/abhiroopb/synthetic-mind/tree/main/skills/${{name}}`;
}}

function filterCards() {{
  const q = searchInput.value.toLowerCase().trim();
  let visible = 0;
  cards.forEach(card => {{
    const matchesCat = activeCat === 'all' || card.dataset.cat === activeCat;
    const matchesSearch = !q || card.textContent.toLowerCase().includes(q);
    const show = matchesCat && matchesSearch;
    card.classList.toggle('hidden', !show);
    if (show) visible++;
  }});
  countEl.textContent = `Showing ${{visible}} of ${{cards.length}} catalog entries on this page`;
}}

tabs.forEach(tab => {{
  tab.addEventListener('click', () => {{
    tabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    activeCat = tab.dataset.cat;
    filterCards();
  }});
}});

searchInput.addEventListener('input', filterCards);

cards.forEach(card => {{
  card.addEventListener('click', () => {{
    const name = card.querySelector('.skill-name')?.textContent?.trim();
    if (name) {{
      window.location.href = resolveSkillHref(name);
    }}
  }});
}});

filterCards();
</script>

</body>
</html>'''


def escape(text):
    """HTML-escape text."""
    return html_mod.escape(text, quote=True)


def inline_format(raw_text):
    """Apply inline markdown formatting: bold, italic, code, links.

    Accepts raw (unescaped) markdown text.  Escapes everything *except*
    the contents of code spans (which are escaped separately to avoid
    double-escaping).
    """
    # 1. Pull out code spans, replacing with placeholders
    code_spans = []
    def _stash_code(m):
        idx = len(code_spans)
        code_spans.append('<code>' + escape(m.group(1)) + '</code>')
        return f'\x00CODE{idx}\x00'
    text = re.sub(r'`([^`]+)`', _stash_code, raw_text)

    # 2. Escape the remaining (non-code) text
    text = escape(text)

    # 3. Apply markdown formatting on the escaped text.
    # Keep these patterns line-bounded and non-greedy to avoid pathological
    # backtracking on long skill docs with lots of marker characters.
    text = re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)

    # 4. Restore code spans
    for idx, html in enumerate(code_spans):
        text = text.replace(f'\x00CODE{idx}\x00', html)

    return text


def strip_frontmatter(md_text):
    """Remove a leading YAML frontmatter block when present."""
    return re.sub(r'\A---\s*\n.*?\n---\s*\n', '', md_text, count=1, flags=re.DOTALL)


def extract_h1(md_text, fallback_title):
    """Extract the first markdown H1, falling back to a titleized slug."""
    match = re.search(r'(?m)^# (.+)$', md_text)
    if match:
        return match.group(1).strip()
    return fallback_title.replace('-', ' ').title()


def extract_description(md_text, fallback_title):
    """Use the first descriptive line for meta description."""
    for line in md_text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        return stripped[:200]
    return f'{fallback_title.replace("-", " ").title()} — an Amp agent skill.'


def render_skill_fallback_html(md_text):
    """Render raw SKILL.md content safely without complex inline markdown parsing."""
    body = re.sub(r'(?m)^# .+$\n?', '', md_text, count=1).strip()
    return f'  <pre><code>{escape(body)}</code></pre>'


def md_to_html(md_text):
    """Convert markdown text to HTML, skipping the first H1."""
    lines = md_text.split('\n')
    html_parts = []
    h1_title = ''
    description = ''
    skipped_h1 = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # H1 — extract title, skip rendering
        if not skipped_h1 and line.startswith('# '):
            h1_title = line[2:].strip()
            skipped_h1 = True
            i += 1
            continue

        # Empty line — skip
        if line.strip() == '':
            i += 1
            continue

        # Blockquote
        if line.startswith('> '):
            bq_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                bq_lines.append(lines[i][2:].strip())
                i += 1
            bq_text = ' '.join(bq_lines)
            if not description:
                description = bq_text
            html_parts.append(f'  <blockquote>{inline_format(bq_text)}</blockquote>')
            continue

        # H2
        if line.startswith('## '):
            html_parts.append(f'  <h2>{escape(line[3:].strip())}</h2>')
            i += 1
            continue

        # H3
        if line.startswith('### '):
            html_parts.append(f'  <h3>{escape(line[4:].strip())}</h3>')
            i += 1
            continue

        # Fenced code block
        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip closing ```
            code_content = escape('\n'.join(code_lines))
            if lang:
                html_parts.append(f'  <pre><code class="language-{escape(lang)}">{code_content}</code></pre>')
            else:
                html_parts.append(f'  <pre><code>{code_content}</code></pre>')
            continue

        # Unordered list
        if re.match(r'^[-*] ', line):
            list_items = []
            while i < len(lines) and re.match(r'^[-*] ', lines[i]):
                item_text = re.sub(r'^[-*] ', '', lines[i]).strip()
                list_items.append(f'    <li>{inline_format(item_text)}</li>')
                i += 1
            html_parts.append('  <ul>\n' + '\n'.join(list_items) + '\n  </ul>')
            continue

        # Ordered list
        if re.match(r'^\d+\. ', line):
            list_items = []
            while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
                item_text = re.sub(r'^\d+\. ', '', lines[i]).strip()
                list_items.append(f'    <li>{inline_format(item_text)}</li>')
                i += 1
            html_parts.append('  <ol>\n' + '\n'.join(list_items) + '\n  </ol>')
            continue

        # Regular paragraph — collect contiguous non-empty, non-special lines
        para_lines = []
        while i < len(lines) and lines[i].strip() != '' and \
              not lines[i].startswith('#') and \
              not lines[i].startswith('> ') and \
              not lines[i].strip().startswith('```') and \
              not re.match(r'^[-*] ', lines[i]) and \
              not re.match(r'^\d+\. ', lines[i]):
            para_lines.append(lines[i].strip())
            i += 1
        if para_lines:
            para_text = ' '.join(para_lines)
            html_parts.append(f'  <p>{inline_format(para_text)}</p>')
        continue

    return h1_title, description, '\n\n'.join(html_parts)


def generate_skill_page(skill_name, source_path, out_dir):
    """Generate a single skill HTML page."""
    with open(source_path, 'r', encoding='utf-8') as f:
        md_text = strip_frontmatter(f.read())

    if os.path.basename(source_path) == 'SKILL.md':
        h1_title = extract_h1(md_text, skill_name)
        meta_description = extract_description(md_text, skill_name)
        body_html = render_skill_fallback_html(md_text)
    else:
        h1_title, description, body_html = md_to_html(md_text)
        if not h1_title:
            h1_title = skill_name.replace('-', ' ').title()
        meta_description = description if description else f'{h1_title} — an Amp agent skill.'

    page_title = h1_title

    rendered = TEMPLATE.format(
        page_title=escape(page_title),
        meta_description=escape(meta_description),
        h1_title=escape(h1_title),
        skill_name=escape(skill_name),
        body_html=body_html,
    )

    out_path = os.path.join(out_dir, f'{skill_name}.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    return out_path


def resolve_skill_source(entry_path):
    """Prefer README.md, then fall back to SKILL.md for public detail pages."""
    for candidate in ('README.md', 'SKILL.md'):
        source_path = os.path.join(entry_path, candidate)
        if os.path.isfile(source_path):
            return source_path
    return None


def write_manifest(skill_names):
    manifest = (
        '// Generated by docs/_generate_skill_pages.py\n'
        f'window.DETAILED_SKILL_PAGES = {json.dumps(skill_names, indent=2)};\n'
    )
    with open(MANIFEST_OUT, 'w', encoding='utf-8') as f:
        f.write(manifest)


def load_catalog_source():
    with open(CATALOG_SOURCE, 'r', encoding='utf-8') as f:
        return json.load(f)


def render_catalog_tabs(tabs):
    rendered = []
    for tab in tabs:
        active = ' active' if tab.get('active') else ''
        rendered.append(
            f'      <button class="tab{active}" data-cat="{escape(tab["id"])}">{escape(tab["label"])}</button>'
        )
    return '\n'.join(rendered)


def render_catalog_cards(skills):
    rendered = []
    for skill in skills:
        rendered.append(
            '      '
            f'<div class="skill-card cat-{escape(skill["cat"])}" data-cat="{escape(skill["cat"])}">'
            f'<div class="skill-card-header"><div class="skill-icon">{escape(skill["icon"])}</div>'
            f'<div class="skill-name">{escape(skill["name"])}</div></div>'
            f'<div class="skill-desc">{escape(skill["desc"])}</div>'
            f'<div class="skill-example">{escape(skill["example"])}</div>'
            '</div>'
        )
    return '\n'.join(rendered)


def write_catalog_index(catalog):
    rendered = CATALOG_TEMPLATE.format(
        page_title=escape(catalog['page']['title']),
        meta_description=escape(catalog['page']['description']),
        intro_html=catalog['page']['intro'],
        subintro_html=escape(catalog['page']['subintro']),
        tabs_html=render_catalog_tabs(catalog['tabs']),
        cards_html=render_catalog_cards(catalog['skills']),
    )
    with open(CATALOG_INDEX_OUT, 'w', encoding='utf-8') as f:
        f.write(rendered)


def main():
    os.makedirs(SKILLS_OUT, exist_ok=True)
    catalog = load_catalog_source()

    entries = sorted(os.listdir(SKILLS_SRC))
    generated = []
    generated_skill_names = []
    errors = []

    for entry in entries:
        entry_path = os.path.join(SKILLS_SRC, entry)
        if not os.path.isdir(entry_path):
            continue

        source_path = resolve_skill_source(entry_path)
        if not source_path:
            errors.append(f'SKIP {entry}: no README.md or SKILL.md')
            continue

        try:
            out = generate_skill_page(entry, source_path, SKILLS_OUT)
            generated.append(out)
            generated_skill_names.append(entry)
            print(f'  ✓ {entry}')
        except Exception as e:
            errors.append(f'ERROR {entry}: {e}')
            print(f'  ✗ {entry}: {e}')

    write_catalog_index(catalog)
    write_manifest(generated_skill_names)

    print(f'\nGenerated: {len(generated)} pages')
    if errors:
        print(f'Errors/skips: {len(errors)}')
        for err in errors:
            print(f'  - {err}')


if __name__ == '__main__':
    main()
