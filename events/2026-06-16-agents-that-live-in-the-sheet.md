---
date: 2026-06-16
tags: [agentic-workflow, architecture]
title: Agents that live in the sheet
---

Most automation reads a spreadsheet, does something elsewhere, then writes a result back. We turned that inside out. The sheet isn't a data source the agent visits — it's the room the agent lives in.

An agent assigned to a sheet watches its own rows, acts when one changes, and writes its work back in place. The sheet is the interface, the queue, and the audit trail at once — what you see is exactly what the agent sees.

The guardrails aren't prompts politely asking it to behave. They're deterministic code gates around every write: an agent can only touch its own rows, only the columns it owns, and every change is logged. We ran it overnight against dozens of adversarial scenarios — zero improper edits.

When the operating surface is the same one your team already reads, nobody has to ask the agent what it did. It's right there.
