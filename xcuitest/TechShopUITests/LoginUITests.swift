import XCTest

/// Login test suite covering all authentication test cases and planted bug regressions
/// defined in the TechShop Test Case Matrix (test-cases.md).
final class LoginUITests: TechShopUITestCase {

    // MARK: - TC-LOG-001: Valid Authentication

    /// TC-LOG-001: Authenticate successfully with valid credentials.
    /// Category: Positive
    func test_tc_log_001_authenticate_successfully_with_valid_credentials() {
        let emailField = el("login-email")
        XCTAssertTrue(emailField.waitForExistence(timeout: 5.0), "Expected login-email field to exist")
        emailField.tap()
        emailField.typeText(testEmail)

        let passField = passwordField()
        XCTAssertTrue(passField.waitForExistence(timeout: 5.0), "Expected login-password field to exist")
        passField.tap()
        passField.typeText(testPassword)

        let loginButton = app.buttons["Log In"]
        XCTAssertTrue(loginButton.waitForExistence(timeout: 5.0), "Expected 'Log In' button to exist")
        loginButton.tap()

        let firstProduct = el("product-name-p1")
        XCTAssertTrue(firstProduct.waitForExistence(timeout: 5.0), "Expected catalog screen with product 'p1' to be displayed")
        XCTAssertFalse(el("login-error").exists, "Expected no error message on successful login")
    }

    // MARK: - TC-LOG-002: Empty Credentials Submission

    /// TC-LOG-002: Reject login submission with empty email and password.
    /// Category: Negative (Regression: BUG-002)
    func test_tc_log_002_reject_login_submission_with_empty_email_and_password() {
        let loginButton = app.buttons["Log In"]
        XCTAssertTrue(loginButton.waitForExistence(timeout: 5.0), "Expected 'Log In' button to exist")
        loginButton.tap()

        let errorElement = el("login-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected error message displayed for empty submission (BUG-002)")
        XCTAssertEqual(errorElement.label, "Email and password are required", "Expected 'Email and password are required' error message")
        XCTAssertFalse(el("product-name-p1").exists, "Navigation should be blocked on empty credentials")
    }

    // MARK: - TC-LOG-003: Missing Password Submission

    /// TC-LOG-003: Reject login submission when password field is missing.
    /// Category: Negative (Regression: BUG-002)
    func test_tc_log_003_reject_login_submission_when_password_is_missing() {
        let emailField = el("login-email")
        XCTAssertTrue(emailField.waitForExistence(timeout: 5.0), "Expected login-email field to exist")
        emailField.tap()
        emailField.typeText(testEmail)

        let loginButton = app.buttons["Log In"]
        XCTAssertTrue(loginButton.waitForExistence(timeout: 5.0), "Expected 'Log In' button to exist")
        loginButton.tap()

        let errorElement = el("login-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected error message displayed when password is missing (BUG-002)")
        XCTAssertEqual(errorElement.label, "Email and password are required", "Expected 'Email and password are required' error message")
        XCTAssertFalse(el("product-name-p1").exists, "Navigation should be blocked when password is missing")
    }

    // MARK: - TC-LOG-004: Malformed Email Format

    /// TC-LOG-004: Reject login with malformed email format.
    /// Category: Negative (Requirement: L2)
    func test_tc_log_004_reject_login_with_malformed_email_format() {
        let emailField = el("login-email")
        XCTAssertTrue(emailField.waitForExistence(timeout: 5.0), "Expected login-email field to exist")
        emailField.tap()
        emailField.typeText("invalidemail")

        let passField = passwordField()
        XCTAssertTrue(passField.waitForExistence(timeout: 5.0), "Expected login-password field to exist")
        passField.tap()
        passField.typeText(testPassword)

        let loginButton = app.buttons["Log In"]
        XCTAssertTrue(loginButton.waitForExistence(timeout: 5.0), "Expected 'Log In' button to exist")
        loginButton.tap()

        let errorElement = el("login-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected error message displayed for invalid email format")
        XCTAssertEqual(errorElement.label, "Enter a valid email address", "Expected 'Enter a valid email address' error message")
        XCTAssertFalse(el("product-name-p1").exists, "Navigation should be blocked for invalid email format")
    }

    // MARK: - TC-LOG-005: Incorrect Password

    /// TC-LOG-005: Reject login with incorrect password.
    /// Category: Negative (Regression: BUG-003)
    func test_tc_log_005_reject_login_with_incorrect_password() {
        let emailField = el("login-email")
        XCTAssertTrue(emailField.waitForExistence(timeout: 5.0), "Expected login-email field to exist")
        emailField.tap()
        emailField.typeText(testEmail)

        let passField = passwordField()
        XCTAssertTrue(passField.waitForExistence(timeout: 5.0), "Expected login-password field to exist")
        passField.tap()
        passField.typeText("wrongpassword")

        let loginButton = app.buttons["Log In"]
        XCTAssertTrue(loginButton.waitForExistence(timeout: 5.0), "Expected 'Log In' button to exist")
        loginButton.tap()

        let errorElement = el("login-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected error message displayed for incorrect password (BUG-003)")
        XCTAssertEqual(errorElement.label, "Invalid email or password", "Expected 'Invalid email or password' error message")
        XCTAssertFalse(el("product-name-p1").exists, "Navigation should be blocked for incorrect password")
    }

