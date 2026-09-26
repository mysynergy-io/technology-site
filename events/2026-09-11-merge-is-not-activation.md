---
date: 2026-09-11
tags: [governance, architecture]
title: Merge is not activation
---

Code can exist without being allowed to act.

That sounds obvious, but software workflows often collapse several different events into one: merged means approved, approved means ready, ready means running.

We separated them.

A builder can produce an object. A reviewer can examine it. A certifier can say the evidence is sufficient. None of those actions turns the object on.

Activation is a separate authority decision.

The distinction matters most when the code touches external systems. A technically correct component is not automatically entitled to send a message, move money, change a record or publish something. Capability and authority are different things, and our system now treats them that way.
