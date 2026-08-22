# TechShop iOS — Defect Reports (Section 12)

This directory contains formal, developer-ready bug reports for all confirmed real defects identified in the broken build during automated and manual testing across **Maestro**, **Appium**, and **XCUITest**.

---

## Master Bug Report Inventory (Ranked by Severity)

| Bug ID | Title | Severity | Frameworks | Cross-Build Status | Blocker Context |
|---|---|---|---|---|---|
| [BUG-011](BUG-011.md) | Proceed to Checkout Button Is Unresponsive | **Critical** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | **Primary Blocker** (Blocks BUG-009, 010, 012, 013, 017) |
| [BUG-001](BUG-001.md) | Password Input Renders Plaintext Characters Instead of Secure Masked Text | **High** | Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-002](BUG-002.md) | Login Submission Accepts Empty and Incomplete Credentials | **High** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-003](BUG-003.md) | Login Form Accepts Incorrect Password and Unregistered Email | **High** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-006](BUG-006.md) | Shopping Cart Order Total Fails to Reactively Update on Quantity Change | **High** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-009](BUG-009.md) | Checkout Payment Form Accepts Expired Credit Card Dates | **High** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | Blocked by BUG-011 |
| [BUG-012](BUG-012.md) | Checkout Form Submits with All Required Fields Empty | **High** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | Blocked by BUG-011 |
| [BUG-017](BUG-017.md) | Software Keyboard Obscures CVV Input Field and Checkout Action | **High** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | Blocked by BUG-011 |
| [BUG-004](BUG-004.md) | Discount Calculation Divides by 1000 Instead of 100 | **Medium** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-005](BUG-005.md) | Shopping Cart Quantity Stepper Decrements Below 1 | **Medium** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-010](BUG-010.md) | Checkout CVV Accepts Alphabetical Input and Lacks Numeric Keypad | **Medium** | Appium / XCUITest / Maestro | Both SwiftUI & React Native | Blocked by BUG-011 |
| [BUG-013](BUG-013.md) | Confirmation Screen Missing Order Reference Identifier | **Medium** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | Blocked by BUG-011 |
| [BUG-015](BUG-015.md) | Bottom Tab Bar Navigation Is Visible and Interactive Prior to Authentication | **Medium** | Maestro / Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-007](BUG-007.md) | Product Catalog Long Title Overflows Cell Height Bounds | **Low** | Appium / XCUITest | Both SwiftUI & React Native | No |
| [BUG-008](BUG-008.md) | Out-of-Stock Status Badge Rendered in Green Instead of Red | **Low** | Manual / Visual | Both SwiftUI & React Native | No |
| [BUG-014](BUG-014.md) | Product Catalog Navigation Bar Title Displays "Untitled" | **Low** | Maestro / XCUITest | Both SwiftUI & React Native | No |
| [BUG-016](BUG-016.md) | Log In Submit Button Lacks Accessibility Identifier | **Low** | Appium / XCUITest / Maestro | Both SwiftUI & React Native | Testability Defect |
