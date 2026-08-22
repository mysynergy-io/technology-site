---
date: 2026-07-21
tags: [agentic-workflow, verification, supply-chain]
title: "Approved" is a claim, not a fact
---
Part of our supply-chain system acts on purchase orders the moment they're marked "approved" in the accounting system — pulls the document, records the order, moves on. The risk hides in plain sight: the software trusts a status, and anything that reaches that status gets acted on.

So it doesn't take the status on faith. An order is only meant to become approved by passing a submit step first. This week the watcher cleared the ones that had, and stopped on two that were marked approved but never submitted — it didn't pull them, it flagged them and asked. Automating a workflow shouldn't mean automating away the one check the workflow existed for.
