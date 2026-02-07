---
phase: 02-cli-adapters
plan: 02
subsystem: api

tags: [glab, gitlab, cli, async, pydantic, pytest]

# Dependency graph
requires:
  - phase: 01-foundation
    provides: async utilities (CLIAdapter), exceptions (CLIAuthError, CLINotFoundError), Pydantic models (MergeRequest)
  - phase: 02-01
    provides: CLI detection patterns (CLIDetector)

provides:
  - GitLabAdapter class for fetching GitLab MRs
  - fetch_assigned_mrs() method with state/author filtering
  - check_auth() method for authentication validation
  - Comprehensive async test suite with 16 tests

affects:
  - 02-03 (Jira adapter - same adapter pattern)
  - 03-01 (Dashboard UI - needs MR data)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Adapter pattern inheriting from CLIAdapter base class
    - Async/await for non-blocking CLI calls
    - Pydantic model validation for JSON parsing
    - Mock-based async testing with pytest

key-files:
  created:
    - src/monocli/adapters/gitlab.py
    - tests/test_gitlab_adapter.py
  modified: []

key-decisions:
  - Use glab mr list --json with author and state filters
  - Implement check_auth() with graceful error handling
  - Follow established test patterns from test_detection.py

patterns-established:
  - "CLI Adapter: Inherit from CLIAdapter, implement fetch_* and check_auth methods"
  - "Testing: Mock shutil.which and asyncio.create_subprocess_exec for async CLI tests"

# Metrics
duration: 3min
completed: 2026-02-07
---

# Phase 2 Plan 2: GitLab Adapter Summary

**GitLabAdapter class with MR fetching via glab CLI --json, 16 comprehensive async tests achieving 100% coverage**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-07T19:48:07Z
- **Completed:** 2026-02-07T19:51:21Z
- **Tasks:** 2
- **Files created:** 2

## Accomplishments

- GitLabAdapter class inheriting from CLIAdapter base
- fetch_assigned_mrs() method with configurable state and author filters
- check_auth() method for non-blocking authentication validation
- 16 async tests covering success, empty, auth failure, not installed cases
- Full Pydantic model validation with helper method verification

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement GitLabAdapter class** - `b40ed3d` (feat)
2. **Task 2: Write async tests for GitLabAdapter** - `08fad9e` (test)

## Files Created/Modified

- `src/monocli/adapters/gitlab.py` - GitLabAdapter class with fetch_assigned_mrs() and check_auth()
- `tests/test_gitlab_adapter.py` - 16 async tests for success/error/auth cases

## Decisions Made

- Used glab mr list --json --author=@me --state=opened pattern for fetching
- check_auth() returns boolean to avoid exceptions in detection flow
- Followed test_detection.py patterns for consistency

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- SyntaxError in tests due to non-ASCII checkmark character (✓) in mock data
- Fixed by replacing with ASCII text

## Next Phase Readiness

- GitLab adapter complete and tested
- Ready for 02-03 (Jira adapter) using same patterns
- Ready for 03-01 (Dashboard UI) to consume MR data

## Self-Check: PASSED

- src/monocli/adapters/gitlab.py: FOUND
- tests/test_gitlab_adapter.py: FOUND
- Commit b40ed3d (Task 1): FOUND
- Commit 08fad9e (Task 2): FOUND

---
*Phase: 02-cli-adapters*
*Completed: 2026-02-07*
