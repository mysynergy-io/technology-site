---
date: 2026-06-20
tags: [agentic-workflow, architecture]
title: Automate everything except the decision
---

Automating a step that moves money is where automation earns its scary reputation. So we drew the line on purpose: automate everything up to the irreversible act — and never through it.

When a transaction is ready, the system now prepares the financial document on its own and checks it against every rule. Then it stops. Nothing is committed until a person approves it, and up to that point it has written nothing that counts. The machine does the preparation; the human keeps the decision.

The part we're proud of is what approval actually means here. It isn't a rubber stamp on a snapshot taken minutes or hours ago. At the instant you approve, the system re-checks the live state against what it proposed — and if anything has moved since it asked, it cancels itself and asks again rather than acting on stale numbers. Approving the present, not the past.

Around all of it: the pipeline runs against a sandbox set of books first, never the real ledger; it keeps a hard wall between cost data and price data; and when something doesn't reconcile, it raises a flag instead of guessing. Automation should be most aggressive where mistakes are cheap, and most humble where they're permanent.
