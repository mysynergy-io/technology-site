---
date: 2026-09-01
tags: [verification, architecture]
title: The reviewer got a clean room
---

We used to talk about independent review as if independence were a property of the reviewer. It is not. It is also a property of the environment the reviewer is given.

A reviewer working inside the builder's normal workspace can inherit the same files, the same configuration, the same credentials and the same accidental assumptions. Two different people can still be looking through the same window.

So we changed the shape of the review. The object is reconstructed in a clean environment, the evidence is carried in explicitly, and the reviewer has to establish what is true from that material rather than from whatever happens to be lying around on the builder's machine.

The goal is not cleanliness for its own sake. It is to make the answer reproducible: if the review depends on an invisible local fact, it is not yet evidence.
