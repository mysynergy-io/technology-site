#!/usr/bin/env python3
"""
build.py — render mysynergy.technology static site

Reads:  events/*.md  (frontmatter + markdown body)
        index.template.html
Writes: dist/  -> Hostinger /public_html (published by FTP)
        docs/  -> GitHub Pages at mysynergy-io.github.io/technology-site (published by git push)

TWO PUBLIC SURFACES. Both are live. This script writes BOTH, always, byte-identical.
2026-09-26 it wrote only dist/, so the 17 September cards went live on Hostinger and never
reached Pages; Pages served a 26-August snapshot for a further four weeks while the primary
surface moved on. The hazard had been written down on 2026-09-13 and recurred on the very next
publish, because a note does not copy a file. Mirroring also fixes the dangerous direction:
--no-events strips the log from dist/, and an unmirrored docs/ would keep serving every card.

Writing docs/ PUBLISHES NOTHING on its own -- Pages ships on `git push`, Hostinger on FTP.

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
DOCS = ROOT / 'docs'          # GitHub Pages surface; mirrored from DIST, never built separately
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

# -- GEOGRAPHY GATE (Bill 2026-09-13) -----------------------------------------
# The rule applies to ALL location references, not just supply-chain lines, and
# it is checked on the RENDERED PAGE - not on events/*.md.
#
# Why the rendered page: on 2026-09-13 all 42 source cards scanned clean while
# the built page still said "Shenzhen", because the term lived in
# index.template.html furniture a card-level scan cannot see. A content rule
# has to be enforced on what ships.
BLOCKED_PLACES = [
    'China', 'Chinese', 'PRC',
    'Shenzhen', 'Guangzhou', 'Dongguan', 'Guangdong', 'Shanghai', 'Beijing',
    'Ningbo', 'Yiwu', 'Xiamen', 'Qingdao', 'Kowloon', 'Macau', 'Macao',
    'Taiwan', 'Mexico', 'Tijuana', 'Monterrey',
    'Ho Chi Minh', 'Hanoi', 'Haiphong', 'Da Nang', 'Binh Duong', 'Bac Ninh',
]
ALLOWED_PLACES = ['Vietnam', 'Hong Kong', 'Singapore']


def geography_gate(html_text):
    """Abort the build if a blocked place name reaches the rendered page."""
    hits = []
    for place in BLOCKED_PLACES:
        for m in re.finditer(r'\b' + re.escape(place) + r'\b', html_text, re.I):
            a, b = max(0, m.start() - 60), min(len(html_text), m.end() + 60)
            hits.append((place, ' '.join(html_text[a:b].split())))
    if hits:
        print('\nGEOGRAPHY GATE FAILED - blocked place name(s) in the RENDERED page:',
              file=sys.stderr)
        for place, ctx in hits:
            print('  %-12s ...%s...' % (place, ctx), file=sys.stderr)
        print('\nThe rule covers ALL locations, not only supply-chain lines.',
              file=sys.stderr)
        print('Cleared for publication: %s' % ', '.join(ALLOWED_PLACES), file=sys.stderr)
        print('Nothing was written. Fix events/*.md OR index.template.html, then rebuild.',
              file=sys.stderr)
        sys.exit(2)


def main():
    DIST.mkdir(exist_ok=True)
    template = TEMPLATE.read_text(encoding='utf-8')
    # --no-events / SITE_NO_EVENTS=1 : render the site with the public build log
    # REMOVED, while leaving every events/*.md on disk so writing continues.
    # Bill 2026-09-13. Revert = build with no flag.
    suppress = ('--no-events' in sys.argv) or os.environ.get('SITE_NO_EVENTS') == '1'
    if suppress:
        template, n = re.subn(
            r'<section class="log-section">.*?</section>\s*', '', template, flags=re.S)
        if n != 1:
            sys.exit('ABORT: expected exactly 1 log-section to strip, matched %d. '
                     'Template changed - not shipping a half-stripped page.' % n)
    events = [] if suppress else load_events()
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
    geography_gate(html_out)
    (DIST / 'index.html').write_text(html_out, encoding='utf-8')
    shutil.copy2(ROOT / 'style.css', DIST / 'style.css')
    shutil.copy2(ROOT / 'countdown.js', DIST / 'countdown.js')
    shutil.copy2(ROOT / 'robots.txt', DIST / 'robots.txt')
    # Manifest for debugging / future RSS
    (DIST / 'events.json').write_text(json.dumps(
        [{'src': e['src'], **e['fm']} for e in events],
        indent=2, ensure_ascii=False
    ), encoding='utf-8')
    # Mirror to the SECOND public surface. A build that updates one surface and not the other
    # leaves two different public versions of the same log, which is what happened on 09-26.
    DOCS.mkdir(exist_ok=True)
    mirrored = []
    for fn in ('index.html', 'style.css', 'countdown.js', 'robots.txt', 'events.json'):
        shutil.copy2(DIST / fn, DOCS / fn)
        mirrored.append(fn)

    # Refuse to report success on a half-mirrored publish. A MISSING mirror file is the
    # worst case, not an edge case -- read_bytes() on it used to raise a bare FileNotFoundError
    # and the refusal message never printed, so the operator got a traceback instead of being
    # told which surface was short which file.
    def _bytes_or_none(path):
        try:
            return path.read_bytes()
        except OSError:
            return None

    drift = []
    for fn in mirrored:
        a, b = _bytes_or_none(DIST / fn), _bytes_or_none(DOCS / fn)
        if a is None:
            drift.append('%s (missing from dist/)' % fn)
        elif b is None:
            drift.append('%s (missing from docs/)' % fn)
        elif a != b:
            drift.append('%s (differs)' % fn)
    if drift:
        sys.exit('ABORT: docs/ does not match dist/ after mirroring: %s. The two public '
                 'surfaces would serve different content. Nothing should be published.'
                 % ', '.join(drift))

    print(f'Built {len(events)} events → {DIST/"index.html"}')
    print(f'Mirrored {len(mirrored)} files → {DOCS}/ (GitHub Pages surface)')
    print('NOT PUBLISHED YET: Hostinger needs the FTP upload, Pages needs a git push.')

if __name__ == '__main__':
    main()
