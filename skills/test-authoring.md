# Skill: Mobile Test Authoring

## Purpose
Follow these instructions whenever asked to turn test cases or test matrices into executable mobile automation tests. This skill defines the universal quality standards and framework-specific patterns for **Maestro**, **Appium (Python/pytest)**, and **XCUITest (Swift)**.

---

## Universal Rules (All Frameworks)

1. **Locators**:
   - Prefer stable accessibility identifiers (`accessibilityIdentifier` in SwiftUI / `testID` in React Native).
   - Use visible text **only** when no identifier exists. If a key interactive control lacks an identifier, flag it and recommend adding one.
   - **Never** locate elements by screen coordinates, relative positions, or array indices.
2. **Assertions**:
   - Every test must assert a concrete business outcome (value, state, element visibility, element type).
   - Never write shallow assertions that only check "the app didn't crash".
3. **Isolation**:
   - Each test must launch the app fresh with clean state.
   - Tests must be completely independent and capable of running in any sequence.
4. **Secrets & Credentials**:
   - Never hardcode credentials in test files.
   - Read test credentials from environment variables (`TEST_EMAIL` and `TEST_PASSWORD`).
5. **No Manual Sleeps**:
   - Never use fixed sleeps (`sleep()`, `time.sleep()`).
   - Use each framework's explicit wait/polling mechanism.
6. **Reuse**:
   - Encapsulate repeated setup workflows (e.g., login, adding items to cart) in subflows, flow helpers, or base test classes. Do not copy-paste setup steps.
7. **Cross-Build Compatibility**:
   - Tests must run interchangeably against native SwiftUI and React Native builds (bundle id: `com.techshop.ios`).
   - Exception: The login submit button lacks an accessibility identifier in the broken build, so it must be located by visible text `"Log In"`.
8. **Honesty Rule**:
   - Maestro cannot inspect hidden element attributes (e.g., `secureTextEntry` masking, exact UI colors).
   - Defer those specific assertions to Appium or XCUITest rather than writing a weak or deceptive assertion.

---

## Framework Standards & Best Practices

### 1. Maestro (YAML Flows)

- **Structure**:
  - Store standalone test flows under `maestro/flows/<feature>-<scenario>.yaml`.
  - Store reusable steps (e.g., `login.yaml`, `add-to-cart.yaml`) under `maestro/subflows/` and invoke them with `runFlow`.
- **App ID & Isolation**:
  - Set `appId: com.techshop.ios` at the top of every main flow.
  - Launch with `launchApp: { clearState: true }` at the start of each test.
- **Locators & Assertions**:
  - Locate with `id: <accessibility-id>` or visible text: `tapOn: "Log In"`.
  - Assert visibility with `assertVisible` or `assertNotVisible`.
  - Assert dynamic values using regex (e.g., `assertVisible: ".*120.*"` for cart totals).
- **Credentials**:
  - Reference parameters via `${EMAIL}` and `${PASSWORD}`.
  - Pass at CLI runtime: `maestro test maestro/flows/ -e EMAIL="$TEST_EMAIL" -e PASSWORD="$TEST_PASSWORD"`.
- **Waits & Flow Control**:
  - Prefer `extendedWaitUntil: { visible: <target> }` for asynchronous transitions.
  - Keep YAML declarative without complex inline scripting. Defer attribute-level checks to Appium/XCUITest.

---

### 2. Appium (Python + pytest + Page Object Model)

- **Structure**:
  - `appium/conftest.py`: Driver fixture configuring `automationName: "XCUITest"`, `bundleId: "com.techshop.ios"`, fresh launch per test, and reading env vars.
  - `appium/pytest.ini`: pytest configuration and test discovery settings.
  - `appium/pages/`: One Page Object class per screen (`LoginPage`, `CatalogPage`, `CartPage`, `CheckoutPage`). Keep page objects thin (locators and UI actions only; no test assertions).
  - `appium/flows.py`: High-level business flows combining page actions (e.g., `login_as_standard_user()`, `add_first_item_and_view_cart()`).
  - `appium/tests/`: Test files (`test_login.py`, `test_cart.py`, etc.) where assertions reside.
- **Locators & Attributes**:
  - Locate primarily with `AppiumBy.ACCESSIBILITY_ID`.
  - Use `-ios predicate string` for visible text lookups (e.g., `label == "Log In"`).
  - Read element attributes when required: verify `element.get_attribute("type") == "XCUIElementTypeSecureTextField"` to validate password masking (BUG-001).
- **Waits**:
  - Use `WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(...))`.
  - Never use `time.sleep()`.

---

### 3. XCUITest (Swift + Xcode)

- **Structure**:
  - Base class `TechShopUITestCase` (subclass of `XCTestCase`) inside `xcuitest/TechShopUITests/`:
    - Launches `XCUIApplication(bundleIdentifier: "com.techshop.ios")`.
    - Reads credentials from `ProcessInfo.processInfo.environment["TEST_EMAIL"]` and `["TEST_PASSWORD"]`.
    - Provides a type-agnostic element helper: `el(_ id: String) -> XCUIElement` via `app.descendants(matching: .any)[id]`.
    - Holds shared helper functions: `login()`, `addItemAndOpenCart()`.
  - Feature test classes (`LoginUITests.swift`, `CartUITests.swift`, `CheckoutUITests.swift`) inheriting from `TechShopUITestCase`.
- **Locators & Masking Assertions**:
  - Use `el("identifier")` to survive type differences between SwiftUI and React Native.
  - Verify password masking by asserting `app.secureTextFields["login-password"].exists` vs `app.textFields["login-password"].exists` (BUG-001).
- **Waits & Code Cleanup**:
  - Use `XCTAssertTrue(element.waitForExistence(timeout: 5.0))` for UI synchronization. Never call `Thread.sleep()`.
  - Treat the Xcode Test Recorder as a rough scratchpad: immediately refactor any recorded coordinate- or index-based locators into identifier-based lookups.

---

## Authoring Self-Check
Before delivering authored test code, verify:
- [ ] Are locators using accessibility identifiers (or text `"Log In"` where ID is missing)?
- [ ] Are all credentials sourced from environment variables?
- [ ] Are tests isolated with fresh app launches?
- [ ] Are shared setups extracted into reusable subflows/helpers?
- [ ] Are explicit waits used instead of arbitrary sleeps?
- [ ] Are assertions verifying real outcomes, and are framework attribute limitations honestly respected?
