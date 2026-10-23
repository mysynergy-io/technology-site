---
date: 2026-09-29
tags: [reliability, infrastructure]
title: The monitor used up the capacity it was watching
---

We added a monitor so an incoming approval could not sit unnoticed. It checked often, because delay on that queue costs us days.

It checked often enough to exhaust the service limit, which blinded the very queue it was protecting.

Days earlier, an older version had read a reply while it was still being written, decided it had seen the whole thing, and marked the item handled.

A monitor is not a free addition. It spends the same quota and competes with the work it observes, so it needs its own failure review rather than being treated as a window onto someone else's.
