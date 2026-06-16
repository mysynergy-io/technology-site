---
date: 2026-06-16
tags: [persistence, architecture, agentic-workflow]
title: What happens when you give an AI agent fleet a real database
---

Spent the day putting a real persistence layer under a multi-agent fleet. Three things I wanted to prove, all held.

• Structural firewall. Cost data and price data live in two separate ledgers — they physically cannot touch. The only place they meet is one audited sync, and margin is computed only at that join. You can't accidentally leak a supplier cost into a customer-facing number.

• Shadow, not cutover. Bidirectional sync every 10 minutes against the system-of-record, which stays the single source of truth. The new layer mirrors; it never overrides.

• A budget that actually stops. Set a hard spend cap, then had an agent try to run anyway. The system rejected it _before any execution_ — no run, no cost.

Verdict: foundation go, no cutover. Earn trust in shadow first.
