---
date: 2026-07-24
tags: [infrastructure, verification]
title: Eighty-seven files were running in production and none of them were in version control
---
We went looking for something else and found that eighty-seven Python files had fallen through a deny-all ignore rule and were not under version control at all. Not stale, not on a branch — absent. They were running in production the entire time, doing real work, and any one of them could have been edited or lost with no history and no way to tell what changed. Ten test suites covering already-shipped work were in the same state.

Nothing was broken, which is exactly why it survived. The system worked, so nobody asked the question that would have surfaced it. The ignore rule was deliberate — deny everything, allow what we name — and it did precisely what it was told. The failure was that adding a file and adding it to the allow list are two actions, and only one of them is enforced by anything.

All eighty-seven went in that day. The durable change is the assumption we retired: _if it's running, it must be committed_ was never true, and we had no check that could have told us otherwise. We have one now.

There's a version of this in every codebase that has ever had a convenient ignore rule. It's worth twenty seconds to go and look.
