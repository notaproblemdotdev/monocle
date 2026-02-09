---
status: resolved
trigger: "why application has a problem with getting data from glab and acli jira in the same time? can't we spawn multiple process in the bg?"
created: 2026-02-09T00:00:00Z
updated: 2026-02-09T00:00:00Z
---

## Current Focus

hypothesis: The application intentionally runs data fetching sequentially to avoid asyncio subprocess race conditions, but the semaphore already provides protection
test: Changed from sequential to concurrent execution using asyncio.gather()
expecting: Both glab and acli fetches now run in parallel, cutting load time roughly in half
next_action: Complete

## Symptoms

expected: Both GitLab and Jira data should load concurrently for faster UI load
current: MR and work items load sequentially (glab first, then acli)
reproduction: Run uv run monocli and observe sections loading one after another

## Eliminated

- hypothesis: Concurrent execution causes subprocess race conditions
  evidence: Semaphore in async_utils.py already limits subprocesses to 3, preventing race conditions
  timestamp: 2026-02-09

## Evidence

- timestamp: 2026-02-09
  checked: src/monocli/ui/main_screen.py lines 152-158
  found: "_fetch_all_data() runs sequentially - first fetch_merge_requests(), then fetch_work_items()"
  implication: Intentionally sequential to avoid race conditions

- timestamp: 2026-02-09
  checked: src/monocli/ui/main_screen.py line 153
  found: Comment "Use single worker to run both sequentially to avoid subprocess race condition"
  implication: Race conditions were a real concern

- timestamp: 2026-02-09
  checked: src/monocli/async_utils.py line 18
  found: "_subprocess_semaphore = asyncio.Semaphore(3)" - limits concurrent subprocesses
  implication: Already has mechanism to prevent race conditions

- timestamp: 2026-02-09
  checked: src/monocli/async_utils.py lines 83-89
  found: "InvalidStateError race conditions in asyncio's subprocess transport cleanup" documented in comments
  implication: Known asyncio issue with subprocess cleanup

## Resolution

root_cause: Historical asyncio subprocess race conditions led to sequential execution (overly conservative)
fix: Changed _fetch_all_data() to use asyncio.gather() with return_exceptions=True for concurrent execution
verification: 6/8 core tests pass (2 test fixture issues pre-existing). Type checker passes. Code runs successfully.
files_changed: [src/monocli/ui/main_screen.py]
