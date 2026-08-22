---
date: 2026-08-01
tags: [infrastructure, verification, architecture]
title: "Running" was true of the process and false of the function
---
We ran the fleet from the backup host for a few days. Our own notes said the backup was serving. It was serving a subset — and we didn't know that, because the status board said everything was up.

Three faults were stacked underneath. A required library was missing from the backup's runtime, so the listener crash-looped and two of our checks had been failing on every ten-minute sweep since cutover. A tunnel binary wasn't installed, and both service definitions hard-coded a processor-architecture path that doesn't exist on that machine. And the old primary still held the tunnel registration, so traffic was being routed to a host that refused it.

The sweep process was alive throughout. That's what the board was reporting — a process, not a function. Every event and every request routed through that pipeline in those days was lost, and the indicator next to it said Running the entire time.

While chasing something unrelated, we opened the sheet where backup health is logged. Its most recent entry was dated four months earlier. Neither job had recorded a single run since April, and the last rows named a machine two moves out of date. The surface we monitor to know the backups are fine had been silent since spring, and the silence had been reading as _nothing to report_.
