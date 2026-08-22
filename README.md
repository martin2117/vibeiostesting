# Vibetesting in 2026: iOS Mobile App Testing with Maestro, Appium & XCUITest — Course Repository

Resources for the Udemy course. Everything you need to follow along is in this repo.

> **You need a Mac.** iOS testing requires macOS + Xcode's iOS Simulator. There is no
> supported way to run these on Windows or Linux.

## Getting started

**Fork this repo** (click **Fork**, top-right) so you have your own copy to commit
to and push from, then clone your fork:

```
git clone git@github.com:<your-username>/vibeiostesting.git
cd vibeiostesting
```

Full setup — Xcode, Node, Antigravity, Maestro, Appium, and the mobile MCP — is Section 3.

---

## What's in here

```
vibeiostesting/
├── techshop/                     ← The app under test — two implementations
│   ├── swiftui-broken/           ← Native SwiftUI — 15 bugs planted (+2 mobile-specific)
│   ├── swiftui-fixed/            ← Native SwiftUI — clean, used in verification
│   ├── reactnative-broken/       ← React Native (Expo) — SAME 15 bugs
│   ├── reactnative-fixed/        ← React Native (Expo) — clean
│   └── requirements.md           ← Sprint 1 spec — the Section 4 coverage check
│
├── capstone/                     ← Your independent project (Section 15)
│   ├── booknow-swiftui-broken/   ← Hotel booking app — bugs planted, count not disclosed
│   ├── booknow-swiftui-fixed/
│   ├── booknow-reactnative-broken/
│   ├── booknow-reactnative-fixed/
│   └── requirements.md           ← BookNow spec — verify the app against it
│
├── skills/                       ← YOU BUILD in Section 5 — starts empty
├── maestro/                      ← YOU BUILD in Section 8 — starts empty
├── appium/                       ← YOU BUILD in Section 9 — starts empty
├── xcuitest/                     ← YOU BUILD in Section 10 — starts empty
├── .github/workflows/            ← YOU BUILD in Section 14 — starts empty
│
├── docs/                         ← Written guides — the companion to each lecture
│   ├── setup-01…setup-07-*.md    ← Xcode, Node, Maestro, Appium, XCUITest, mobile MCP
│   ├── s04…s16-*.md              ← one guide per section
│   └── README.md                 ← index
│
├── prompts/                      ← Every Antigravity prompt, by section + clip
│   └── section-03-setup.md … section-15-capstone.md
│
└── snippets/                     ← Setup commands, MCP config, CLI references, cheat sheet
```

> **This is a build-along course.** `skills/`, `maestro/`, `appium/`, `xcuitest/`, and
> `.github/workflows/` start **empty** — you generate every one of them yourself with the
> AI agent during the course, guided by the `prompts/` and `docs/`. Your instructor builds
> the same artifacts live and shares the finished versions as the class answer key — but
> the learning is in the doing, so build yours first.

---

## Running TechShop iOS

### SwiftUI build

Open `techshop/swiftui-broken/TechShop.xcodeproj` in Xcode, pick an iPhone Simulator,
and press **Run** (⌘R). Or from the command line:

```bash
cd techshop/swiftui-broken
xcodebuild -scheme TechShop -destination 'platform=iOS Simulator,name=iPhone 16' build
```

### React Native (Expo) build

```bash
cd techshop/reactnative-broken
npm install
npx expo start --ios      # boots the Simulator and installs the app
```

**Test credentials:** `demo@techshop.com` / `password123`

> **One build at a time — reinstall when you switch.** All four builds (SwiftUI/React
> Native × broken/fixed) share the bundle id `com.techshop.ios`, so only one can be
> installed on the Simulator at once. Whenever you switch — **broken → fixed** for the
> Section 13 regression, or SwiftUI ↔ React Native — **uninstall the current app first (or
> reinstall over it)** so you're actually running the build you think you are. The test
> suites relaunch the app fresh on every test, so in-run state is handled for you; this is
> only about *which build* is installed. For **Section 4 exploration**, start from a clean
> install of the **broken** build.

The **same 15 bugs** are planted in both builds, so a Maestro/Appium suite you write once
runs against both — and you get to watch it behave differently under the hood.

---

## The 15 Bugs (broken builds only) — what the suites target

