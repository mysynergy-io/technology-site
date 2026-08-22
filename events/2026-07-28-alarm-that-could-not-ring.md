---
date: 2026-07-28
tags: [verification, agentic-workflow, architecture]
title: The alarm that could not ring
---
We audited our own monitoring and found an alarm for records that arrive but never get registered. It sat in the table with a twenty-minute threshold, next to the others, looking like a thing that worked.

Its trigger name appears nowhere else in the codebase. No classifier could ever produce it, and nothing scanned that sheet at all. It had never fired because it was structurally incapable of firing. Underneath it, a third of a test run had been sitting untouched for a full day.

The lesson is not that we forgot to wire it up. It's that the whole process — us included — reads silence as health. For a day, everyone looked at a quiet dashboard and concluded nothing was wrong, and the dashboard was quiet because it was disconnected. An alert you have never seen fire and an alert that cannot fire look identical from the outside, and the second one is worse than having no alert at all, because it occupies the space where a real one would go.

We now require every alarm to prove it can ring — a test that deliberately creates the condition and asserts the alert appears. Not that the code is correct. That the alarm _reaches someone_.