    // MARK: - TC-LOG-006: Unregistered Email

    /// TC-LOG-006: Reject login with unregistered email.
    /// Category: Negative (Regression: BUG-003)
    func test_tc_log_006_reject_login_with_unregistered_email() {
        let emailField = el("login-email")
        XCTAssertTrue(emailField.waitForExistence(timeout: 5.0), "Expected login-email field to exist")
        emailField.tap()
        emailField.typeText("unregistered@techshop.com")

        let passField = passwordField()
        XCTAssertTrue(passField.waitForExistence(timeout: 5.0), "Expected login-password field to exist")
        passField.tap()
        passField.typeText(testPassword)

        let loginButton = app.buttons["Log In"]
        XCTAssertTrue(loginButton.waitForExistence(timeout: 5.0), "Expected 'Log In' button to exist")
        loginButton.tap()

        let errorElement = el("login-error")
        XCTAssertTrue(errorElement.waitForExistence(timeout: 3.0), "Expected error message displayed for unregistered email (BUG-003)")
        XCTAssertEqual(errorElement.label, "Invalid email or password", "Expected 'Invalid email or password' error message")
        XCTAssertFalse(el("product-name-p1").exists, "Navigation should be blocked for unregistered email")
    }

    // MARK: - TC-LOG-007: Password Masking (BUG-001)

    /// TC-LOG-007 / BUG-001: Mask password input characters with secure text entry.
    /// Category: Edge / Attribute Assertion (Appium / XCUITest only)
    func test_tc_log_007_password_field_is_secure() {
        // Maestro cannot assert secure-entry masking. XCUITest inspects native accessibility element types.
        XCTAssertFalse(
            app.textFields["login-password"].exists,
            "BUG-001: Password field is rendered as a plain TextField (unmasked plaintext)"
        )
        XCTAssertTrue(
            app.secureTextFields["login-password"].exists,
            "BUG-001: Expected password field to be an XCUIElementTypeSecureTextField with secureTextEntry enabled"
        )
    }

    // MARK: - TC-LOG-008: Tab Bar Hidden Before Auth (BUG-015)

    /// TC-LOG-008: Ensure tab bar navigation is hidden while unauthenticated.
    /// Category: Edge (Regression: BUG-015)
    func test_tc_log_008_ensure_tab_bar_hidden_while_unauthenticated() {
        // Tab bar (Products and Cart tabs) must not be rendered or accessible on the unauthenticated login screen
        XCTAssertFalse(
            app.tabBars.buttons["Products"].exists || app.buttons["Products"].exists,
            "BUG-015: Products tab is visible before authentication"
        )
        XCTAssertFalse(
            app.tabBars.buttons["Cart"].exists || app.buttons["Cart"].exists,
            "BUG-015: Cart tab is visible before authentication"
        )
    }

    // MARK: - TC-LOG-009: Session Retention Across Backgrounding

    /// TC-LOG-009: Retain authenticated session across app backgrounding.
    /// Category: Edge (Requirement: L8)
    func test_tc_log_009_retain_authenticated_session_across_app_backgrounding() {
        login()

        let firstProduct = el("product-name-p1")
        XCTAssertTrue(firstProduct.waitForExistence(timeout: 5.0), "Expected to be on catalog screen before backgrounding")

        // Send app to background
        XCUIDevice.shared.press(XCUIDevice.Button.home)
        
        // Wait in background
        _ = XCTWaiter.wait(for: [XCTestExpectation(description: "background_delay")], timeout: 3.0)

        // Foreground the app
        app.activate()

        // Verify user remains on the catalog screen
        XCTAssertTrue(firstProduct.waitForExistence(timeout: 5.0), "Expected user session to be retained on catalog after backgrounding")
    }

    // MARK: - BUG-016: Login Button Accessibility Identifier

    /// BUG-016: Verify Login button has a stable accessibility identifier ('login-submit').
    /// Category: Testability Defect (Regression: BUG-016)
    func test_tc_log_016_login_button_has_accessibility_identifier() {
        // Catches BUG-016 where the login submit button lacks accessibilityIdentifier "login-submit"
        XCTAssertTrue(
            el("login-submit").exists || app.buttons["login-submit"].exists,
            "BUG-016: Login button lacks accessibilityIdentifier 'login-submit'"
        )
    }
}
