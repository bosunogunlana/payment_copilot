# Curriculum and study-flow review — 9 September 2026

Historical review. The additive requirements in `CURRICULUM-UPDATE-20260911.md` supersede optionality and workload guidance here where they differ (especially hybrid retrieval/reranking, routing, cache experiments and the final flywheel/fallback slice).

## Retained

All 16 weeks, monthly sequence, existing resource links, assignments, deliverables and saved checkpoint identifiers. The project remains simulator-first, with Python for the copilot and Go for MCP. Paqet integration is not a prerequisite.

The source is the AI Curriculum Checkpoint conversation and the seeded syllabus in this app. The conversation reader limits long messages, so this review does not claim a verbatim audit of every word of the original long syllabus. New weekly guidance is an explicit editorial supplement in `study.js`.

## Adjustments and why

- Every week now has prerequisites, a focused build brief and optional extensions. A suggested 8-hour core rhythm plus up to 2 hours for catch-up avoids treating linked courses as cover-to-cover assignments. These are planning budgets, not promises of completion time.
- Core vs optional resource labels keep duplicate/reference readings from blocking progress. No existing resource checkpoints were reordered or deleted.
- Weeks 1–2 now distinguish successful schema-valid outputs from refusals/incomplete outputs, and application rejection of invalid tool calls from expecting a model never to emit one.
- Week 3 separates related synthetic templates across dataset splits, uses equal held-out comparisons and warns that synthetic accuracy is not production evidence. See [scikit-learn grouped splits](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).
- Weeks 4 and 13 build cumulatively on earlier eval datasets. Reproducibility means versioned inputs/settings, not identical model outputs. The 300-case target is cumulative, with 500 as stretch.
- Weeks 5–7 prioritize exact search, controlled RAG experiments and separate retrieval/generation failures. Recall@5 ≥0.85, citation precision ≥0.90 and unsupported answers ≤0.10 are learning targets with denominators and error analysis, not production certification.
- Security starts with application authorization in Week 2, tenant tests in Week 8 and bounded/approved actions in Weeks 9–11. Week 15 audits those controls. Live financial actions are never required for exercises.
- Week 12 starts with local stdio and the [official Go SDK](https://github.com/modelcontextprotocol/go-sdk). Resource/tool links point to the [2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools). SDK/protocol compatibility should be pinned together. [MCP security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) replaces the old location.
- Week 16 defines a reproducible simulator demo as the learning finish; production rollout remains a separate operational/security milestone.

## App changes

Continue learning selects a real missing checkpoint and wraps to earlier unfinished weeks. It is available above the reading list and in the side rail. Notes are per-week and autosaved. Core progress uses decimal percentages instead of hiding the first completed checkpoint at 0%. The fake checkpoint-derived hours-remaining estimate is removed. Month navigation uses native buttons. Checkbox focus is restored after progress updates.

Backups contain checklists, active week and notes. Restore validates shape/size and asks before replacement; failed storage writes do not claim success. Corrupt stored data is not automatically erased. Existing origin-local progress is preserved, but there is no cloud sync or concurrent-tab conflict resolution.

## Review and verification

Direct source review plus 12 dependency-free Node regression tests: 16-week content completeness, legacy migration, optional-progress math, next-action gaps/wraparound, fully complete state, fractional progress, backup validation, corrupted storage, quota failures, note persistence and invalid week fallback.

Browser check on the actual localhost app confirmed updated curriculum rendering, Continue learning focus, a checked item surviving reload, and correct 0.5% progress for the first checkpoint. The temporary test check was reopened afterward.

The learning note also survived a browser reload and was cleared afterward. At a 390px viewport, document width and scroll width both measured 390px (no horizontal overflow); the temporary viewport override was reset. Browser error logs were empty. Backup validation is covered by automated tests; file-picker export/restore was not tested end-to-end in the browser.

The design-system skill guided the new prefixed study controls and token reuse; original page styling remains intact, split behind an imports-only stylesheet. Code review: skipped (ce-code-review unavailable) — its required Git base cannot be resolved because this folder is not a repository; direct source review and tests were used instead. No deployment or live payment integration was performed.
