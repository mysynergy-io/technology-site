---
date: 2026-06-16
tags: [delivery-management, agentic-workflow]
title: The golden rule of delivery management
---

A purchase order is a promise of quantity. We track every one through four states: received → placed → shipped → invoiced.

The golden rule: for each component, everything placed to suppliers over time = ordered quantity × bill-of-materials factor. When the deal closes cleanly, ordered = placed = shipped = invoiced.

The math is the easy part. The real work is the exceptions: multi-part assemblies, parts dual-sourced across two suppliers, a BOM that lags what was actually bought, one invoice covering several deliveries. The rule handles ~90% deterministically. For the other 10%, the agent flags for help instead of guessing — asking is a feature, not a failure.
