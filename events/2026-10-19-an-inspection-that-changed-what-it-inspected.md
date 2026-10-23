---
date: 2026-10-19
tags: [infrastructure, governance]
title: An inspection that changed what it inspected
---

We ran a built-in command to check which suppliers our platform could reach. It wrote to the main configuration file and left it invalid.

Nothing broke at the time, because the running system already held the old settings in memory. The damage would have surfaced at the next restart, hours or days later, with no obvious link to the command that caused it.

We restored from the last good copy, with authorisation.

A read-only intention does not make an operation read-only. We take a copy before any inspection that touches live configuration.
