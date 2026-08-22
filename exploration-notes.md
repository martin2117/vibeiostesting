# TechShop — Exploratory Testing Notes

**Build under test:** `swiftui-broken` · bundle ID `com.techshop.ios`  
**Device:** iPhone 17 Pro Simulator · iOS 26.5  
**Session date:** 2026-08-22

---

## Login

### Elements & Accessibility Identifiers

| # | Element | Type | Accessibility identifier | Notes |
|---|---------|------|--------------------------|-------|
| 1 | TechShop title | `StaticText` | ⚠️ **NONE** (`name="TechShop"`) | No `identifier`; label-only |
| 2 | "Sign in to continue" subtitle | `StaticText` | ⚠️ **NONE** (`name="Sign in to continue"`) | No `identifier` |
| 3 | Email input | `TextField` | ✅ `login-email` | |
| 4 | Password input | `TextField` | ✅ `login-password` | ⚠️ Type is `TextField`, not `SecureTextField` — password characters are **not masked** |
| 5 | Log In button | `Button` | ⚠️ **NONE** (`name="Log In"`) | No `identifier` — **BUG-016** |
| 6 | Sign In tab (tab bar) | `Button` | `name="Sign In"` (unselected: `identifier="person"`) | Tab bar should not exist here |
| 7 | Products tab (tab bar) | `Button` | `name="Products"` (unselected: `identifier="bag"`) | Tab bar should not exist here |
| 8 | Cart tab (tab bar) | `Button` | `name="Cart"` (unselected: `identifier="cart"`) | Tab bar should not exist here |

**Controls with NO accessibility identifier:** Title label, subtitle label, **Log In button** (the most important interactive element on this screen).

---

### Flows Tested

#### Flow 1 — Empty submit (both fields blank)

1. Launched app fresh → Login screen appeared.
2. Tapped **Log In** without entering anything in `login-email` or `login-password`.
3. **Result:** App navigated directly to the Product Catalog screen.
4. No error message, no alert, no field highlighting, no shake animation — complete silence.

#### Flow 2 — Wrong password

1. Tapped `login-email` → typed `demo@techshop.com` → pressed Return to dismiss keyboard.
2. Tapped `login-password` → typed `wrongpassword`.
3. Tapped **Log In**.
4. **Result:** App navigated directly to the Product Catalog screen — identical to Flow 1.
5. No "Incorrect password" alert, no inline error, no indication the credentials were rejected.

#### Flow 3 — Valid credentials

1. Tapped `login-email` → typed `demo@techshop.com` → pressed Return.
2. Tapped `login-password` → typed `password123`.
3. Tapped **Log In**.
4. **Result:** App navigated to the Product Catalog screen — same destination as Flows 1 and 2.
5. Visually and behaviourally indistinguishable from the two failing flows above.

---

### Observations & Anomalies

#### 🔴 BUG-002 / BUG-003 — Login accepts any credentials (no auth check)
All three input combinations — empty, wrong password, and correct password — produced exactly the same outcome: silent navigation to the catalog. The login form performs no credential validation whatsoever. This means any user (or automated script) can bypass authentication entirely.

**Expected:** Empty or invalid credentials should show an error (e.g. "Invalid email or password") and keep the user on the login screen. Only the correct pair should advance.

#### 🔴 BUG-001 — Password field is not masked
The `login-password` field is declared as `TextField` in the accessibility tree, not `SecureTextField`. The typed password appears as plain text in the accessibility hierarchy and would be visible on-screen to anyone looking over the user's shoulder. iOS's built-in password masking (bullet characters) is absent.

**Expected:** `login-password` should be a `SecureTextField`; characters should be replaced with bullets immediately after typing.

#### 🔴 BUG-016 — Log In button has no accessibility identifier
The button's accessibility representation is `name="Log In"` with no `identifier` property set. A label-only reference is fragile — if the button text ever changes (localisation, copy update), any XCUITest targeting it by label will break.

**Expected:** The button should have a stable `identifier` such as `login-button` or `login-submit`.

