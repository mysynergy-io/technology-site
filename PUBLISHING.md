# Publishing to mysynergy.technology — process runbook

How a build-log card gets from idea to the live public site. Two flows: the weekly
**recommendation** (automated) and the **publish** (manual, gated by Bill).

Last verified end-to-end: **2026-06-27** (JOR-20260627-002).

---

## Architecture (know this first)

- ⚠️ **TWO PUBLIC SURFACES. Both are live.** A publish is not done until both have it.
  - **Hostinger** serves `mysynergy.technology` from `/public_html/`, a copy of local `dist/`, deployed by FTP.
  - **GitHub Pages** serves `mysynergy-io.github.io/technology-site` from branch `main`, path `/docs`, deployed by `git push`.
- **`build.py` writes BOTH `dist/` and `docs/`, byte-identical, and aborts on a half-mirror** (since `ceeb7b2`, 2026-10-23).
- ⚠️ **This section used to say "ignore `docs/` — `build.py` does not write it." That was wrong and it cost 40 days.**
  On 2026-09-26 a 17-card publish wrote `dist/` only; Pages kept serving a 26-August snapshot until 2026-10-23.
  The hazard had been recorded on 2026-09-13 and recurred on the very next publish, because a note does not copy a file.
  Do not re-introduce a "docs/ is dead" claim without checking `build.py` and `gh api repos/.../pages`.
- **Source of truth = the git repo** `github.com/mysynergy-io/technology-site` (branch `main`). FTP deploys Hostinger; the push deploys Pages.
- Runtime is **`/usr/bin/python3` (3.9)** for both `build.py` and the FTP uploader.

---

## Flow A — Weekly recommendation (automated)

- **launchd job** `com.mysynergy.jor-sunday-build-update` (`~/Library/LaunchAgents/`) fires **Sunday 09:00 SGT**.
- Runs `~/scripts/jor_sunday_build_update.py` → spawns Jor (`claude -p`), reads the week's daily journey + git log + CCL + the current live log, drafts **3 ranked candidate cards**, and DMs them to Bill via `jor_telegram_send.py`.
- **Recommendation only — never publishes.** Bill picks/edits; an approved card goes through Flow B.
- Manual fire / test: `/usr/bin/python3 ~/scripts/jor_sunday_build_update.py [--dry-run]`.
- Log: `~/.openclaw/workspace/logs/jor_sunday_build_update.log`.

---

## Flow B — Publish an approved card (manual)

Site dir: `~/.openclaw/workspace/mysynergy-technology-site`

### 1. Pre-flight checks (before writing)
- **No-repeat rule:** scan `events/` and the live `events.json` so you don't re-post a story
  already covered. (We have shipped near-duplicates only on Bill's explicit call.)
- **Public-page hard constraints** (non-negotiable):
  - **No client names, ever** — no Figure / Arise / Skydio. Use program codenames only if needed.
  - **Geography: the rule covers ALL location references, not just supply-chain lines.**
    (Bill 2026-09-13 — widened after a card naming an internship location slipped the
    old supply-chain-only wording, and a *second* reference survived in page furniture.)
    - Cleared for publication: **Vietnam**, **Hong Kong**, **Singapore** — country/territory level only.
    - Never: **China / Chinese / PRC**, any city or province (Shenzhen, Guangzhou, Dongguan,
      Shanghai, Ho Chi Minh, Hanoi …), Taiwan, Macau, Mexico.
    - **This is enforced, not just written.** `build.py` runs a geography gate over the
      **rendered page** and exits 2 without writing `dist/` if a blocked name appears.
      It is checked on the rendered output because on 2026-09-13 all 42 source cards
      scanned clean while the built page still said "Shenzhen" — the term was in
      `index.template.html`, which a card-level scan cannot see. To change what is
      allowed, edit `BLOCKED_PLACES` / `ALLOWED_PLACES` in `build.py`.
  - Honest building-in-public voice. Plain headline. The page uses **no bold lead-ins**.

### 2. Author `events/YYYY-MM-DD-slug.md`
Frontmatter (YAML-lite, parsed by hand — keep it simple):
```
---
date: 2026-06-27          # required, ISO; also drives sort + "last updated"
tags: [persistence, architecture]   # required, list
title: Headline text       # required
link_text: Apply           # optional (renders a CTA link)
link_url:  https://...      # optional (pair with link_text)
pinned: true               # optional — keeps card at very top
---
Body...
```

### 3. Body markdown — SUPPORTED SUBSET ONLY (gotchas)
`build.py`'s renderer is deliberately minimal. Watch these:
- **Paragraphs split on blank lines.** Within one paragraph, all newlines collapse to spaces.
- **Bullets are NOT a list feature.** To show `•` lines stacked, put a **blank line between each
  bullet** so each becomes its own `<p>`. Consecutive bullet lines with no blank line collapse
  onto ONE line.
- **Italic = `_word_`** (underscores). Bold = `**word**`. Inline code = `` `code` ``.
  ⚠️ Single-asterisk `*word*` does **NOT** italicize — it prints literal asterisks. Convert to `_word_`.
- Everything else is HTML-escaped (quotes/ampersands render fine as entities).
- Ordering on the page: **pinned first, then date descending.**

### 4. Build
```
cd ~/.openclaw/workspace/mysynergy-technology-site
/usr/bin/python3 build.py
```
Then eyeball the rendered card in `dist/index.html` — confirm italics/bullets, and that no
literal `*...*` leaked.

### 5. Deploy to Hostinger (FTP) — surface 1 of 2
```
/usr/bin/python3 ~/scripts/intern_deadline_ftp_tech.py
```
Uploads `dist/*` → `/public_html/`. Creds: `~/.openclaw/.secrets/hostinger_ftp.json`.
Expect `5 uploaded, 0 failed`.

### 6. Verify LIVE (always — FTP success ≠ rendered correctly)
Cache-bust with a query param:
```
curl -s "https://mysynergy.technology/events.json?cb=$(date +%s)" | grep -c '"date"'   # card count
curl -s "https://mysynergy.technology/?cb=$(date +%s)" | grep -c '<your title>'         # title present
```
Confirm count incremented, newest date is correct, title + emphasis render.

### 7. Commit + push — surface 2 of 2, and the source of truth
The push is a DEPLOY, not just a backup: it is what publishes GitHub Pages. Stage `docs/` too.
```
git add events/<new>.md dist/ docs/
git commit -m "Publish build-log card: <Title> (Bill-approved YYYY-MM-DD)"
git push origin main
```
Then verify Pages the same way as Hostinger, cache-busted:
```
curl -s "https://mysynergy-io.github.io/technology-site/events.json?cb=$(date +%s)" | grep -c '"date"'
```
Pages can lag a push by a minute or two. A stale read is not a failed deploy — re-read before concluding.

### 8. Log
Add a CCL row (sheet `1034007769730948`): Type=Build, Status=PASS, Evidence = FTP result +
live-verify + commit hash.

---

## One-glance checklist
- [ ] No client name / geography violation; not a repeat
- [ ] Frontmatter complete (date, tags, title)
- [ ] Bullets blank-line-separated; `_italic_` not `*italic*`
- [ ] `build.py` run; local render eyeballed
- [ ] FTP deploy `5 uploaded, 0 failed`
- [ ] Hostinger verified (cache-busted) — count + title + render
- [ ] Committed + pushed to `origin/main` (stage `docs/` — this deploys Pages)
- [ ] **GitHub Pages verified (cache-busted) — the second surface, same checks**
- [ ] CCL logged
