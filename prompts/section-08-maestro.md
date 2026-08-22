# Section 8 — Writing the Test Suite in Maestro

> 📖 **Guide:** [Maestro flows](../docs/s08-maestro.md) · builds into `maestro/`

You build the Maestro flow suite yourself, feature by feature, from the **test matrix**
(`test-cases.md`, Section 7) using the **test-authoring skill** (Section 5). Point the
Simulator at the **broken** build. You *run and triage* the whole suite in Section 12 —
here you just author it.

## Course reference
| Prompt | Used in clip |
|--------|-------------|
| Prompt 1 — Login flows + reusable subflow | **8, Clip 2** |
| Prompt 2 — Cart & catalog flows | **8, Clip 3** |
| Prompt 3 — Checkout flows | **8, Clip 3** |
| Prompt 4 — One flow, two apps | **8, Clip 4** |

---

## Prompt 1: Login flows + reusable subflow
*Used in: Section 8, Clip 2*

```
First make sure the BROKEN build is installed on the Simulator — com.techshop.ios from
techshop/reactnative-broken or techshop/swiftui-broken (the version with the planted bugs),
not the fixed build.

Then, following skills/test-authoring.md and the LOGIN cases in test-cases.md, build the
Maestro login flows for TechShop iOS (appId com.techshop.ios). Read the matrix to decide
which flows to write and what each one asserts — cover exactly the login cases I designed,
no more and no less. Put a reusable valid login in maestro/subflows/login.yaml and one
flow per case under maestro/flows/.

Then list the flows you created and the test-case ID each one covers.
```

**Expected:** a login subflow plus one flow per login case in the matrix. Run the folder:
`maestro test maestro/flows/ -e EMAIL=$TEST_EMAIL -e PASSWORD=$TEST_PASSWORD`.

---

## Prompt 2: Cart & catalog flows
*Used in: Section 8, Clip 3*

```
Following skills/test-authoring.md and reusing subflows/login.yaml, build the CART and
CATALOG flows from test-cases.md — one flow per matrix case, under maestro/flows/. Read the
matrix for what each case asserts; use id: locators for the stepper/total/discount and
assertVisible with a text regex for values.

If the matrix contains a case Maestro cannot assert (it can't read a secure-entry attribute
or a colour), say so and skip it here — note that it belongs to Appium/XCUITest.

List the flows you created and the test-case ID each covers.
```

**Expected:** one flow per cart/catalog case in the matrix. Maestro can't do the
secure-entry or colour cases — it should flag those for Appium/XCUITest rather than writing
a weak assertion.

---

## Prompt 3: Checkout flows
*Used in: Section 8, Clip 3*

```
Following skills/test-authoring.md, build the CHECKOUT flows from test-cases.md — one flow
per matrix case, under maestro/flows/. The matrix marks which checkout cases are blocked by
the unresponsive "Proceed to Checkout" button (they can only be verified on the fixed
build) — respect those markings and explain the dependency in the flow.

List the flows you created and the test-case ID each covers.
```

**Expected:** one flow per checkout case; the blocker dependency is documented in the flows.

---

## Prompt 4: One flow, two apps
*Used in: Section 8, Clip 4*

```
Without changing any flow, run your login happy-path flow against the SwiftUI build, then
reinstall the React Native build (same bundle id) and run the same flow again. Explain why
the identical flow works on both, and where in the accessibility tree the two apps differ.
```

**Expected:** the same YAML passes on both builds — the payoff of stable accessibility ids.
This is the bridge to the Android course, where the same flows carry across platforms.
