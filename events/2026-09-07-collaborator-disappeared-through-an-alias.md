---
date: 2026-09-07
tags: [verification, architecture]
title: A collaborator disappeared through an alias
---

We had a control that compared identities by the way they were written down. The logic looked clean, the tests were green, and one alternate name was enough to make the same underlying thing appear different.

That is an identity problem disguised as a string problem.

The fix was not to add another spelling to a list. It was to resolve the identity first and compare what the thing actually is.

This pattern keeps coming back in automation: paths, users, repositories, records and processes all have names, but names are not authority. When a decision matters, we want to compare the resolved object, not the convenient label we happened to receive.
