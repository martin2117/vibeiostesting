import XCTest

/// Base XCTestCase for TechShop UI tests providing cross-framework helpers,
/// environment-based credentials, and standard setup/teardown flows.
class TechShopUITestCase: XCTestCase {
    var app: XCUIApplication!

    /// Test user email sourced from environment variable TEST_EMAIL, defaulting to demo credential.
    var testEmail: String {
        ProcessInfo.processInfo.environment["TEST_EMAIL"] ?? "demo@techshop.com"
    }

    /// Test user password sourced from environment variable TEST_PASSWORD, defaulting to demo credential.
    var testPassword: String {
        ProcessInfo.processInfo.environment["TEST_PASSWORD"] ?? "password123"
    }

    override func setUpWithError() throws {
        try super.setUpWithError()
        continueAfterFailure = false
        app = XCUIApplication(bundleIdentifier: "com.techshop.ios")
        app.launch()
    }

    override func tearDownWithError() throws {
        app = nil
        try super.tearDownWithError()
    }

    /// Framework-agnostic element lookup via descendants(matching: .any) using accessibility identifier.
    /// Survives element type differences between native SwiftUI and React Native builds.
    func el(_ id: String) -> XCUIElement {
        app.descendants(matching: .any)[id]
    }

    /// Checks if a given text exists on screen within the specified timeout.
    func hasText(_ text: String, timeout: TimeInterval = 5.0) -> Bool {
        let element = app.descendants(matching: .any)[text]
        if element.waitForExistence(timeout: timeout) {
            return true
        }
        let predicate = NSPredicate(format: "label CONTAINS[c] %@ OR value CONTAINS[c] %@", text, text)
        return app.descendants(matching: .any).matching(predicate).firstMatch.waitForExistence(timeout: 1.0)
    }

    /// Returns the password field whether rendered as a SecureTextField or plain TextField.
    func passwordField() -> XCUIElement {
        let secureField = app.secureTextFields["login-password"]
        if secureField.exists {
            return secureField
        }
        let plainField = app.textFields["login-password"]
        if plainField.exists {
            return plainField
        }
        return el("login-password")
    }

    /// Logs into TechShop using valid or provided credentials. Locates login button by label "Log In".
    func login(email: String? = nil, password: String? = nil) {
        let userEmail = email ?? testEmail
        let userPassword = password ?? testPassword

        let emailField = el("login-email")
        if emailField.waitForExistence(timeout: 5.0) {
            emailField.tap()
            emailField.typeText(userEmail)
        }

        let passField = passwordField()
        if passField.waitForExistence(timeout: 5.0) {
            passField.tap()
            passField.typeText(userPassword)
        }

        // Locate login button via stable ID 'login-submit' with fallback to label 'Log In' (BUG-016 cross-build compatibility)
        let loginSubmit = el("login-submit")
        if loginSubmit.waitForExistence(timeout: 2.0) {
            loginSubmit.tap()
        } else {
            let loginButton = app.buttons["Log In"]
            if loginButton.waitForExistence(timeout: 5.0) {
                loginButton.tap()
            }
        }
    }

    /// Adds the first catalog item (p1) to cart and opens the Cart screen.
    func addItemAndOpenCart() {
        if el("login-email").exists {
            login()
        }

        let addButton = el("add-p1")
        XCTAssertTrue(addButton.waitForExistence(timeout: 5.0), "Expected Add button for product p1 to exist")
        addButton.tap()

        let cartTab = app.buttons["Cart"]
        if cartTab.waitForExistence(timeout: 5.0) {
            cartTab.tap()
        } else {
            let cartById = el("cart")
            if cartById.waitForExistence(timeout: 5.0) {
                cartById.tap()
            }
        }

        // Wait for Cart screen transition to settle
        _ = el("order-total").waitForExistence(timeout: 3.0) || el("cart-empty").waitForExistence(timeout: 3.0)
    }
}
