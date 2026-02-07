# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2025-02-07)

**Core value:** One dashboard showing all assigned work items and pending PRs/MRs without switching between browser tabs or context switching between platforms.
**Current focus:** Phase 2 - CLI Adapters

## Current Position

Phase: 2 of 3 (CLI Adapters)
Plan: 2 of 3 in current phase
Status: In progress
Last activity: 2026-02-07 — Completed 02-02-PLAN.md (GitLab Adapter)

Progress: [█████░░░░░] 55% (5 of 9 total plans)

## Performance Metrics

**Velocity:**
- Total plans completed: 5
- Average duration: 4.4 min
- Total execution time: 0.37 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Foundation | 3/3 | 12m 33s | 4m 11s |
| 2. CLI Adapters | 2/3 | 11m 0s | 5m 30s |

**Recent Trend:**
- Last 5 plans: 01-03 (6m 0s), 02-01 (8m 0s), 02-02 (3m 0s)
- Trend: 02-02 was faster due to established patterns from 02-01

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Initialization: Use Textual framework for TUI (modern async support)
- Initialization: Shell out to existing CLIs vs APIs (reuse existing auth)
- Initialization: UV for dependency management, Ruff for linting, MyPy for type checking

**New from 01-01:**
- Use src/ layout for better package isolation and testing
- Configure Ruff with comprehensive lint rules (E, F, I, N, W, UP, B, C4, SIM)
- Enable strict MyPy type checking for early error detection
- Use pytest-asyncio for testing async code in future phases

**New from 01-02:**
- Use BeforeValidator for datetime parsing from ISO 8601 JSON strings
- Standardize helper interface: display_key(), display_status(), is_open() on all models
- Pattern validation with regex for Jira keys (PROJECT-123 format)
- Strict mode with ConfigDict for early type error detection

**New from 01-03:**
- Use asyncio.create_subprocess_exec over subprocess.run for true async execution
- Implement @work(exclusive=True) pattern to prevent data fetching race conditions
- Create CLIAdapter base class for consistent CLI interface across platforms
- Use TypeVar for generic model parsing in fetch_and_parse()
- Cache CLI availability check in adapter to avoid repeated which() calls

**New from 02-01:**
- Use TypedDict for DetectionResult to provide clear field names and type safety
- Cache detection results at registry level after first detect_all() call
- Use lightweight auth check commands (e.g., "auth status") rather than data fetching
- Return copies of cached results to prevent external mutation
- Clear cache when new detector registered to ensure freshness
- Registry pattern: register detectors, detect_all returns all results, query methods filter

**New from 02-02:**
- CLI Adapter pattern: Inherit from CLIAdapter, implement fetch_* and check_auth methods
- glab mr list --json with --author and --state filters for targeted fetching
- check_auth() returns boolean (not exception) for detection flow compatibility
- Mock asyncio.create_subprocess_exec for async CLI testing

### Pending Todos

None yet.

### Blockers/Concerns

None yet.

## Session Continuity

Last session: 2026-02-07T19:51:21Z
Stopped at: Completed 02-02-PLAN.md
Resume file: None

## Next Phase

Phase 2: CLI Adapters - In Progress
- ✓ 02-01: CLI Detection Mechanism complete
- ✓ 02-02: GitLab Adapter complete
- Next: 02-03: Jira acli adapter with work item fetching
