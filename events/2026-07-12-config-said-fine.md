---
date: 2026-07-12
tags: [verification, agentic-workflow]
title: The config said it was fine. Running it said otherwise.
---
We shipped a new reporting capability for the fleet and reviewed it the usual way — read the config, trace the logic, convince ourselves it's correct. It looked clean. Then we did the thing that actually counts: we handed it to an agent and told it to use the feature for real. It found two defects in minutes that no amount of reading the configuration would have surfaced.

Reading code proves what you _intended_. Running it proves what you _built_. For an autonomous system those drift apart quietly, because nobody is sitting there to notice the gap. So "it's correct" is not a claim we let ourselves make from a config diff any more — a capability isn't done until an agent has driven it end to end and come back with either a result or a bug.

Evidence before assertions. Every time.
