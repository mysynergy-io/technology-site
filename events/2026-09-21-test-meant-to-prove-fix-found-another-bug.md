---
date: 2026-09-21
tags: [verification, engineering]
title: The test we added to prove the fix found another bug
---

We wrote two adversarial tests because our evidence was incomplete.

One passed.

The other showed that a lifecycle function could still change state without valid ownership. We had fixed the named mutation path and left a neighbouring convenience path unfenced.

That is the kind of defect code review can miss because the implementation reads sensibly. The falsifier did not ask whether the code looked right. It tried to perform the forbidden action.

It succeeded.

So the candidate was changed before review and the test became permanent.

A useful test is not one that proves the implementation is correct. It is one that has a genuine chance of proving you wrong.
