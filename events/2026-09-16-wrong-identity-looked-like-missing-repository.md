---
date: 2026-09-16
tags: [security, verification]
title: The wrong identity looked exactly like a missing repository
---

We tried to access a private review repository and got "not found."

The repository was there.

The problem was the identity making the request. An ambient credential belonged to a different account, and a private repository quite correctly looked nonexistent to it.

The dangerous part is how plausible the wrong conclusion was. "Repository missing" and "wrong identity cannot see repository" produced the same surface result.

So identity is now checked numerically before the work begins, not inferred from whichever credential helper happens to answer first.

A lot of security failures do not look like security failures. They look like ordinary missing data.
