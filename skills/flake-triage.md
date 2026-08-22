# Skill: Mobile Flake Triage

## Purpose
Follow these instructions whenever a mobile automated test fails to determine whether the failure represents a **REAL BUG** in the application or a **FLAKY TEST** caused by mobile synchronization, environment, or test design issues.

---

## 5-Step Triage Workflow

Whenever analyzing a test failure, work through these five steps in order:

### 1. Consistency Check
- Determine if the test fails deterministically (100% on every run) or intermittently (only in CI, under load, or on specific runs).
- **Rule:** If consistency is unclear from a single run, **require a re-run** (at least 2–3 consecutive executions) before making a final determination.

### 2. Root Cause Analysis
- Isolate whether the failure is caused by:
  - **App Defect**: The application logic, UI state, or validation violates the functional specification.
  - **Mobile Noise**: The test tripped over timing, race conditions, keyboard interactions, animation delays, or fragile locators.

### 3. Artifact & Evidence Review
- Inspect the test artifact (Maestro screen recording, Appium failure screenshot, or Xcode `.xcresult` timeline).
- Verify:
  - Was the app genuinely broken or in an error state in the captured frame?
  - Or did the test capture a screenshot while an animation/screen transition was still in progress?
  - Was an interactive control obscured by the software keyboard?

### 4. Classification
Classify the failure into one of two categories:
- **`REAL BUG`**: The application behaves incorrectly under valid test conditions.
- **`FLAKY TEST`**: The application functions correctly, but the test automation failed due to synchronization, timing, or locator fragility.

### 5. Actionable Recommendation
- **If `REAL BUG`**:
  - Do **not** modify the test to work around the defect.
  - Invoke `skills/bug-reporting.md` to produce a developer-ready bug report.
- **If `FLAKY TEST`**:
  - Do **not** file a bug report against the application.
  - Apply the specific test fix (see Common Mobile Flake Sources below) and re-verify.

---

## Common Mobile Flake Sources & Fixes

| Flake Source | Root Cause | Required Fix |
|---|---|---|
| **Premature Tap / Race Condition** | Tapped an element before the screen finished rendering. | Replace with explicit wait for destination element visibility before tapping. |
| **Active Screen Animation** | Screen transition/slide in-flight during assertion. | Wait for transition to complete (`extendedWaitUntil`, `WebDriverWait`). |
| **Keyboard Obscuring Controls** | Software keyboard blocks tap target or footer action. | Tap outside/return key to dismiss keyboard, or scroll element into view. |
| **State Leakage Across Tests** | Residual data or auth state left from a prior test. | Enforce clean launch isolation (`clearState: true`, fresh driver session). |
| **Fragile / Positional Locators** | Locating by coordinate, bounding box, or index. | Replace with stable `accessibilityIdentifier` / `testID`. |
| **Arbitrary Sleeps** | Fixed `sleep()` elapsed before async network/UI completed. | Replace arbitrary sleeps with dynamic polling waits (`waitForExistence`). |

---

## Triage Output Format

When reporting triage findings to the user, format the output as follows:

```markdown
### Flake Triage: <Test Name / ID>

- **Classification:** <REAL BUG | FLAKY TEST>
- **Consistency:** <Deterministic (3/3 runs) | Intermittent (1/3 runs) | Needs Re-run>
- **Failure Symptom:** <Short description of assertion failure or timeout>
- **Evidence Review:** <Observations from recording, screenshot, or .xcresult>
- **Root Cause:** <Application defect OR specific mobile flake factor>
- **Action / Next Step:**
  - *If REAL BUG:* Proceed to bug report via `skills/bug-reporting.md`.
  - *If FLAKY TEST:* <Specific fix: e.g., Add `extendedWaitUntil` on product list before tap>.
```
