#!/usr/bin/env python3
"""
build.py — render mysynergy.technology static site

Reads:  events/*.md  (frontmatter + markdown body)
        index.template.html
Writes: dist/index.html
        dist/style.css
        dist/countdown.js

Frontmatter (YAML-lite, parsed by hand):
  ---
  date: 2026-04-29        (required, ISO date)
  tags: [a, b, c]         (required, list)
  title: Headline text    (required)
  link_text: Apply        (optional)
  link_url:  https://...  (optional)
  pinned: true            (optional — keeps entry at top of build log)
  ---

Body: Markdown subset
  - paragraphs separated by blank lines
  - inline `code` rendered as <code>code</code>
  - **bold** rendered as <strong>bold</strong>
  - _italic_ rendered as <em>italic</em>
  - no other transformations (intentionally minimal)
"""
import os, re, html, sys, datetime, shutil, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVENTS = ROOT / 'events'
DIST = ROOT / 'dist'
TEMPLATE = ROOT / 'index.template.html'

def parse_frontmatter(text):
    """Split ---\nfrontmatter\n---\nbody."""
    if not text.startswith('---'):
        raise ValueError('missing frontmatter')
    parts = text.split('---', 2)
    if len(parts) < 3:
        raise ValueError('malformed frontmatter')
    fm_raw, body = parts[1], parts[2].lstrip('\n')
    fm = {}
    for line in fm_raw.strip().split('\n'):
        if not line.strip(): continue
        if ':' not in line: continue
        k, v = line.split(':', 1)
        k = k.strip(); v = v.strip()
        # Lists like [a, b, c]
        if v.startswith('[') and v.endswith(']'):
            inner = v[1:-1].strip()
            fm[k] = [t.strip() for t in inner.split(',') if t.strip()] if inner else []
        elif v.lower() in ('true','false'):
            fm[k] = v.lower() == 'true'
        else:
            fm[k] = v
    return fm, body

def md_inline(text):
    """Minimal inline transforms."""
    # Escape first
    s = html.escape(text)
    # Restore safe inline patterns (re-apply after escape)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\w)_([^_]+)_(?!\w)', r'<em>\1</em>', s)
    return s

def md_body(body):
    """Paragraphs by blank-line."""
    paragraphs = re.split(r'\n\s*\n', body.strip())
    out = []
    for p in paragraphs:
        if not p.strip(): continue
        # Single-line newlines collapse to spaces
        line = ' '.join(p.split())
        out.append(f'<p>{md_inline(line)}</p>')
    return '\n'.join(out)

def fmt_date(iso):
    """2026-04-29 -> 29 APR 2026"""
    d = datetime.date.fromisoformat(iso)
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    return f'{d.day} {months[d.month-1]} {d.year}'

def render_event(fm, body):
    tags_html = '\n              '.join(
        f'<span class="event__tag">{html.escape(t)}</span>' for t in fm.get('tags', [])
    )
    link_html = ''
    if fm.get('link_url') and fm.get('link_text'):
        link_html = f'\n          <a class="event__link" href="{html.escape(fm["link_url"])}" target="_blank" rel="noopener">{html.escape(fm["link_text"])} →</a>'
    return f'''      <li class="event">
        <div class="event__meta">
          <p class="event__date">{fmt_date(fm['date'])}</p>
          <div class="event__tags">
              {tags_html}
          </div>
        </div>
        <div class="event__body">
          <h3>{html.escape(fm['title'])}</h3>
          {md_body(body)}{link_html}
        </div>
      </li>'''

def load_events():
    events = []
    for path in sorted(EVENTS.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        try:
            fm, body = parse_frontmatter(text)
        except ValueError as e:
            print(f'SKIP {path.name}: {e}', file=sys.stderr)
            continue
        events.append({'fm': fm, 'body': body, 'src': path.name})
    # Sort: pinned first, then date desc
    events.sort(key=lambda e: (
        not e['fm'].get('pinned', False),
        e['fm']['date']
    ), reverse=False)
    # We want pinned first, then most-recent first within unpinned
    pinned = [e for e in events if e['fm'].get('pinned')]
    rest = sorted([e for e in events if not e['fm'].get('pinned')],
                  key=lambda e: e['fm']['date'], reverse=True)
    return pinned + rest

def main():
    DIST.mkdir(exist_ok=True)
    template = TEMPLATE.read_text(encoding='utf-8')
    events = load_events()
    rendered = '\n'.join(render_event(e['fm'], e['body']) for e in events)
    last_event_date = max(
        (datetime.date.fromisoformat(e['fm']['date']) for e in events),
        default=datetime.date.today()
    )
    html_out = (template
        .replace('{{EVENTS}}', rendered)
        .replace('{{LAST_UPDATED}}', fmt_date(last_event_date.isoformat()))
        .replace('{{EVENT_COUNT}}', str(len(events)))
    )
    (DIST / 'index.html').write_text(html_out, encoding='utf-8')
    shutil.copy2(ROOT / 'style.css', DIST / 'style.css')
    shutil.copy2(ROOT / 'countdown.js', DIST / 'countdown.js')
    # Manifest for debugging / future RSS
    (DIST / 'events.json').write_text(json.dumps(
        [{'src': e['src'], **e['fm']} for e in events],
        indent=2, ensure_ascii=False
    ), encoding='utf-8')
    print(f'Built {len(events)} events → {DIST/"index.html"}')

if __name__ == '__main__':
    main()
