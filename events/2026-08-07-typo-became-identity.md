---
date: 2026-08-07
tags: [architecture, supply-chain, verification]
title: A mistyped character became a permanent identity
---
Someone typed a zero where the letter belonged, in a free-text field on a delivery record. Nothing checked it, because nothing had ever needed to.

Downstream, that string was used to build the durable identity of the shipment in our ledger. From that moment the typo was load-bearing. The shipment became invisible to everything matching the real pattern — it was reported, correctly and uselessly, as a missing delivery. And it could no longer be fixed cheaply: the recorder is idempotent on that identity, so changing the number makes the lookup miss and appends a _second_ delivery instead of correcting the first. Two thousand units against an order of one thousand, on a ledger that only ever appends.

The defect is not the typing. People will always mistype, and a field that a person fills in by hand is not the place to be surprised by that. The defect is that an unvalidated free-text field silently became a key.

Our first proposal was to warn on a malformed number rather than block it, so a typo could never hold up an invoice. The reviewer rejected the framing outright: a malformed identifier is not cosmetic once it is durable identity, and a warning issued after the bad key exists is toothless. It now refuses before the record is written. The one bad record we already had is grandfathered by its exact combination — not by its shape, which would have let the next one through.
