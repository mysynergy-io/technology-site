---
date: 2026-10-25
tags: [verification, infrastructure]
title: The tests were writing into the log they measured
---

We put our test suite inside a sandbox that denies writes outside its own directory. Thirty-six tests failed. Twenty-eight of them failed trying to write to live production paths.

The sandbox denying those writes was the control working. The question was what had been happening without it. So we ran five of the twenty-eight unconfined and measured the log before and after: 272 bytes appended to a live production log, and its last three lines were from that run.

Those lines name a row number and an editor address that exist only in our fixtures. In a live log they are indistinguishable from a real event, on a real row, by a real person. The log is shared with a service that was running at the time, and our pre-push check ran 224 test files unconfined on every push — including the one that found this.

A test that writes into the system it measures is not a test. It is a second writer nobody declared.
