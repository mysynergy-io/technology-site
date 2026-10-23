---
date: 2026-10-15
tags: [debugging, verification]
title: Two wrong causes before the right one
---

Our independent review step stopped working. Nothing ships here without it, so the queue stopped with it.

First we blamed an expired credential and replaced it. No change. Then we reported that the account had lost its entitlement, which would have been a commercial problem with no technical fix. Also wrong.

The real cause was a tool twenty-one versions out of date, asking for something that had been withdrawn.

Both wrong answers explained the symptom, which is why we stopped at them. On a mandatory step, a comfortable explanation is the expensive one.
