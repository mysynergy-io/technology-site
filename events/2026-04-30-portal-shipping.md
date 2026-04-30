---
date: 2026-04-30
tags: [internship, infrastructure, launch]
title: Three stages, one Worker
---

The application portal — three candidate-facing stages plus an agent-API path — is one Cloudflare Worker, one set of static pages, and a few KV + R2 buckets. No app server. No operator standing by during traffic. The form itself does the receiving.

We tested every stage end-to-end today, including the 90 MB video upload path, the magic-link expiry, and the duplicate-submit gate (it returns a clean 410 instead of a duplicate row).

Applications open tomorrow night at 20:00 HKT. We will be quiet on the platform for the first 24 hours and watch what real candidates do with it.
