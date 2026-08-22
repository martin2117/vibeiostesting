# Section 4 — Exploring TechShop iOS with an AI Agent

> 📖 **Guide:** [s04 exploration](../docs/s04-exploration.md) · spec in [../techshop/requirements.md](../techshop/requirements.md)

The agent drives the Simulator via the mobile MCP and explores the app *before any test
exists*. You capture what it finds into `exploration-notes.md` — the raw material for the
test matrix in Section 7.

> **Explore the BROKEN build** (`techshop/reactnative-broken` or `techshop/swiftui-broken`) —
> that is the version with the planted bugs. Start from a **clean install** (Prompt 1
> handles this) so you're exploring the pristine buggy app, not a modified or stateful copy.

## Course reference
| Prompt | Used in clip |
|--------|-------------|
| Prompt 1 — Explore the login flow | **4, Clip 2** |
| Prompt 2 — Capture notes | **4, Clip 3** |
| Prompt 3 — Repeat for cart & checkout | **4, Clip 3** |
| Prompt 4 — Coverage vs requirements | **4, Clip 4** |

---

## Prompt 1: Explore the login flow live
*Used in: Section 4, Clip 2*

```
First, make sure the app under test is the BROKEN build — techshop/reactnative-broken
(or techshop/swiftui-broken), NOT the fixed build. Install a clean, fresh copy: uninstall
any existing com.techshop.ios from the Simulator, then reinstall the broken build and
launch it, so we explore the pristine buggy version with no leftover state.

Then, using the mobile MCP, drive the TechShop login screen. Try: a valid login
(demo@techshop.com / password123), an empty submit, and a wrong password. After each,
describe what actually happened (which screen, any error) and list the accessibility
identifiers of every field and button you interacted with. Do not write any test yet.
```

## Prompt 2: Capture notes
*Used in: Section 4, Clip 3*

```
Write what you just observed into exploration-notes.md under a "Login" heading: the
elements and their ids (flag any control with NO id), the flows you tried, and anything
that looked wrong or surprising versus what a login should do.
```

## Prompt 3: Repeat for cart and checkout
*Used in: Section 4, Clip 3*

```
Now explore the catalog, cart, and checkout the same way (add an item, change quantity,
apply a discount, try to proceed to checkout, attempt a purchase). Append a section per
flow to exploration-notes.md — elements + ids + anything that behaves oddly. If a button
does nothing when tapped, record exactly that.
```

## Prompt 4: Coverage against the requirements
*Used in: Section 4, Clip 4*

```
Read techshop/requirements.md. Compare it to exploration-notes.md and list: which
requirements you have observed, which you have not exercised yet, and any behaviour that
contradicts the spec.
```

**Expected:** a populated `exploration-notes.md` and a coverage list — the input to the
test-case-design skill. Several of the "odd" behaviours you recorded are the planted bugs.
