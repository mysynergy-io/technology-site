---
date: 2026-10-30
tags: [infrastructure, debugging]
title: One credential vanished and seven jobs failed quietly for fifty days
---

A credential stored on this machine no longer existed. Seven scheduled jobs read it.

This was not the usual explanation, where a background service cannot unlock the store. We checked by hand, in an ordinary shell: the item was simply gone. A sibling credential was still there, so the store itself was fine.

The useful part was the cliff. Four sync jobs had a last good run on 9 or 10 September and then fifty-odd consecutive days of nothing but failures. A listener that resolves identifiers returned thirty-two real ones on 9 September and none since — every single call after that returned empty, and kept going.

Fifty days is not how long it takes to notice an outage. It is how long it takes to notice one that reports success. Four of the jobs are fixed. The listener is not, and we are not going to describe it as healthy until it is.
