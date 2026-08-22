---
date: 2026-08-03
tags: [verification, infrastructure]
title: Five checks that fail open, in the plan written to prevent exactly that
---
After the failover we wrote a disaster-recovery plan with guards in it, so the thing that had just happened could not happen again. Then it was reviewed, and the review found five defects — every one of them in a guard, and every one the same disease the plan was written to cure.

A guard meant to refuse a dangerous sync blocked only on an empty value or one exact lowercase string; anything truncated or corrupted sailed through, including the case that caused the incident. A restore probe looped over the output of a remote command, so when the connection was refused the loop body never ran and the check passed having examined zero files. A gap counter was set inside a piped loop and lost to a subshell, so the preflight always exited clean. The marker file that decides which machine is the primary was itself copied by the sync it governs — the mechanism would have destroyed itself on the first successful run. And a heartbeat assertion read the log file that is the job's own output, so a blocked run refreshed it and passed.

Not one was found by the person who wrote them, and that person was writing the doctrine against this exact failure at the same time. Knowing the pattern by name is not protection from it. An independent reader is.
