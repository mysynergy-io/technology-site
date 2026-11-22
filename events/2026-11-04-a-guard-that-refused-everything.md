---
date: 2026-11-04
tags: [verification, agentic-workflow]
title: A guard that refuses everything looks exactly like a guard that works
---

We added an identity check so that one of our agents verifies which account it is acting as before it posts anything.

The check could never match. Escaping was consumed passing through the layers that generated the code, and the comparison it produced was impossible to satisfy. We measured it: the correct identity and a deliberately wrong one both aborted.

It failed closed, which is precisely why it looked fine. Nothing posts. No alarming error, no corrupted data. The agent would simply never have spoken, and every test of the form "a wrong identity is refused" would have passed.

Fail-closed is normally the behaviour to reach for, so a guard whose broken state _is_ the safe state gives no signal at all. An over-permissive guard announces itself through damage. An over-restrictive one announces itself through absence, and absence is also what a working guard produces. The only thing that separates them is a positive control: prove the guard lets the right thing through, not just that it stops the wrong one.
