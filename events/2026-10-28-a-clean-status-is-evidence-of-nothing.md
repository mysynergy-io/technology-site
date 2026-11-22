---
date: 2026-10-28
tags: [infrastructure, verification]
title: A clean status line was evidence of nothing
---

Our repositories list what they track file by file. Anything new is invisible by default. So a version-control status reporting "clean" says nothing about whether the code on disk is accounted for.

We built a control that separates two failures usually spoken of as one. Untracked: version control has never seen the file — no history, no review trail, no diff. Dirty: it is tracked, but the bytes on disk differ from the committed version, which means the reviewed program and the running program are not the same program.

First run, across 164 files reachable from scheduled jobs: nineteen untracked and three dirty. Ten of the untracked were attached to jobs currently loaded and running.

Our own prior note recorded this as "three files". That number came from the status command, which is blinded by exactly the mechanism this control was built to see around. The instrument had been wrong, not the tree.
