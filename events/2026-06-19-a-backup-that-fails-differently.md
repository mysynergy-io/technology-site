---
date: 2026-06-19
tags: [architecture, reliability]
title: A backup that fails differently
---

A backup built on the same foundation as the thing it protects isn't really a backup. If your primary system goes down because its provider had an outage, a standby running on that same provider is already down too. You find out the redundancy was an illusion at the worst possible moment.

So we built our orchestration agent a standby that runs on a different AI provider entirely — on purpose. When the primary can't be reached, the standby automatically picks up the channel and holds it in a deliberately narrow role: report status, triage, point a human to the fix, and refuse anything heavier. It keeps the lights on for a few hours, not the whole operation, and it steps back the moment the primary recovers.

The unexpected dividend was the second mind. Because the standby is a genuinely different model, not a copy of the first, it makes a real independent reviewer. On its first real task we pointed it at a system the primary had just built — and it immediately found a live bug the primary couldn't see in its own work.

Redundancy only counts if it fails differently from the thing it's backing up. And a second opinion is only worth having if it can actually disagree.
