---
phase: "04"
plan: "02"
subsystem: core-infrastructure
tags:
  - asyncio
  - subprocess
  - semaphore
  - race-condition
  - concurrency
dependency-graph:
  requires:
    - 04-01
  provides:
    - stable-subprocess-execution
  affects: []
tech-stack:
  added: []
  patterns:
    - asyncio.Semaphore for limiting concurrent subprocesses
key-files:
  created: []
  modified:
    - src/monocli/async_utils.py
    - tests/test_async_utils.py
decisions:
  - Use asyncio.Semaphore(3) to limit concurrent subprocess execution
  - Keep semaphore locked for entire subprocess lifecycle including cleanup
  - Add await proc.wait() in finally block to ensure proper cleanup
  - Add concurrency tests for race condition verification
metrics:
  duration: "11m"
  completed: "2026-02-08"
---

# Phase 4 Plan 2: Fix asyncio subprocess race condition Summary

## One-Liner

Fixed asyncio InvalidStateError exceptions by adding asyncio.Semaphore(3) to limit concurrent subprocess execution and ensure proper cleanup.

## What Was Delivered

Fixed the race condition in `run_cli_command()` that was causing `asyncio.exceptions.InvalidStateError: invalid state` exceptions in logs when concurrent CLI operations ran simultaneously.

### Key Changes

1. **src/monocli/async_utils.py:**
   - Added module-level semaphore: `_subprocess_semaphore = asyncio.Semaphore(3)`
   - Wrapped subprocess creation and communication in `async with _subprocess_semaphore:` block
   - Added proper cleanup with `await proc.wait()` in finally block
   - Extended semaphore protection to include entire subprocess lifecycle

2. **tests/test_async_utils.py:**
   - Added `TestConcurrentSubprocesses` test class with race condition tests
   - `test_concurrent_subprocesses_no_race_condition()`: Runs 5 concurrent subprocesses to verify no exceptions
   - `test_semaphore_limits_concurrent_execution()`: Verifies semaphore value is 3

## Verification

- ✅ Semaphore value is 3 (verified programmatically)
- ✅ No InvalidStateError in logs after fix (tested with app run)
- ✅ Concurrent subprocess tests pass (5 concurrent echo commands)
- ✅ All existing tests pass (172 passed, 7 pre-existing failures unrelated to this fix)
- ✅ Application runs stable with concurrent CLI operations

## Implementation Details

### Root Cause
When GitLab and Jira authentication checks ran simultaneously, they competed for asyncio transport resources. The Python asyncio subprocess transport cleanup has a race condition when multiple subprocesses terminate concurrently.

### Solution
1. **Semaphore Protection**: Limit to 3 concurrent subprocesses using `asyncio.Semaphore(3)`
2. **Lifecycle Management**: Keep semaphore locked for entire subprocess lifecycle (creation → communication → cleanup)
3. **Proper Cleanup**: Added `await proc.wait()` in finally block to ensure process reaping before releasing semaphore

### Why Semaphore(3)?
- Value of 3 is reasonable for CLI tools (allows concurrent auth checks + data fetching)
- Small enough to prevent resource contention
- Large enough to not impact performance under normal operation

## Commits

- `4fcfaac`: fix(04-02): add semaphore to prevent subprocess race conditions

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Improved subprocess cleanup in timeout handling**

- **Found during:** Task 1 implementation
- **Issue:** Original code called `proc.kill()` but didn't wait for process to terminate
- **Fix:** Added `await proc.wait()` after `proc.kill()` to ensure proper cleanup
- **Files modified:** src/monocli/async_utils.py
- **Impact:** Prevents zombie processes and ensures semaphore is only released after full cleanup

**2. [Rule 1 - Bug] Extended semaphore scope to include result processing**

- **Found during:** Testing verification
- **Issue:** Original implementation released semaphore before processing stdout/stderr
- **Fix:** Moved all processing inside `async with _subprocess_semaphore:` block
- **Files modified:** src/monocli/async_utils.py
- **Impact:** Ensures complete subprocess isolation until fully cleaned up

### Note on Test Suite
Some UI tests have pre-existing failures unrelated to this fix:
- `test_main_screen_renders_both_sections` - Missing DOM fixture
- `test_tab_updates_visual_indicator` - CSS query issues
- Various adapter tests with mismatched signatures

These failures existed before this change and are documented in previous plans.

## Next Phase Readiness

The asyncio subprocess race condition is now resolved. The application:
- Runs without InvalidStateError exceptions
- Handles concurrent CLI operations reliably
- Has comprehensive tests for subprocess concurrency

No blockers for future development.

## Self-Check: PASSED

- [x] Modified files exist and have correct content
- [x] Commit 4fcfaac exists in repository
- [x] Semaphore value verified as 3
- [x] No InvalidStateError in logs
- [x] All concurrency tests pass
