---
date: 2026-07-04
tags: [agentic-workflow, architecture]
title: A stale sentence is an outage that never pages anyone
---

Our AI agents each act under their own identity on a shared system of record — when one writes something, it's stamped as that agent, not a shared login. This week we found that three of them had been quietly convinced they couldn't do something they'd been able to do for months. Nothing errored. Their access was real and had been all along — but their operating instructions still read "you don't have this; hand it to someone else." So, faithfully, they did.

An agent that believes it lacks a permission behaves exactly like an agent that lacks it. The capability was real; the self-knowledge was missing — and for an autonomous system those are the same thing. We fixed the instruction, then re-ran each agent and asked it, cold, what it could do — because editing a document doesn't prove the agent understood it. The answer flipped from "I have to route this through someone else" to "I do this myself, and every action is stamped as me."

The instruction had drifted in the first place because there was no single source of truth — the guidance had been hand-copied to each agent and the copies quietly diverged. So the durable fix wasn't the wording. It was collapsing everything to one canonical copy, and giving each agent a way to ask the system directly _"who am I, and what can I touch?"_ instead of trusting a list that goes stale.

We watch credentials and networks like infrastructure. This was the reminder that what an agent _believes_ it can do is infrastructure too — and a stale sentence is an outage that never pages anyone.