| ID | Area | What's wrong | Caught by |
|----|------|-------------|-----------|
| BUG-001 | Login | Password field is not a secure entry — plaintext | Secure-entry / attribute assertion |
| BUG-002 | Login | Empty email/password accepted | Negative test |
| BUG-003 | Login | Wrong credentials still navigate to catalog | Negative test |
| BUG-004 | Cart | Discount divides by 1000 not 100 | Computed-total assertion |
| BUG-005 | Cart | Quantity stepper decrements below 1 | Boundary test |
| BUG-006 | Cart | Total does not update on quantity change | State assertion |
| BUG-007 | Catalog | Long product names overflow / clip the cell | Optional visual assertion |
| BUG-008 | Catalog | "Out of Stock" badge is green, not red | Optional visual assertion |
| BUG-009 | Checkout | Expiry date accepts past dates | Negative test |
| BUG-010 | Checkout | CVV accepts letters/symbols — keyboard not numeric | Input validation test |
| BUG-011 | Checkout | "Proceed to Checkout" unresponsive (blocker) | Tap / navigation assertion |
| BUG-012 | Checkout | Form submits with all fields empty | Negative test |
| BUG-013 | Checkout | Confirmation missing order reference | Presence assertion |
| BUG-014 | General | Navigation title shows "Untitled" | Title assertion |
| BUG-015 | General | Tab bar visible before auth | Visibility assertion |

**Mobile-specific bonus bugs:**

| ID | Area | What's wrong | Caught by |
|----|------|-------------|-----------|
| BUG-016 | Accessibility | Login button has no accessibility identifier | Testability lesson — add one |
| BUG-017 | Keyboard | Keyboard covers the CVV field and won't dismiss | Interaction / scroll test |

> **BUG-011 is a blocker** for checkout flows — the "Proceed to Checkout" button does not
> respond to taps. Note this dependency in any checkout test; it is a realistic example of
> a bug that blocks other tests.
>
> **BUG-016 is special:** you cannot write a stable test for the login button until the
> app is given an accessibility identifier. This is the mobile testability lesson — the
> agent proposes the fix, then the test becomes writable.

---

## Credentials — keep secrets out of your code

The suites read credentials from environment variables. Never hardcode usernames,
passwords, or tokens in flow files, test code, prompts, or commits.

**Local:** copy `.env.example` to `.env`, fill in your values. `.env` is gitignored.

**CI (GitHub Actions):** add `TEST_EMAIL` and `TEST_PASSWORD` as repository secrets.

---

## The mobile MCP (Antigravity)

The agent drives a real iOS Simulator through a mobile MCP server (tap, type, read the
screen, report what it sees) — the mobile equivalent of Playwright MCP for the web.

1. Install Xcode, boot a Simulator, install the app under test.
2. Add the mobile MCP server to Antigravity's MCP config.
3. Restart Antigravity and confirm the agent can see the Simulator.

Full step-by-step is in **[docs/setup-06-mobile-mcp.md](docs/setup-06-mobile-mcp.md)**.

---

## Written guides

Every lecture has a written companion in **[`docs/`](docs/README.md)** — the exact
commands, capabilities, config, templates, and troubleshooting you cannot pause a video
to copy.

---

## How to use the prompts

Each file in `prompts/` maps to a course section and lists every prompt with the exact
clip it is used in. Copy the prompt, paste it into the Antigravity chat, and follow along.
Prompts reference the skills in `skills/` and the app running on the Simulator.

## Course sections and what to find here

| Section | What to grab |
|---------|-------------|
| 3 — Setup | `techshop/*`, `prompts/section-03-setup.md`, MCP config |
| 4 — Exploration | `techshop/*`, `techshop/requirements.md`, `prompts/section-04-exploration.md` |
| 5 — Skills | `prompts/section-05-skills.md` → builds `skills/` |
| 6 — Accessibility tree | `prompts/section-06-accessibility.md` |
| 7 — Test cases | `prompts/section-07-testcases.md` |
| 8 — Maestro | `prompts/section-08-maestro.md`, `maestro/` |
| 9 — Appium | `prompts/section-09-appium.md`, `appium/` |
| 10 — XCUITest | `prompts/section-10-xcuitest.md`, `xcuitest/` |
| 11 — Compared | `prompts/section-11-compare.md`, framework comparison cheat sheet |
| 12 — Bugs | `prompts/section-12-bugs.md` |
| 13 — Stability | `prompts/section-13-stability.md`, `techshop/*-fixed` |
| 14 — CI | `prompts/section-14-ci.md`, `.github/workflows/*` |
| 15 — Capstone | `prompts/section-15-capstone.md`, `capstone/*` |
