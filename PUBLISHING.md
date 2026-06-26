# Publishing to mysynergy.technology — process runbook

How a build-log card gets from idea to the live public site. Two flows: the weekly
**recommendation** (automated) and the **publish** (manual, gated by Bill).

Last verified end-to-end: **2026-06-27** (JOR-20260627-002).

---

## Architecture (know this first)

- **Live site is served by Hostinger over FTP** — NOT GitHub Pages.
  Live = whatever sits in Hostinger `/public_html/`, which is a copy of local `dist/`.
- **`build.py` only writes `dist/`.** It renders `events/*.md` → `dist/index.html` + `dist/events.json` (+ css/js).
- **Source of truth = the git repo** `github.com/mysynergy-io/technology-site` (branch `main`). FTP is the deploy; git is the backup/history.
- ⚠️ **Ignore the `docs/` folder.** It is a stale, divergent leftover (frozen ~2026-06-11). `build.py` does not write it. Do not edit or trust it. (Open cleanup: JOR-20260627-001.)
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
  - Supply-chain geography may sit at **"China and Vietnam"** — no Mexico, nothing more specific.
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

### 5. Deploy to Hostinger (FTP)
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

### 7. Commit + push (source of truth)
```
git add events/<new>.md dist/
git commit -m "Publish build-log card: <Title> (Bill-approved YYYY-MM-DD)"
git push origin main
```

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
- [ ] Live verified (cache-busted) — count + title + render
- [ ] Committed + pushed to `origin/main`
- [ ] CCL logged
