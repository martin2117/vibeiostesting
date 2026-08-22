import XCTest

/// Checkout UI test suite covering form navigation, validation rules,
/// payment processing, order confirmation, and keyboard interaction.
///
/// NOTE:
/// - `test_tc_chk_001_navigate_from_cart_to_checkout` runs on both broken and fixed builds;
///   on the broken build, it catches BUG-011 (the unresponsive "Proceed to Checkout" blocker).
/// - Tests `test_tc_chk_002` through `test_tc_chk_010` run on the fixed build only
///   because BUG-011 prevents reaching the Checkout screen in the broken build.
final class CheckoutUITests: TechShopUITestCase {

    // MARK: - Helpers

    /// Navigates from unauthenticated launch through login, adding item p1 to cart,
    /// and tapping "Proceed to Checkout".
    private func navigateToCheckout() {
        addItemAndOpenCart()
        let proceedBtn = el("proceed-checkout")
        XCTAssertTrue(proceedBtn.waitForExistence(timeout: 5.0), "Expected 'Proceed to Checkout' button to exist in Cart")
        proceedBtn.tap()
    }

    /// Fills the checkout form fields with the provided values.
    private func fillCheckoutForm(
        firstName: String? = "Jane",
        lastName: String? = "Doe",
        email: String? = "jane.doe@example.com",
        phone: String? = "1234567890",
        card: String? = "1111222233334444",
        expiry: String? = "12/29",
        cvv: String? = "123"
    ) {
        if let firstName = firstName, !firstName.isEmpty {
            let fn = el("checkout-firstName")
            if fn.waitForExistence(timeout: 3.0) { fn.tap(); fn.typeText(firstName) }
        }
        if let lastName = lastName, !lastName.isEmpty {
            let ln = el("checkout-lastName")
            if ln.waitForExistence(timeout: 3.0) { ln.tap(); ln.typeText(lastName) }
        }
        if let email = email, !email.isEmpty {
            let em = el("checkout-email")
            if em.waitForExistence(timeout: 3.0) { em.tap(); em.typeText(email) }
        }
        if let phone = phone, !phone.isEmpty {
            let ph = el("checkout-phone")
            if ph.waitForExistence(timeout: 3.0) { ph.tap(); ph.typeText(phone) }
        }
        if let card = card, !card.isEmpty {
            let cd = el("checkout-card")
            if cd.waitForExistence(timeout: 3.0) { cd.tap(); cd.typeText(card) }
        }
        if let expiry = expiry, !expiry.isEmpty {
            let ex = el("checkout-expiry")
            if ex.waitForExistence(timeout: 3.0) { ex.tap(); ex.typeText(expiry) }
        }
        if let cvv = cvv, !cvv.isEmpty {
            let cv = el("checkout-cvv")
            if cv.waitForExistence(timeout: 3.0) { cv.tap(); cv.typeText(cvv) }
        }
        dismissKeyboardIfPresent()
    }

