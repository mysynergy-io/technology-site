---
date: 2026-08-12
tags: [supply-chain, verification, agentic-workflow]
title: Three days on site with the people who use it
---
Our supply-chain system had been running in test for months and passing. This month our project lead spent three days in Vietnam, at the premises of the supplier whose operations lead owns two of its sheets, training her team and watching them work.

Before the visit we did the obvious check: does she have what our existing tester has? She didn't — she was short six screens, all of them the delivery and fulfilment chain she personally owns, including the one report that summarises her own two sheets. She was the only tester in the system without it. We would have run three days of training with the person whose work it describes unable to open it.

They came back with eleven problems. We fixed none of them on the spot, deliberately — every one was diagnosed against live code and data first, because the fastest way to turn one report into three defects is to fix it in the room. Then we asked our reviewer to attack the diagnosis, and it overturned the two we had confidently marked _no defect_. Both were real. One of them worked only while an order line stayed with a single supplier, which made it operational discipline we had been calling a system guarantee.

Then it named ten more scenarios missing from the list of eleven entirely. Nobody had reported those, because nobody had hit them yet.

Three days in a room with the people who do the work found more than the previous month of green test runs. That isn't a criticism of the tests. It's what tests are for, and what they can't do.
