# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2025-02-07)

**Core value:** One dashboard showing all assigned work items and pending PRs/MRs without switching between browser tabs or context switching between platforms.
**Current focus:** Phase 2 - CLI Adapters

## Current Position

Phase: 3 of 3 (Dashboard UI)
Plan: 3 of 3 in current phase
Status: Phase complete
Last activity: 2026-02-08 — Completed 03-03-PLAN.md (Keyboard Navigation)

Progress: [█████████░] 100% (9 of 9 total plans)

## Performance Metrics

**Velocity:**
- Total plans completed: 9
- Average duration: 6.1 min
- Total execution time: 0.92 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Foundation | 3/3 | 12m 33s | 4m 11s |
| 2. CLI Adapters | 3/3 | 14m 0s | 4m 40s |
| 3. Dashboard UI | 3/3 | 22m 0s | 7m 20s |

**Recent Trend:**
- Last 5 plans: 03-01 (4m), 03-02 (3m), 03-03 (15m)
- Trend: Navigation plan took longer due to Textual API changes and test writing

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

**New from 02-03:**
- acli whoami for lightweight Jira auth checking
- acli jira issue list --json with --assignee and --status filters
- Bug fix: Add 'not authenticated' to CLIAuthError.AUTH_PATTERNS
- Jira API URL to browser URL transformation in model property

**New from 03-01:**
- Textual reactive properties for data binding in widgets
- SectionState enum for explicit UI state management (LOADING, EMPTY, ERROR, DATA)
- Base class pattern for shared section functionality
- DataTable with zebra_stripes for readability
- Row keys for storing item URLs (for browser integration)
- Title truncation with ellipsis (40 char limit)
- Pilot API with TestApp wrapper for widget testing

**New from 03-02:**
- Nested @work decorator pattern for fire-and-forget async workers
- DetectionRegistry with CLIDetector instances for CLI availability checking
- Reactive active_section property with CSS border highlight
- Fire-and-forget workers with `_ = worker_func()` to silence warnings
- MainScreen.compose() stores section references as instance attributes
- Error handling per section (CLI not found, not authenticated, network errors)

**New from 03-03:**
- Textual 7.x uses run_worker() instead of @work decorator (API change)
- Section widgets expose navigation API: focus_table(), select_next(), select_previous()
- Store URLs as DataTable row keys for efficient retrieval
- on_key() handler for custom keyboard shortcuts in MainScreen
- Visual indicators via CSS class toggling (.active class on containers)
- Error notifications using Textual's notify() method
- Section-scoped selection (each section maintains its own cursor position)

### Pending Todos

None yet.

### Blockers/Concerns

None yet.

## Session Continuity

Last session: 2026-02-08T10:44:54Z
Stopped at: Completed 03-03-PLAN.md (Phase 3 complete)
Resume file: None

## Next Phase

**PROJECT V1 COMPLETE** - All 9 plans finished

Dashboard UI phase complete with:
- ✅ Two-section layout (MRs top, Work Items bottom)
- ✅ Keyboard navigation (Tab, j/k, arrows)
- ✅ Browser integration ('o' key)
- ✅ Visual indicators for active section
- ✅ Loading, empty, and error states
- ✅ Async data fetching without blocking
- ✅ 12 navigation integration tests

**Ready for:**
- End-to-end testing
- Documentation
- Packaging and distribution
- v2 feature planning (GitHub support, refresh, search)