#### 🟡 BUG-015 — Tab bar visible and interactive before authentication
The tab bar (Sign In / Products / Cart) renders at the bottom of the login screen before the user has authenticated. Tapping "Products" or "Cart" at this point bypasses the login screen via the tab bar — a separate auth-bypass vector.

**Expected:** The tab bar should only appear after a successful login. During the unauthenticated state, only the login form should be visible.

#### 🟡 Surprising: valid and invalid login are indistinguishable
A correct login should feel different from a failed one — at minimum via a different navigation destination, a welcome message, or a logged-in state indicator. Here, all outcomes are identical, which means even if credential checking were fixed, the UI provides no feedback that "you are now logged in as demo@techshop.com".

---

### Quick Reference — Login Screen Element IDs

```
login-email       TextField   ← email input
login-password    TextField   ← password input (NOT SecureTextField — bug)
(none)            Button      ← Log In button — NO identifier (bug)
```

---

## Catalog

### Elements & Accessibility Identifiers

| # | Element | Type | Accessibility identifier | Notes |
|---|---------|------|--------------------------|-------|
| 1 | Page title | `StaticText` | ⚠️ **NONE** (`name="Untitled"`) | Should read "Products" — **BUG-014** |
| 2 | Product 1 name — Wireless Headphones | `StaticText` | ✅ `product-name-p1` | |
| 3 | Product 1 price — $60 | `StaticText` | ⚠️ **NONE** (`name="$60"`) | Price labels have no identifier |
| 4 | Product 1 Add button | `Button` | ✅ `add-p1` | |
| 5 | Product 2 name — Mechanical Keyboard | `StaticText` | ✅ `product-name-p2` | |
| 6 | Product 2 price — $90 | `StaticText` | ⚠️ **NONE** (`name="$90"`) | |
| 7 | Product 2 Add button | `Button` | ✅ `add-p2` | |
| 8 | Product 3 name — Ultra-Wide Curved 49-inch Professional Gaming Monitor with HDR | `StaticText` | ✅ `product-name-p3` | ⚠️ Name spans 76px height vs ~19px for others — text overflows row (**BUG-007**) |
| 9 | Product 3 price — $700 | `StaticText` | ⚠️ **NONE** (`name="$700"`) | |
| 10 | Product 3 Add button | `Button` | ✅ `add-p3` | |
| 11 | Product 4 name — USB-C Hub | `StaticText` | ✅ `product-name-p4` | |
| 12 | Product 4 price — $40 | `StaticText` | ⚠️ **NONE** (`name="$40"`) | |
| 13 | Product 4 "Out of Stock" badge | `StaticText` | ✅ `badge-p4` | ⚠️ Badge renders in **green** — should be red (**BUG-008**) |
| 14 | Product 4 Add button (OOS) | `Button` | ✅ `add-p4` | Visually greyed out; tapping it correctly does NOT add the item to cart |

**Controls with NO accessibility identifier:** Page title, all four price labels.

---

### Flows Tested

#### Flow 1 — Browse and Add to cart

1. Tapped `add-p1` (Wireless Headphones) three times in rapid succession.
2. **Result in catalog:** No visible feedback on the catalog screen — button does not change label, no count badge, no animation observed. The Add button appeared to do nothing.
3. Navigated to Cart tab to verify.
4. **Result in cart:** All three taps registered — qty showed 3, line total $180. Items were silently added with no in-catalog confirmation.

#### Flow 2 — Tap Add on Out-of-Stock item

1. Tapped `add-p4` (USB-C Hub, marked "Out of Stock").
2. Navigated to Cart.
3. **Result:** USB-C Hub did not appear in the cart. The greyed-out button correctly blocked the add.

---

### Observations & Anomalies

#### 🔴 BUG-014 — Navigation title is "Untitled"
The catalog page title displays "Untitled" instead of an expected label such as "Products". This is a clear data/configuration error visible immediately on entering the screen.

#### 🟡 BUG-007 — Long product name overflows its row
Product 3 ("Ultra-Wide Curved 49-inch Professional Gaming Monitor with HDR") wraps to multiple lines inside what should be a fixed-height list cell. Its bounding box is 76px tall vs ~19px for single-line items, suggesting the name label has no line limit set. This would cause layout breakage for any product with a long name.

