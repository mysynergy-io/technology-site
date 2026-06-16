---
date: 2026-06-13
tags: [debugging, infrastructure]
title: Don't rebuild what regressed
---

Our agent's Telegram channel had run 7–16s for three months, then suddenly went sluggish. Instinct says redesign. Wrong move. We pulled the time-series, found a hard cliff at one specific change (an async-worker rewrite), and reverted just that. Back to ~4s.

Lesson: when something with a long working history breaks, it's a regression — find the cliff, don't redesign the system.
