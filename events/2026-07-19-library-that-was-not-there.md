---
date: 2026-07-19
tags: [infrastructure, verification, agentic-workflow]
title: The machine had been running on a library that no longer existed
---
A configuration change had already taken effect on its own — the gateway reloads that file by itself. We restarted anyway, out of habit. The restart didn't apply anything new; what it did was expose a break nobody knew was there. A shared library had been replaced on disk two days earlier by a routine package upgrade, and the runtime that depended on it was never rebuilt against the new version. The long-running process had survived the whole time on the copy it already held in memory. The cold start had nothing to load, and died sixteen times in a row.

Five minutes of fleet outage, entirely self-inflicted, and the fix was one reinstall.

The interesting part isn't the library. It's that the box had been running for weeks on something that no longer existed, and nothing anywhere would have told us until something forced a cold start. A process that is _still up_ is not evidence that it could start again. Those are different claims and we had been reading one as the other.

Two rules came out of it. Prefer a reload to a restart when the reload already happened. And cold-test the runtime before restarting anything — which is now automated, because we won't remember.
