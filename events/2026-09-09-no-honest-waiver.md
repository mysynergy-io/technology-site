---
date: 2026-09-09
tags: [governance, verification]
title: We tried to write a waiver and found there was no honest one
---

We had a control that was operationally inconvenient, so we asked the obvious question: can we write a narrow exception?

We tried. Every version of the exception either weakened the thing the control was meant to guarantee or moved the same risk somewhere harder to see.

So the answer was no waiver.

That is not a failure of flexibility. It is the control doing its job. If an exception cannot be stated without destroying the property being protected, the correct design may be to make the exception impossible.

A system that can always be overridden is not fail-closed. It is fail-open with paperwork.