#### 🟡 BUG-008 — Out-of-stock badge is green (should be red/orange)
The "Out of Stock" badge on USB-C Hub renders in green — the colour typically associated with availability or success. A red or amber badge is the conventional signal for unavailability. This is a visual/semantic mismatch that could mislead users.

#### 🟡 No add-to-cart feedback in catalog
Tapping an Add button gives zero in-catalog visual confirmation — no count increment on the button, no toast, no animation. The item was added (confirmed in cart), but users cannot tell whether their tap registered. This is a UX gap, not listed as a planted bug, but worth noting.

---

## Cart

### Elements & Accessibility Identifiers

| # | Element | Type | Accessibility identifier | Notes |
|---|---------|------|--------------------------|-------|
| 1 | "Cart" title | `StaticText` | ⚠️ **NONE** (`name="Cart"`) | No identifier |
| 2 | Item name — Wireless Headphones | `StaticText` | ⚠️ **NONE** (`name="Wireless Headphones"`) | No identifier on cart row names |
| 3 | Unit price — $60 each | `StaticText` | ⚠️ **NONE** (`name="$60 each"`) | No identifier |
| 4 | Line total | `StaticText` | ✅ `line-total-p1` | Updates correctly when qty changes |
| 5 | Decrement (−) button | `Button` | ✅ `qty-decrement-p1` | Allows qty below 1 — **BUG-005** |
| 6 | Quantity display | `StaticText` | ✅ `qty-p1` | Shows negative values when bug triggered |
| 7 | Increment (+) button | `Button` | ✅ `qty-increment-p1` | Works; but Order Total doesn't update — **BUG-006** |
| 8 | Discount code input | `TextField` | ✅ `discount-input` | Accepts text; discount has no visible effect — **BUG-004** |
| 9 | Subtotal label | `StaticText` | ⚠️ **NONE** (`name="Subtotal: $XX"`) | Updates when qty changes |
| 10 | Order Total label | `StaticText` | ✅ `order-total` | **Stale — does not update on qty change** (**BUG-006**) |
| 11 | Proceed to Checkout button | `Button` | ✅ `proceed-checkout` | Tapping does **nothing** — **BUG-011** |

**Controls with NO accessibility identifier:** Cart title, item name rows, unit price, Subtotal label.

---

### Flows Tested

#### Flow 1 — Increment quantity

1. Tapped `qty-increment-p1` with 3 items in cart (qty=3, Line=$180, Subtotal=$180, Order Total=$180).
2. **Result:** qty→4, `line-total-p1`→$240, Subtotal→$240. **Order Total stayed at $180** — did not update.

#### Flow 2 — Decrement quantity below 1

1. Tapped `qty-decrement-p1` five times from qty=4.
2. Passed through: 3 → 2 → 1 → 0 → **-1**. Decrement was not blocked at 1.
3. At qty=-1: `line-total-p1`="Line: $-60", Subtotal="Subtotal: $-60". Order Total still stale.
4. No error, no minimum-quantity guard, no item removal.

#### Flow 3 — Apply discount code SAVE10

1. Tapped `discount-input`, typed `SAVE10`, pressed Return.
2. **Result:** Code accepted (visible in field). Subtotal=$60, Order Total=$60. No "Discount applied" confirmation. No visible reduction in the displayed total — expected $54 ($60 - 10%), got $60.
3. The discount amount is computed as $60 × 10% ÷ 1000 = $0.006, which rounds to $0 in integer display — effectively invisible.

#### Flow 4 — Tap "Proceed to Checkout"

1. Tapped `proceed-checkout` twice.
2. **Result both times:** Nothing happened. Screen remained on the Cart view. No navigation, no animation, no error message.
3. The checkout screen is **completely unreachable** from the broken build via this button.

---

### Observations & Anomalies

