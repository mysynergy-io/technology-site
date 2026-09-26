---
date: 2026-09-22
tags: [architecture, reliability]
title: Age is not proof of death
---

We used elapsed time as evidence that a lock owner had disappeared.

The certifier paused a perfectly live owner, waited until the lock looked old, reclaimed it, and let two consumers commit the same result.

Nothing crashed. Every individual step was reasonable. The assumption connecting them was not.

An old lock is not proof of a dead owner.

We replaced elapsed-time reasoning with ownership and fencing that can distinguish a superseded actor from the current one.

The general lesson is larger than locks. Time is evidence that something is old. It is not evidence that something is safe to take over.
