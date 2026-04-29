---
date: 2026-03-27
tags: [agentic-workflow]
title: Capability profiles per agent
---

Each agent in the OpenClaw fleet got a mechanical capability profile — what files it can read, which tools it can call, what shell commands it can execute. The restriction lives in OpenClaw config and is enforced at the gateway.

Agents cannot escalate themselves. Privilege creep, automated.