#### 🔴 BUG-011 — "Proceed to Checkout" is a no-op (BLOCKER)
Tapping the `proceed-checkout` button produced zero response on two consecutive taps. The app stays on the Cart screen. This blocks all downstream checkout and confirmation testing in this build.

**Expected:** Tapping "Proceed to Checkout" should navigate to a Checkout screen with name, card number, expiry, and CVV fields.

#### 🔴 BUG-005 — Quantity can go below 1 (into negative values)
The `qty-decrement-p1` button has no floor guard. Tapping it at qty=1 reduces to 0, then -1, and further. At qty=-1 the line total displays "$-60" and the subtotal goes negative. The cart remains in this broken state with no warning.

**Expected:** At qty=1, the decrement button should either be disabled or remove the item from the cart. Negative quantities should never be possible.

#### 🔴 BUG-006 — Order Total does not update when quantity changes
When qty is changed (up or down), the Line total and Subtotal update correctly, but `order-total` remains frozen at the value it held when the cart was first rendered. Only a full screen reload causes it to recalculate.

**Expected:** `order-total` should reactively update any time qty or discount changes.

#### 🔴 BUG-004 — Discount code SAVE10 has no visible effect
Entering `SAVE10` is accepted silently but does not reduce the Order Total in any perceptible way. The discount amount is divided by 1000 internally, making it effectively $0.00 — invisible in the rounded display. No "Discount applied" or "Invalid code" message is shown.

**Expected:** Applying SAVE10 to a $60 subtotal should deduct $6, showing an Order Total of $54, with a confirmation message (e.g. "10% discount applied").

---

## Checkout

Checkout is **unreachable** in this build due to **BUG-011** (Proceed to Checkout no-op). No elements could be inspected or interacted with on the Checkout screen via the broken build.

Checkout bugs (BUG-009 past expiry accepted, BUG-010 CVV non-numeric keyboard, BUG-012 empty form submits, BUG-013 no order reference, BUG-017 keyboard covers CVV) must be verified against the **swiftui-fixed** build where the Proceed button works.
---

## Requirements Coverage Analysis

_Compared against `techshop/requirements.md` (Sprint 1)._

---

### Login Screen

| Req | Requirement | Status | Notes |
|-----|-------------|--------|-------|
| L1 | Users log in with email and password | ✅ Observed | Fields present; form submittable |
| L2 | Email must be valid format (contains @ and domain) | ❌ NOT exercised | Did not test a malformed email (e.g. `notanemail`); format validation may not exist given BUG-002/003 |
| L3 | Password field must **mask input** | ❌ CONTRADICTS SPEC | `login-password` is `TextField` — password shown in plain text (**BUG-001**) |
| L4 | Empty fields must be rejected with an inline error message | ❌ CONTRADICTS SPEC | Empty submit navigates to catalog silently (**BUG-002**) |
| L5 | Valid credentials: demo@techshop.com / password123 | ✅ Observed | Correct credentials accepted and navigated to catalog |
| L6 | Successful login navigates to product catalog | ✅ Observed | Navigation occurs (though it also occurs for invalid creds) |
| L7 | Failed login shows an error, stays on the login screen | ❌ CONTRADICTS SPEC | Wrong password navigates to catalog; no error shown (**BUG-003**) |
| L8 | Session persists for the app session | ❌ NOT exercised | Did not background/foreground the app to test session persistence |
| L9 | Tab bar is **hidden** until user is authenticated | ❌ CONTRADICTS SPEC | Tab bar visible on login screen (**BUG-015**) |
| L10 | Every interactive element must have an accessibility identifier | ❌ CONTRADICTS SPEC | Log In button has no `identifier` (**BUG-016**) |

---

### Product Catalog

