# Payment Reliability Copilot · AI Engineering Curriculum

A local, simulator-first learning app for the 16-week AI Engineering curriculum. It includes the complete reading list, build assignment, deliberate failure pass, deliverables, exit criteria, week/month navigation, and a browser-persisted progress tracker.

## Run locally

From this folder, start any static web server. Python is already enough:

```bash
python3 -m http.server 4173
```

Then open [http://localhost:4173](http://localhost:4173).

You can also open `index.html` directly, but a local server is recommended so external resource links behave consistently.

## Use the app

- Pick a week from the course map or month rail.
- Start with the weekly prerequisite and focused build brief. Expand the suggested 8–10-hour session rhythm when planning your time.
- Read the focus sections of core resources. Optional depth is tracked but does not gate completion.
- Use **Continue learning** to focus the actual next unfinished checkpoint, including unfinished earlier weeks.
- Mark the assignment complete after the build and failure pass.
- In updated weeks, complete **Extend this build**, **Experiments & comparisons**, and the appended deliverable/exit checkpoints too. Older assignment checks remain intact; the appended requirements capture new work.
- Check off deliverables and exit criteria as you earn them.
- Overall and per-week progress update immediately and persist in `localStorage`.
- Write a week-specific note with your evidence and next action; notes save as you type.
- Use **Export backup** to download progress and notes. **Restore backup** validates the file and asks before replacing this browser's data. Back up first: restore replaces, it does not merge.
- Use **Reset progress** to clear checklists and notes after confirmation.

Existing v1 checkpoint keys are retained. Progress includes all current required readings, the assignment, deliverables and exit criteria. Recommended and optional reading checks are saved but do not gate completion. New checkpoints are appended, so a previously complete week may reopen and the overall percentage may decrease without losing any completions. Browser storage is specific to the browser and origin: keep using `http://localhost:4173/`, not a mixture of localhost and 127.0.0.1. Multiple devices are not automatically synced. Do not edit concurrently in multiple tabs; export before switching browsers or clearing browser data.

## Files and verification

The app has no runtime dependencies or build step. Serve this whole folder, including `progress.js`, `study.js`, `curriculum-updates.js`, `study.css`, and `styles/` alongside the original HTML and JavaScript. No API key is needed to use the tracker. All AI-system implementations described in the syllabus are learner assignments, not services running inside the tracker.

Run the regression tests with Node.js:

```bash
node --test tests/progress.test.cjs
```

Read [CURRICULUM.md](CURRICULUM.md) for the consolidated learner-facing syllabus. `CURRICULUM-UPDATE-20260911.md` records the additive changes and verification, while `CURRICULUM-REVIEW.md` records the earlier review. The frozen test fixture captures the actual pre-update syllabus and protects every legacy resource and checkpoint from accidental renumbering.
Use [LEARNING-ASSISTANT-PROMPT.md](LEARNING-ASSISTANT-PROMPT.md) as a reusable prompt for a coaching assistant that walks through the course without resetting progress.
