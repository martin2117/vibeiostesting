# Skill: Mobile Bug Reporting

## Purpose
Follow these instructions whenever asked to convert a failing mobile automated test, manual observation, or test execution artifact into a developer-ready, reproducible bug report.

---

## Standard Bug Report Format

Every bug report must strictly adhere to the following markdown template:

```markdown
# [BUG-ID]: <Specific Behavioural Title>

**Severity:** <Critical | High | Medium | Low> — <One-line reason for severity rating>
**Framework:** <Maestro | Appium | XCUITest | Manual>
**Element Identifier:** `<accessibility-id>` (or `None — [DEFECT: Missing accessibility identifier]`)
**Cross-Build Status:** <Reproduces on both SwiftUI & React Native | SwiftUI only | React Native only>
**Blocks Other Tests:** <Yes — details of blocked tests/features | No>

### Environment
- **Build Type:** <SwiftUI | React Native>
- **Build Variant:** <Broken | Fixed>
- **iOS Version:** <e.g., iOS 18.2>
- **Simulator / Device:** <e.g., iPhone 16 Simulator>
- **Framework & Runner:** <e.g., Maestro v1.39 / pytest 8.x / Xcode 16 xcodebuild>

### Steps to Reproduce
1. Launch the app fresh on a clean simulator.
2. <Action with exact control name and input value>
3. <Action with exact control name and input value>
4. <Final trigger action>

### Expected Result
<Clear, specific statement of expected app behaviour, state transition, or UI display according to requirements.>

### Actual Result
<Precise description of what actually happened, including observed error, stuck state, incorrect value, or visual defect.>

### Evidence & Artifacts
- **Artifact Type:** <Maestro recording | Appium screenshot | Xcode .xcresult bundle>
- **Artifact Path / Reference:** `<path/to/artifact.png|.mp4|.xcresult>`
- **Error Log / Trace:** `<Relevant failure snippet or stack trace if applicable>`
```

---

## Reporting Rules & Requirements

1. **Specific Behavioural Title**:
   - Describe the exact failure behavior (e.g., `Password field renders plaintext characters instead of secure masked text`).
   - Avoid vague summaries like `Login broken` or `Test failed`.
2. **Strictly Separate Expected and Actual**:
   - `Expected Result` defines the correct specification requirement.
   - `Actual Result` defines the observed failure.
   - Never combine them into a single narrative.
3. **Reproducible Cold Steps**:
   - Number every step starting from initial app launch.
   - Use explicit values (credentials, quantities, card numbers) instead of generic placeholders.
   - Ensure the steps require no prior app state or unstated preconditions.
4. **Locators & Element Testability**:
   - Always state the target element's accessibility identifier.
   - If the element lacks an identifier, explicitly highlight this testability defect.
5. **Cross-Build & Blocker Context**:
   - Note whether the failure occurs in both SwiftUI and React Native builds or is isolated to one platform stack.
   - Explicitly note if this defect acts as a test blocker for downstream scenarios (e.g., a broken proceed button blocking checkout assertions).
6. **Objective Severity Rating**:
   - **Critical**: App crashes, data corruption, or complete block on core revenue/auth paths with no workaround.
   - **High**: Major functional requirement broken or security/privacy issue (e.g., plaintext password).
   - **Medium**: Non-blocking functional defect, calculation glitch, or validation inaccuracy with a workaround.
   - **Low**: Minor cosmetic defect, label truncation, or missing accessibility identifier without functional failure.

---

## Mandatory Self-Check
Before finalizing any bug report, answer this question:

> **"Could a developer reproduce this from the steps alone on a clean Simulator?"**
>
> If the answer is **NO** (steps are missing, data is ambiguous, or preconditions are omitted), the report is **NOT DONE**. Refine the steps until reproduction is guaranteed.
