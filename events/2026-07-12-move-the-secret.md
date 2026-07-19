---
date: 2026-07-12
tags: [security, architecture, agentic-workflow]
title: Don't deny the tool — move the secret out of the room
---
When you give an AI agent a shell, the honest question isn't "which commands do we forbid" — it's "what can it read." We checked, and the answer was uncomfortable: an agent running a task could reach the same credential files the rest of the system used. Denying a tool in config didn't change that; the process still had the file.

So we stopped trying to fence the tool and moved the thing worth stealing. Secrets now live behind a broker that runs as its own user. An agent asks the broker to _perform_ an action — send this mail, sign this request — and the broker does it and hands back the result. The token itself never enters the agent's sandbox. The blast radius of a compromised agent shrank from "every secret on the box" to "the specific actions the broker will take on its behalf."

The lesson we keep re-learning: a rule that _says_ no is not the same as a wall that _is_ no. Configuration is a promise; isolation is a fact. We'd rather build the fact.
