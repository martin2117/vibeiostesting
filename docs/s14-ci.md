# S14 — Shipping to CI

Companion to Section 14. Builds into `.github/workflows/`. Prompts:
[`prompts/section-14-ci.md`](../prompts/section-14-ci.md).

## The mobile CI model (one skeleton, three workflows)
Every workflow is a variation on:
1. **macOS runner** (mandatory — iOS needs Xcode/Simulator).
2. **Boot an iPhone Simulator** headless (`xcrun simctl`).
3. **Build & install** the app.
4. **Install the framework** and **run the suite**, reading `TEST_EMAIL` / `TEST_PASSWORD`
   from **repository secrets**.
5. **Upload artifacts** (recording / screenshots / `.xcresult`).

## The three workflows
- `maestro.yml` — install Maestro, `maestro test`, upload the report.
- `appium.yml` — start Appium, `pip install`, `pytest`, upload results.
- `xcuitest.yml` — `xcodebuild test` on a Simulator destination, upload the `.xcresult`.

## Secrets — set these up FIRST
Do this **before** writing any workflow, or every first run fails on a missing credential.
Add `TEST_EMAIL` and `TEST_PASSWORD` as **repository secrets** — either in the UI (Settings →
Secrets and variables → Actions) or, faster, with the agent via the GitHub CLI — set to the
**actual** values (source `.env-local` first, then pass each explicitly):
`gh secret set TEST_EMAIL --body "$TEST_EMAIL"` / `gh secret set TEST_PASSWORD --body
"$TEST_PASSWORD"`, then `gh secret list` to confirm they exist and are non-empty. They never appear in code — your skills enforced env-var
credentials from the first test, so this is trivial now.

## Debugging CI failures
Most early failures are infrastructure, not tests: Simulator didn't boot, app didn't install,
wrong destination, missing secret. The push prompts (4 & 6) fold this in: after pushing, the
agent **monitors** the run (`gh run watch`) and, on red, diagnoses from the logs, **fixes**
the workflow or test directly, and pushes again — looping until green, not just describing the
fix. CI logs are long and noisy, and the agent parses them fast, iteration after iteration.

## Career note
Maestro and Appium workflows are cross-platform: point the same skeleton at an Android
emulator and they run on Android. You're learning the mobile CI pattern, not just iOS CI.
