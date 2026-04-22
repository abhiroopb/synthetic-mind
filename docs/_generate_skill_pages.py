#!/usr/bin/env python3
"""Generate individual HTML skill detail pages from README.md files."""

import os
import re
import html as html_mod

SKILLS_SRC = os.path.join(os.path.dirname(__file__), '..', 'skills')
SKILLS_OUT = os.path.join(os.path.dirname(__file__), 'skills')

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
      <a href="./" class="active">Projects</a>
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

    # 3. Apply markdown formatting on the escaped text
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)

    # 4. Restore code spans
    for idx, html in enumerate(code_spans):
        text = text.replace(f'\x00CODE{idx}\x00', html)

    return text


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


def generate_skill_page(skill_name, readme_path, out_dir):
    """Generate a single skill HTML page."""
    with open(readme_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    h1_title, description, body_html = md_to_html(md_text)

    if not h1_title:
        h1_title = skill_name.replace('-', ' ').title()

    page_title = h1_title
    meta_description = description if description else f'{h1_title} — an Amp agent skill.'

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


def main():
    os.makedirs(SKILLS_OUT, exist_ok=True)

    entries = sorted(os.listdir(SKILLS_SRC))
    generated = []
    errors = []

    for entry in entries:
        entry_path = os.path.join(SKILLS_SRC, entry)
        if not os.path.isdir(entry_path):
            continue

        readme_path = os.path.join(entry_path, 'README.md')
        if not os.path.isfile(readme_path):
            errors.append(f'SKIP {entry}: no README.md')
            continue

        try:
            out = generate_skill_page(entry, readme_path, SKILLS_OUT)
            generated.append(out)
            print(f'  ✓ {entry}')
        except Exception as e:
            errors.append(f'ERROR {entry}: {e}')
            print(f'  ✗ {entry}: {e}')

    print(f'\nGenerated: {len(generated)} pages')
    if errors:
        print(f'Errors/skips: {len(errors)}')
        for err in errors:
            print(f'  - {err}')


if __name__ == '__main__':
    main()
