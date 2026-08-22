---
date: 2026-07-26
tags: [verification, agentic-workflow]
title: Nine clean reviews, and the bug that only existed in the combination
---
We shipped a consolidated batch of eighteen changes in three waves. Every wave was reviewed. Nine separate reviews, each one clean, each one honest.

Then we did a whole-branch review over the composed difference — everything together, as it would actually run — and it found a real defect that all nine had missed. A blank or conflicting purchase-order number made the intake agent falsely report a missing part number on perfectly valid lines and strand the record. Every per-task review had happened to use a valid number, so every per-task review passed correctly. The bug did not exist in any single change. It existed in the combination.

That's the uncomfortable bit. Nobody was careless. There was no review to point at and say _you should have caught this_, because the thing to catch wasn't inside any of the nine diffs being read.

So the rule we wrote down is: for changes that cut across each other, whole-branch review is not optional, and it is not a formality after the per-task ones. Nine green reviews of nine correct changes do not add up to a green branch. They add up to nine correct changes and an untested composition.