    /// Safely dismisses the software keyboard if active so submit buttons are not blocked.
    private func dismissKeyboardIfPresent() {
        if app.keyboards.element.exists {
            if app.buttons["Done"].exists {
                app.buttons["Done"].tap()
            } else if app.buttons["Return"].exists {
                app.buttons["Return"].tap()
            } else {
                app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.1)).tap()
            }
        }
    }

    // MARK: - TC-CHK-001: Navigation to Checkout (BUG-011 Blocker)

    /// TC-CHK-001: Navigate from Cart to Checkout screen via Proceed button.
    /// Category: Positive (Regression: BUG-011)
    /// Runs on: Broken & Fixed builds.
    /// Catches BUG-011 (Blocker): on the broken build, "Proceed to Checkout" is a no-op.
    func test_tc_chk_001_navigate_from_cart_to_checkout() {
        addItemAndOpenCart()

        let proceedBtn = el("proceed-checkout")
        XCTAssertTrue(proceedBtn.waitForExistence(timeout: 5.0), "Expected 'Proceed to Checkout' button in Cart")
        proceedBtn.tap()

        let firstNameField = el("checkout-firstName")
        XCTAssertTrue(
            firstNameField.waitForExistence(timeout: 5.0),
            "BUG-011 [BLOCKER]: 'Proceed to Checkout' button is unresponsive; failed to navigate to Checkout screen."
        )
    }

    // MARK: - TC-CHK-002: Complete Checkout and Order Reference (BUG-013)

    /// TC-CHK-002: Complete checkout and place order with valid payment details.
    /// Category: Positive (Regression: BUG-013)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    /// Catches BUG-013 if confirmation screen lacks the generated order reference.
    func test_tc_chk_002_complete_checkout_and_place_order() {
        navigateToCheckout()

        let firstNameField = el("checkout-firstName")
        guard firstNameField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        fillCheckoutForm(
            firstName: "Jane",
            lastName: "Doe",
            email: "jane.doe@example.com",
            phone: "1234567890",
            card: "1111222233334444",
            expiry: "12/29",
            cvv: "123"
        )

        let submitBtn = el("checkout-submit")
        XCTAssertTrue(submitBtn.waitForExistence(timeout: 3.0), "Expected 'Place Order' button")
        submitBtn.tap()

        let confirmTitle = el("confirmation-title")
        XCTAssertTrue(confirmTitle.waitForExistence(timeout: 5.0), "Expected 'Order Confirmed' screen")
        XCTAssertEqual(confirmTitle.label, "Order Confirmed")

        let orderRef = el("confirmation-order-ref")
        XCTAssertTrue(orderRef.waitForExistence(timeout: 3.0), "BUG-013: Confirmation screen is missing order reference")
        XCTAssertTrue(
            orderRef.label.contains("TS-"),
            "Expected order reference format TS-XXXXXX, got '\(orderRef.label)'"
        )

        let totalPaid = el("confirmation-total")
        XCTAssertTrue(totalPaid.waitForExistence(timeout: 3.0), "Expected total paid label on confirmation screen")
    }

    // MARK: - TC-CHK-003: Empty Form Rejection (BUG-012)

    /// TC-CHK-003: Reject checkout submission when required fields are empty.
    /// Category: Negative (Regression: BUG-012)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    /// Catches BUG-012 if empty checkout form is submitted without validation.
    func test_tc_chk_003_reject_empty_checkout_submission() {
        navigateToCheckout()

        let firstNameField = el("checkout-firstName")
        guard firstNameField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        let submitBtn = el("checkout-submit")
        XCTAssertTrue(submitBtn.waitForExistence(timeout: 3.0), "Expected 'Place Order' button")
        submitBtn.tap()

        let errorElement = el("checkout-error")
        XCTAssertTrue(
            errorElement.waitForExistence(timeout: 3.0),
            "BUG-012: Empty checkout form was submitted without error"
        )
        XCTAssertEqual(errorElement.label, "All fields are required")
    }

    // MARK: - TC-CHK-004: Invalid Email Format Rejection

    /// TC-CHK-004: Reject checkout submission with invalid email format.
    /// Category: Negative (Requirement: CH4)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    func test_tc_chk_004_reject_invalid_email_format() {
        navigateToCheckout()

        let firstNameField = el("checkout-firstName")
        guard firstNameField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        fillCheckoutForm(
            firstName: "Jane",
            lastName: "Doe",
            email: "bademail",
            phone: "1234567890",
            card: "1111222233334444",
            expiry: "12/29",
            cvv: "123"
        )

        let submitBtn = el("checkout-submit")
        submitBtn.tap()

        let errorElement = el("checkout-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected validation error for invalid email")
        XCTAssertEqual(errorElement.label, "Enter a valid email")
    }

    // MARK: - TC-CHK-005: Non-10-Digit Phone Rejection

    /// TC-CHK-005: Reject checkout submission with non-10-digit phone number.
    /// Category: Negative (Requirement: CH6)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    func test_tc_chk_005_reject_non_10_digit_phone() {
        navigateToCheckout()

        let firstNameField = el("checkout-firstName")
        guard firstNameField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        fillCheckoutForm(
            firstName: "Jane",
            lastName: "Doe",
            email: "jane.doe@example.com",
            phone: "12345",
            card: "1111222233334444",
            expiry: "12/29",
            cvv: "123"
        )

        let submitBtn = el("checkout-submit")
        submitBtn.tap()

        let errorElement = el("checkout-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected validation error for invalid phone")
        XCTAssertEqual(errorElement.label, "Phone must be 10 digits")
    }

    // MARK: - TC-CHK-006: Non-16-Digit Card Rejection

    /// TC-CHK-006: Reject checkout submission with non-16-digit card number.
    /// Category: Negative (Requirement: CH5)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    func test_tc_chk_006_reject_non_16_digit_card() {
        navigateToCheckout()

        let firstNameField = el("checkout-firstName")
        guard firstNameField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        fillCheckoutForm(
            firstName: "Jane",
            lastName: "Doe",
            email: "jane.doe@example.com",
            phone: "1234567890",
            card: "41112222",
            expiry: "12/29",
            cvv: "123"
        )

        let submitBtn = el("checkout-submit")
        submitBtn.tap()

        let errorElement = el("checkout-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected validation error for invalid card number")
        XCTAssertEqual(errorElement.label, "Card number must be 16 digits")
    }

    // MARK: - TC-CHK-007: Expired Card Date Rejection (BUG-009)

    /// TC-CHK-007: Reject checkout submission with expired card date.
    /// Category: Negative (Regression: BUG-009)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    /// Catches BUG-009 if past expiry date is accepted without error.
    func test_tc_chk_007_reject_expired_card_date() {
        navigateToCheckout()

        let firstNameField = el("checkout-firstName")
        guard firstNameField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        fillCheckoutForm(
            firstName: "Jane",
            lastName: "Doe",
            email: "jane.doe@example.com",
            phone: "1234567890",
            card: "1111222233334444",
            expiry: "01/20",
            cvv: "123"
        )

        let submitBtn = el("checkout-submit")
        submitBtn.tap()

        let errorElement = el("checkout-error")
        XCTAssertTrue(
            errorElement.waitForExistence(timeout: 3.0),
            "BUG-009: Expired card date was accepted without error"
        )
        XCTAssertEqual(errorElement.label, "Expiry date must not be in the past")
    }

    // MARK: - TC-CHK-008: Non-3-Digit CVV Rejection (BUG-010)

    /// TC-CHK-008: Reject checkout submission with non-3-digit CVV.
    /// Category: Negative (Regression: BUG-010)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    /// Catches BUG-010 if invalid CVV length is accepted without error.
    func test_tc_chk_008_reject_non_3_digit_cvv() {
        navigateToCheckout()

        let firstNameField = el("checkout-firstName")
        guard firstNameField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        fillCheckoutForm(
            firstName: "Jane",
            lastName: "Doe",
            email: "jane.doe@example.com",
            phone: "1234567890",
            card: "1111222233334444",
            expiry: "12/29",
            cvv: "12"
        )

        let submitBtn = el("checkout-submit")
        submitBtn.tap()

        let errorElement = el("checkout-error")
        XCTAssertTrue(
            errorElement.waitForExistence(timeout: 3.0),
            "BUG-010: Invalid CVV was accepted without error"
        )
        XCTAssertEqual(errorElement.label, "CVV must be 3 digits")
    }

    // MARK: - TC-CHK-009: Numeric Keypad Input Restriction (BUG-010)

    /// TC-CHK-009: Restrict phone, card, and CVV inputs to numeric keypad.
    /// Category: Edge (Regression: BUG-010)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    func test_tc_chk_009_restrict_numeric_keypad_inputs() {
        navigateToCheckout()

        let cvvField = el("checkout-cvv")
        guard cvvField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        cvvField.tap()
        XCTAssertTrue(cvvField.exists, "CVV element must exist and accept input")
    }

    // MARK: - TC-CHK-010: Keyboard Positioning Over CVV (BUG-017)

    /// TC-CHK-010: Ensure software keyboard does not obscure CVV input during entry.
    /// Category: Edge (Regression: BUG-017)
    /// Runs on: Fixed build only (Blocked by BUG-011 on broken build).
    /// Catches BUG-017 where CVV and submit button were permanently obscured by keyboard on broken build.
    func test_tc_chk_010_ensure_keyboard_does_not_obscure_cvv() {
        navigateToCheckout()

        let cvvField = el("checkout-cvv")
        guard cvvField.waitForExistence(timeout: 5.0) else {
            XCTFail("Blocked by BUG-011: Checkout screen did not open")
            return
        }

        cvvField.tap()
        cvvField.typeText("123")

        let submitBtn = el("checkout-submit")
        XCTAssertTrue(
            submitBtn.waitForExistence(timeout: 3.0),
            "BUG-017: Checkout submit button obscured or not interactable after focusing CVV"
        )
    }
}
