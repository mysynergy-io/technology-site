---
date: 2026-10-27
tags: [security, verification]
title: We said credentials were denied. They were in the environment.
---

We built a sandbox to run our own tooling with no access to secrets, and the commit message said so: credentials denied.

A reviewer disagreed with the wording. Broad filesystem denials, she said, do not establish that credentials are unreachable — environment variables and inherited descriptors are still open channels.

She was right, and worse than she put it. We measured the environment the tool was built in and found three live credentials sitting in it, inherited by every child process, including every test we ran under a profile whose own commit message claimed they were denied. Blocking the secret store did nothing about them.

The claim was false and we withdrew it. What the denials established was that the _secret store_ was unreadable, not that credentials were unreachable. The sandbox now launches with an empty environment, and we proved it with a planted test credential: demonstrably inherited by an ordinary child, demonstrably stripped inside the sandbox. A check for "no secrets visible" passes trivially in a place that never had any.
