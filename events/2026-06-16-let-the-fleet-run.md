---
date: 2026-06-16
tags: [agentic-workflow, verification]
title: Let the fleet run, I just watched
---

Handed the agent fleet 10 real business transactions and told it to replay them end-to-end. Each agent owned one slice of the work. I didn't touch a thing — watch-only.

Result: data 100% correct across all 10. Margins computed, no duplicates, every record matched its source.

But the automated checker passed 0 of 10 — flagged "missing evidence" on every single one.

The catch: the fleet wasn't wrong. _My checker was._ The evidence-matcher missed files named for the base order number when the line carried a suffix. The agents did their jobs; the scaffolding I wrote to grade them had the bug.

Building in public means publishing that part too.
