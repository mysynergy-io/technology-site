---
date: 2026-08-05
tags: [agentic-workflow, verification, architecture]
title: We have an AI review our AI's code, and we put it on a different vendor
---
As of this month, every code change to our supply-chain system is reviewed by a second AI before it runs. No size threshold. Fixes, refactors and test-only changes included, the plan as well as the implementation. Reviewing it after it lands doesn't count. The single exception is a live incident, which ships first and is reviewed immediately after, with the incident written down.

It runs on a different vendor's model, deliberately. A reviewer that shares a provider with the thing it reviews shares its blind spots and its bad days, and goes down in the same outage.

It has earned the gate in a month. It caught a value that crashed rather than merely slipping through, on the path that handles money. It refused a fix of ours as best-effort and made us do it fail-closed, pointing out that our own argument contradicted itself two sentences apart — and it was right. It stopped us replaying weeks-old gaps at real suppliers, where a repair would have read as a fresh request. It reframed what we had filed as a cosmetic typo as durable identity, which is what it actually was. And when we said we had checked everywhere for something, it asked once more, and found a seventh place we had missed.

The value isn't a second opinion. It's a reviewer with no stake in the design being right.
