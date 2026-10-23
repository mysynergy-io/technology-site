---
date: 2026-10-18
tags: [reliability, verification]
title: A warning we believed we had sent
---

A check exists to tell us when one of our accounting connections stops being identifiable. It fired correctly, once.

The message failed to leave. The system had already recorded that we had been told, so it never tried again.

The condition stayed true, in silence, for forty-one days.

The record was written next to the attempt instead of after a confirmed delivery, so a failed send and a successful one looked identical from the inside. Both are now keyed to something actually accepting the message.
