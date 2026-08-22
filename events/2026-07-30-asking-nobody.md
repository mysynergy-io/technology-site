---
date: 2026-07-30
tags: [agentic-workflow, verification]
title: We were asking for approval, and nobody was being asked
---
Our agents request human approval by commenting on the record and tagging the person who has to decide. The comments were going out. They read correctly. They notified no one — the platform only alerts on an account address, and a plain name with an at-sign in front of it is just prose. We had built a polite request into the void.

Nothing errored, because nothing failed. A comment was posted, exactly as designed. The only reason we found it is that a person asked why a decision was taking so long.

The one-line fix was the easy part. The durable fix was refusing to let any part of the system type a person's address at the point of use: there is now a single registry of who exists, every alert resolves a name through it, an unknown name raises rather than degrading, and a test fails the build if an address is hard-coded at a call site. When a person changes, one line changes.

A notification you can watch leave is not a notification anyone received. We check the receiving end now — and we found two more of these later, on a different surface, for the same reason.
