---
status: resolved
trigger: "Investigate why the Merge Requests section spinner spins forever without resolving"
created: 2026-02-08T00:00:00Z
updated: 2026-02-08T00:00:00Z
---

## Current Focus

hypothesis: The code uses @work decorator which was removed in Textual 7.x
test: Examine pyproject.toml for Textual version and main_screen.py for worker API
expecting: Version >= 7.x with @work decorator usage
next_action: Provide structured diagnosis

## Symptoms

expected: MR section should load data and show results after fetching
actual: MR section shows loading spinner that never resolves
errors: None visible (silent failure of workers)
reproduction: Run uv run monocli and observe MR section spinner
started: After Textual 7.x upgrade

## Eliminated

## Evidence

- timestamp: 2026-02-08
  checked: pyproject.toml
  found: "textual>=7.5.0" dependency (Textual 7.x)
  implication: Project is using Textual 7.x which removed @work decorator

- timestamp: 2026-02-08
  checked: src/monocli/ui/main_screen.py lines 16, 130, 162
  found: "from textual import work" and "@work(exclusive=True)" used on both fetch methods
  implication: Using deprecated/removed decorator API that won't work in Textual 7.x

- timestamp: 2026-02-08
  checked: sections.py loading state logic
  found: Loading state shows spinner, transitions to DATA state only via update_data()
  implication: Workers not starting means update_data() never called, spinner stays forever

## Resolution

root_cause: The @work decorator was removed in Textual 7.x and replaced with run_worker() method
fix: Convert @work(exclusive=True) decorator to self.run_worker(coro, exclusive=True) calls
verification: Workers will start, fetch data, update sections, and spinner will resolve
files_changed: [src/monocli/ui/main_screen.py]