| Req | Requirement | Status | Notes |
|-----|-------------|--------|-------|
| C1 | Scrollable list of available products | ✅ Observed | 4 products displayed; did not test scroll (only 4 items, fits on screen) |
| C2 | Each cell: product name, price, image placeholder, Add button | ✅ Observed (partial) | Name ✅, price ✅, Add button ✅; image area present but no image content observed |
| C3 | Long product names must truncate cleanly, not overflow the cell | ❌ CONTRADICTS SPEC | Product 3 name wraps to 76px height — overflows cell (**BUG-007**) |
| C4 | Out-of-stock shows a **red** badge and disabled button | ❌ CONTRADICTS SPEC (partial) | Badge present and button disabled ✅; badge colour is **green** not red (**BUG-008**) |
| C5 | Navigation title: "Products" | ❌ CONTRADICTS SPEC | Title shows "Untitled" (**BUG-014**) |

---

### Shopping Cart

| Req | Requirement | Status | Notes |
|-----|-------------|--------|-------|
| S1 | Add products from catalog | ✅ Observed | Items added correctly (3 × Wireless Headphones) |
| S2 | Cart shows: name, unit price, quantity, line total, order total | ✅ Observed | All fields present and labelled |
| S3 | Quantity stepper — **minimum 1**, no negative or zero | ❌ CONTRADICTS SPEC | Qty goes to 0 and -1; line total goes negative (**BUG-005**) |
| S4 | Order total updates immediately when quantity changes | ❌ CONTRADICTS SPEC | `order-total` frozen at first-render value; does not update on qty change (**BUG-006**) |
| S5 | Remove individual items | ❌ NOT exercised | No remove/delete button observed in the cart element list; may be absent entirely |
| S6 | Empty cart message: "Your cart is empty" | ❌ NOT exercised | Did not fully empty the cart to check this message |
| S7 | Discount code applies percentage discount (SAVE10 = 10% off) | ❌ CONTRADICTS SPEC | SAVE10 accepted but discount is ÷1000 internally → $0.006 off; no visible effect (**BUG-004**) |
| S8 | Cart state persists within the app session only | ❌ NOT exercised | Did not test across tab switches sufficiently to confirm persistence |
| S9 | Orders under $10.00 rejected with message | ❌ NOT exercised | Did not attempt a sub-$10 checkout (also blocked by BUG-011) |

---

### Checkout Screen

| Req | Requirement | Status | Notes |
|-----|-------------|--------|-------|
| CH1 | Accessible via "Proceed to Checkout" button | ❌ CONTRADICTS SPEC | Button is a complete no-op (**BUG-011 — BLOCKER**) |
| CH2 | Fields: First Name, Last Name, Email, Phone, Card Number, Expiry, CVV | ❌ NOT exercised | Screen unreachable |
| CH3 | All fields required — empty submission rejected | ❌ NOT exercised | Screen unreachable (**BUG-012**) |
| CH4 | Email: valid format | ❌ NOT exercised | Screen unreachable |
| CH5 | Card Number: exactly 16 digits, numeric keypad | ❌ NOT exercised | Screen unreachable |
| CH6 | Phone: 10 digits, numeric keypad | ❌ NOT exercised | Screen unreachable |
| CH7 | Expiry: MM/YY, not in the past | ❌ NOT exercised | Screen unreachable (**BUG-009**) |
| CH8 | CVV: exactly 3 digits, numeric keypad only | ❌ NOT exercised | Screen unreachable (**BUG-010**) |
| CH9 | Keyboard must not permanently cover field being edited | ❌ NOT exercised | Screen unreachable (**BUG-017**) |
| CH10 | Success: confirmation screen with order reference, items, total | ❌ NOT exercised | Screen unreachable (**BUG-013**) |

---

### Summary Counts

| Outcome | Count |
|---------|-------|
| ✅ Requirement observed / met | 7 |
| ❌ Requirement contradicts the spec (bug confirmed) | 10 |
| ❌ Requirement not yet exercised | 11 |
| **Total requirements** | **28** |

### Not-Yet-Exercised — Priority Order for Next Session

1. **S5** — Remove individual items from cart (button not visible in current build — may be missing)
2. **S6** — Empty cart state message
3. **S9** — Sub-$10 order rejection
4. **L2** — Malformed email format rejection
5. **L8** — Session persistence (background/foreground)
6. **S8** — Cart state across tab navigation
7. **CH2–CH10** — All checkout fields and validation (requires fixed build due to BUG-011)
