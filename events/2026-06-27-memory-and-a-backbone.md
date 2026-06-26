---
date: 2026-06-27
tags: [persistence, architecture]
title: Giving our agents a memory and a backbone
---

For months our AI agents could _do_ work but couldn't _remember_ it. Every order, price, and supplier note lived only in spreadsheets.

Over the last few days we wired up "Paperclip" — a real database backbone behind the fleet:

• A live Postgres database that holds the actual order/finance data

• An always-on service that syncs it both ways with our spreadsheets every 10 minutes

• A hard budget stop so a runaway agent can't rack up cost

• A built-in firewall so cost data and price data never sit in the same place

Result: the agents now read and write to a single source of truth instead of guessing. We ran it in shadow mode (watching, not touching the real books) and got a clean go/no-go to proceed — with cutover held until we're sure.

Building in public, one layer at a time.
