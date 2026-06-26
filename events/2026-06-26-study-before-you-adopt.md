---
date: 2026-06-26
tags: [architecture, agentic-workflow]
title: Study an open-source framework before you adopt it
---

We've been evaluating an open-source agent-orchestration framework to sit under our own fleet. The tempting move is to adopt the whole thing and refactor later. We did the opposite — read it one layer at a time, and held all adoption until we actually understood each layer.

So far we've mapped three: orchestration (how agents take work and report back), persistence (an 85-table data model with a real two-ledger split between cost and price), and execution (how a task actually runs). Each layer taught us where it fits us and where it doesn't — its model assumes software repos and diffs; our deliverables are physical packaging and documents, so parts of it map cleanly and parts don't.

The discipline is the point. Understanding before adopting is slower up front and far cheaper than ripping out something you bolted on before you understood it.
