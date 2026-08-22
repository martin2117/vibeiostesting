# Section 10 — Writing the Test Suite in XCUITest

> 📖 **Guide:** [XCUITest suite](../docs/s10-xcuitest.md) · builds into `xcuitest/`

You build the native XCUITest suite (Swift) from the same **test matrix** (`test-cases.md`)
and the **test-authoring skill**. XCUITest has the deepest access to the accessibility tree
and is the fastest to execute — the trade-off is that it is iOS-only. You run and triage the
suite in Section 12.

## Course reference
| Prompt | Used in clip |
|--------|-------------|
| Prompt 1 — Base test case + login tests | **10, Clip 2** |
| Prompt 2 — Cart & catalog tests | **10, Clip 3** |
| Prompt 3 — Checkout tests | **10, Clip 3** |
| Prompt 4 — The React Native reality | **10, Clip 4** |

> Setup: add a **UI Testing Bundle** target named `TechShopUITests` to the TechShop app in
> Xcode (or use `xcuitest/project.yml` with XcodeGen), and set its Target Application to
> TechShop. See [../docs/s10-xcuitest.md](../docs/s10-xcuitest.md).

---

## Prompt 1: Base test case + login tests
*Used in: Section 10, Clip 2*

```
First make sure the BROKEN build is installed on the Simulator — com.techshop.ios from
techshop/reactnative-broken or techshop/swiftui-broken (the version with the planted bugs),
not the fixed build.

Then, following skills/test-authoring.md, create the XCUITest base under
xcuitest/TechShopUITests/:

- TechShopUITestCase.swift — base XCTestCase that launches
  XCUIApplication(bundleIdentifier: "com.techshop.ios"), reads TEST_EMAIL/TEST_PASSWORD
  from ProcessInfo, and provides framework-agnostic helpers: el(id) via
  descendants(matching:.any), hasText, a passwordField() that returns the secure OR plain
  field, login(), and addItemAndOpenCart(). Locate the login button by the label "Log In".

Then, from the LOGIN cases in test-cases.md, create LoginUITests.swift — one test per login
case in the matrix, no more and no less. Include the secure-entry and login-button-identifier
cases the matrix assigns to native/attribute-aware frameworks (use app.secureTextFields to
prove masking). Read the matrix for what each case asserts.

List the tests you created and the test-case ID each covers.
```

**Expected:** the base plus one login test per matrix case. Run with
`xcodebuild test -scheme TechShop -destination 'platform=iOS Simulator,name=iPhone 16'`
(with TEST_EMAIL/TEST_PASSWORD exported).

---

## Prompt 2: Cart & catalog tests
*Used in: Section 10, Clip 3*

```
Following the skill and the CART and CATALOG cases in test-cases.md, add CartUITests.swift
and GeneralUITests.swift using the base helpers — one test per matrix case. Read the matrix
for what each case asserts (e.g. el("qty-p1").label, a total label, a discounted total).

List the tests you created and the test-case ID each covers.
```

---

## Prompt 3: Checkout tests
*Used in: Section 10, Clip 3*

```
Following the skill and the CHECKOUT cases in test-cases.md, add CheckoutUITests.swift —
one test per matrix case. The matrix marks the cases blocked by the unresponsive "Proceed
to Checkout" button (verify only on the fixed build); comment which run on the fixed build
only and why.

List the tests you created and the test-case ID each covers.
```

---

## Prompt 4: The React Native reality
*Used in: Section 10, Clip 4*

```
Run the XCUITest suite against the SwiftUI build, then against the React Native build
(same bundle id). Report where the accessibility tree differs (element types/hierarchy)
and whether the framework-agnostic el(id) helper absorbed the difference. Explain why a
team on a React Native app might still prefer Maestro or Appium over XCUITest.
```

**Expected:** the suite runs on both, and you can now articulate — for Section 11 — when
native XCUITest is worth its iOS-only constraint and when it isn't.
