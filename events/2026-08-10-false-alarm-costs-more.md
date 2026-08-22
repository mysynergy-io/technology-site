---
date: 2026-08-10
tags: [verification, agentic-workflow, architecture]
title: A false alarm costs more than the outage it warns about
---
We test against a sandbox company in our accounting system. It is rebuilt roughly every month under a new internal identifier. Our code pins that identifier and fails closed when it stops matching — which is the correct behaviour, and completely silent. Writes simply stop, and someone mid-test watches purchase orders quit working with no explanation.

So we built a watcher to tell people before it happens. Two rules shaped it, and both came out of the review rather than the design.

A failed read is never a reset. A dead connection, a rejected credential, an empty list, or no sandbox visible at all — every one of those returns _cannot tell_ and sends nothing. It is tempting to treat "I can't see it" as "it's gone," and that is how you send someone chasing a change that never happened. Do that twice and the group learns to ignore the alert, which costs far more than the outage the alert exists for.

And delivery outranks duplicate suppression. Our first version recorded the event as seen and _then_ sent the message, so a single failed send would have marked it handled and nobody would ever have been told. Inverted: it records what it saw separately from what it successfully delivered, and keeps trying until someone has actually been told.

An alert system's job is not to notice. It's to be believed, and to arrive.
