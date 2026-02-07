---
phase: 02-cli-adapters
plan: 03
subsystem: api
tags: [jira, acli, pydantic, async, pytest]

# Dependency graph
requires:
  - phase: 01-foundation
    provides: CLIAdapter base class, JiraWorkItem model, exceptions
  - phase: 02-cli-adapters
    provides: Detection pattern from 02-01, adapter pattern from 02-02
provides:
  - JiraAdapter class for fetching Jira work items via acli CLI
  - Comprehensive async test suite with mocked subprocess
  - Auth pattern for acli authentication checking
  - Bug fix: Added 'not authenticated' to CLIAuthError patterns
affects:
  - 03-dashboard-ui (will use JiraAdapter for data fetching)
  - Future platform adapters (follows same pattern)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - CLIAdapter inheritance pattern for platform adapters
    - Async subprocess mocking for tests
    - Auth pattern: whoami command for auth checking
    - fetch_and_parse() generic method for JSON→Pydantic

key-files:
  created:
    - src/monocli/adapters/jira.py
    - tests/test_jira_adapter.py
  modified:
    - src/monocli/exceptions.py (added 'not authenticated' pattern)
    - src/monocli/adapters/__init__.py (export JiraAdapter)

key-decisions:
  - Use 'acli whoami' for lightweight auth check (consistent with pattern)
  - Map Jira API URL to browser URL by replacing /rest/api/2/issue/ with /browse/
  - Support custom status filters for flexible querying
  - Support custom assignee filters for team use cases

patterns-established:
  - "Adapter auth check: Use lightweight command like whoami"
  - "Error pattern matching: Include common auth error variations"
  - "URL transformation: Convert API URLs to browser URLs in model"
---

# Phase 2 Plan 3: Jira CLI Adapter Summary

**JiraAdapter with acli integration, 8 async tests covering success/empty/auth/not-installed cases, and bug fix for 'not authenticated' error detection**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-07T19:48:45Z
- **Completed:** 2026-02-07T19:51:22Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- JiraAdapter class inheriting from CLIAdapter base class
- fetch_assigned_items() method using `acli jira issue list --json --assignee=@me --status=!=Done`
- check_auth() method using `acli whoami` for lightweight auth verification
- Proper field mapping from acli JSON to JiraWorkItem (key, summary, status, priority, assignee, url)
- 8 comprehensive async tests with mocked subprocess (no CLI required for testing)
- Fixed CLIAuthError pattern matching to detect 'not authenticated' errors from acli

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement JiraAdapter class** - `4ac43fc` (feat)
2. **Task 2: Write async tests for JiraAdapter** - `d55fe7c` (test)
3. **Export JiraAdapter from adapters package** - `c6c07c5` (refactor)

**Plan metadata:** `TBD` (docs: complete plan)

## Files Created/Modified

- `src/monocli/adapters/jira.py` - JiraAdapter class with fetch_assigned_items() and check_auth()
- `tests/test_jira_adapter.py` - 8 async tests covering success, empty, auth failure, not installed cases
- `src/monocli/exceptions.py` - Added 'not authenticated' to AUTH_PATTERNS (bug fix)
- `src/monocli/adapters/__init__.py` - Export JiraAdapter for clean imports

## Decisions Made

- **Whoami for auth check:** Following the pattern established in GitLabAdapter, using `acli whoami` as the lightweight auth verification command. This is fast and doesn't fetch actual data.
- **URL transformation in model:** The JiraWorkItem model already handles converting API URLs (`/rest/api/2/issue/PROJ-123`) to browser URLs (`/browse/PROJ-123`) via its `url` property.
- **Flexible filtering:** Support custom status_filter and assignee parameters to allow different query scenarios (e.g., only "In Progress" items, or items assigned to team members).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added 'not authenticated' to CLIAuthError.AUTH_PATTERNS**

- **Found during:** Task 2 (Writing async tests for JiraAdapter)
- **Issue:** The test `test_fetch_assigned_items_auth_failure` was failing because CLIAuthError wasn't being raised. The error message from acli was "Not authenticated" but AUTH_PATTERNS only included "authentication failed", "unauthorized", "401", and "not logged in".
- **Fix:** Added "not authenticated" to the AUTH_PATTERNS list in CLIAuthError class
- **Files modified:** `src/monocli/exceptions.py`
- **Verification:** All 8 Jira adapter tests now pass, including auth failure detection
- **Committed in:** `d55fe7c` (Task 2 commit)

**2. [Rule 3 - Blocking] Fixed test assertion for CLIAuthError message format**

- **Found during:** Task 2 (Writing async tests for JiraAdapter)
- **Issue:** The test was asserting `assert "Authentication failed" in str(exc_info.value)` but CLIAuthError uses the parent CLIError's string representation which includes the full command and stderr. The `.message` attribute contains the user-friendly text.
- **Fix:** Updated test to check `exc_info.value.message` for the friendly message and `str(exc_info.value).lower()` for auth-related text
- **Files modified:** `tests/test_jira_adapter.py`
- **Verification:** Test passes with correct assertions
- **Committed in:** `d55fe7c` (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking)
**Impact on plan:** Both auto-fixes necessary for correct auth error detection. No scope creep.

## Issues Encountered

None - plan executed with minor auto-fixes as documented above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- JiraAdapter ready for integration into dashboard UI
- Pattern established: lightweight auth check → fetch data → parse to Pydantic
- All three CLI adapters (GitLab, Jira) follow consistent pattern
- Detection mechanism (02-01) can be extended to include acli
- Ready for Phase 3: Dashboard UI with data table widgets

## Self-Check: PASSED

All files and commits verified:
- FOUND: src/monocli/adapters/jira.py
- FOUND: tests/test_jira_adapter.py
- FOUND: 4ac43fc (JiraAdapter implementation)
- FOUND: d55fe7c (async tests + exception fix)
- FOUND: c6c07c5 (export JiraAdapter)

---
*Phase: 02-cli-adapters*
*Completed: 2026-02-07*
