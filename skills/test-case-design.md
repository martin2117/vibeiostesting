# Skill: Mobile Test-Case Design

## Purpose
Follow these instructions whenever asked to design mobile test cases or produce a test matrix for a feature (`Login`, `Catalog`, `Cart`, or `Checkout`). The goal is to generate a comprehensive, grounded test matrix ready for automated test authoring across Maestro, Appium, and XCUITest.

---

## Required Inputs
Always read and ground test cases in:
1. **Requirements Spec**: `techshop/requirements.md` (expected business logic, validation rules, constraints).
2. **Exploration Notes**: `exploration-notes.md` (real UI hierarchy, screen flows, observed element identifiers, quirks).
3. **Known Bugs List**: `techshop/BUGS.md` (known issues and regression IDs).

> **Rule:** Never invent generic test cases or speculative UI elements. Every step, locator, and assertion must reflect the actual application under test.

---

## 1. Required Test Categories
Every feature test matrix **must** include test cases across all three categories:

1. **Positive (Happy Path)**
   - Valid inputs, standard workflows, successful completions, and state transitions.
2. **Negative (Validation & Error Handling)**
   - Invalid input rejection, empty required fields, incorrect formats, unauthorized access, and inline/modal error messages.
3. **Edge (Boundaries & Device Quirks)**
   - Min/max boundary values (e.g., quantity 1 → 0, minimum order amount thresholds, card/CVV digit lengths).
   - Mobile-specific boundary conditions: keyboard covering inputs, truncation of long labels, rapid multi-taps, session interruptions.

---

## 2. Test Case Specification Standard
Every test case in the matrix must specify the following fields:

- **ID**: Feature-based identifier (e.g., `TC-LOG-001`, `TC-CAT-001`, `TC-CART-001`, `TC-CHK-001`).
- **Behavioural Title**: Concise, active description of the behavior being verified (e.g., `Reject login when email format lacks domain`).
- **Category**: `Positive` | `Negative` | `Edge`.
- **Preconditions**: Exact starting state (e.g., `App launched fresh, on Login screen`, `Cart contains 1 item`).
- **Steps**: Step-by-step numbered user actions using exact control names.
- **Expected Result**: Concrete, assertable outcome (UI visibility, text, navigation, state change).
- **Locator(s)**: Target element locators (`accessibilityIdentifier`, `testID`, or visible text).
- **Tags / Defects**:
  - **Testability Defect**: Flag controls lacking a stable ID (e.g., `[DEFECT: No accessibilityIdentifier]`).
  - **Regression Tag**: Flag known bugs as regression cases with their ID (e.g., `[Regression: BUG-001]`). Test cases must assert the *correct/intended* behavior so they fail on broken builds and pass on fixed builds.
  - **Blocked By**: Flag test cases blocked by existing bugs (e.g., `[Blocked by: BUG-011]`).
  - **Framework Owner**: Flag assertions only testable by specific frameworks (e.g., `[Appium/XCUITest only: secureTextEntry masked attribute]`).

---

## 3. Output Matrix Format
When designing test cases, output a markdown table following this exact structure:

| ID | Behavioural Title | Category | Preconditions | Steps | Expected Result | Locators | Notes / Tags |
|---|---|---|---|---|---|---|---|
| `TC-<FEAT>-001` | *Active title* | `Positive` / `Negative` / `Edge` | *Starting state* | 1. ...<br>2. ... | *Assertable result* | `id: <accessibility-id>` or `text: "<label>"` | `[Regression: BUG-xxx]` / `[DEFECT: No ID]` / `[Blocked by: BUG-xxx]` |

---

## 4. Agent Execution Rules
1. **Consult Source Files First**: Open and read `techshop/requirements.md` and `exploration-notes.md` before generating cases.
2. **Balance Categories**: Never deliver a positive-only suite. Actively probe validation errors and boundary limits.
3. **Be Specific with Locators**: Use exact accessibility identifiers where available from exploration notes. If only text exists, specify `text: "..."` and flag the missing ID.
4. **Assert Expected, Not Buggy Behavior**: For known bug areas, write the expected result according to requirements, not the broken app behavior, and tag with `[Regression: BUG-xxx]`.
5. **Self-Check Before Output**:
   - [ ] Are all 3 categories (Positive, Negative, Edge) represented?
   - [ ] Is every case grounded in actual app screens and requirements?
   - [ ] Are locators defined for all interaction points and assertions?
   - [ ] Are missing accessibility IDs flagged as testability defects?
   - [ ] Are known bugs tagged with `BUG-xxx` and blocked cases marked?
