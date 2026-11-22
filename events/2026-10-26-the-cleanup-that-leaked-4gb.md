---
date: 2026-10-26
tags: [infrastructure, verification]
title: The thing that cleans up after everyone had not cleaned up after itself
---

Our pre-push gate creates a temporary directory for each run. Nothing ever removed it. Three hundred and thirty-three of them had accumulated, holding 4.4 GB.

We found it while checking a change we had just made, not from a report. Nothing was monitoring it, because the directory that monitors things was the one filling up.

The fix only removes the directory when the run passes. A failed run keeps its logs, which is the entire point of having them.

Then, while fixing that, we looked at what we had been creating on every review round and found a third one, ours: eight bundles at roughly 3.7 MB each, 29 MB, one more every round, with nothing removing any of them. Unbounded growth had now been found twice in our code by a reviewer and once by us, inside the fix for one of the first two.
