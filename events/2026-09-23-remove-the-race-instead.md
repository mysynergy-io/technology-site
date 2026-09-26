---
date: 2026-09-23
tags: [architecture, reliability]
title: We stopped fixing the race and removed the race instead
---

We kept finding new interleavings around the same operation.

An owner would check that it was current. Another owner would take over. Cleanup would remove a thing that now belonged to the successor. Each fix tightened the comparison, and each new schedule found another moment where the target could change between check and effect.

Eventually the answer became obvious: stop deleting the target.

The final design changed the mechanism so ownership generations are append-only and claims cannot expose an empty intermediate state. The dangerous operation disappeared instead of acquiring another guard.

Concurrency bugs are often described as timing problems. Sometimes the better fix is to remove the operation whose correctness depends on timing.
