import pytest
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from flows import login_as_standard_user


def test_tc_log_001_authenticate_successfully_with_valid_credentials(driver, test_credentials):
    """
    TC-LOG-001: Authenticate successfully with valid credentials.
    Category: Positive
    Steps:
      1. Enter valid email (from env: TEST_EMAIL)
      2. Enter valid password (from env: TEST_PASSWORD)
      3. Tap 'Log In' button (located by label 'Log In')
    Expected Result:
      Navigates to Product Catalog screen; product list is visible; no error displayed.
    """
    login_page = LoginPage(driver)
    login_page.enter_email(test_credentials["email"])
    login_page.enter_password(test_credentials["password"])
    login_page.tap_login_button()

    catalog_page = CatalogPage(driver)
    assert catalog_page.is_loaded(timeout=5), "Expected Product Catalog to be loaded after valid login"
    assert catalog_page.has_product("p1"), "Expected catalog product 'product-name-p1' to be visible"
    assert not login_page.is_error_displayed(timeout=1), "Expected no error message on successful login"


def test_tc_log_002_reject_login_submission_with_empty_email_and_password(driver):
    """
    TC-LOG-002: Reject login submission with empty email and password.
    Category: Negative (Regression: BUG-002)
    Steps:
      1. Leave login-email and login-password empty
      2. Tap 'Log In' button
    Expected Result:
      User remains on Login screen; error message 'Email and password are required' is displayed;
      navigation to catalog is blocked.
    """
    login_page = LoginPage(driver)
    login_page.tap_login_button()

    assert login_page.is_error_displayed(timeout=3), "Expected error message displayed for empty submission"
    assert login_page.get_error_message() == "Email and password are required", (
        f"Expected 'Email and password are required', got '{login_page.get_error_message()}'"
    )
    catalog_page = CatalogPage(driver)
    assert not catalog_page.is_loaded(timeout=1), "Navigation should be blocked on empty credentials"


def test_tc_log_003_reject_login_submission_when_password_is_missing(driver, test_credentials):
    """
    TC-LOG-003: Reject login submission when password field is missing.
    Category: Negative (Regression: BUG-002)
    Steps:
      1. Enter valid email
      2. Leave login-password empty
      3. Tap 'Log In' button
    Expected Result:
      User remains on Login screen; error message 'Email and password are required' is displayed;
      navigation is blocked.
    """
    login_page = LoginPage(driver)
    login_page.enter_email(test_credentials["email"])
    login_page.tap_login_button()

    assert login_page.is_error_displayed(timeout=3), "Expected error message displayed when password is missing"
    assert login_page.get_error_message() == "Email and password are required", (
        f"Expected 'Email and password are required', got '{login_page.get_error_message()}'"
    )
    catalog_page = CatalogPage(driver)
    assert not catalog_page.is_loaded(timeout=1), "Navigation should be blocked when password is missing"


def test_tc_log_004_reject_login_with_malformed_email_format(driver, test_credentials):
    """
    TC-LOG-004: Reject login with malformed email format.
    Category: Negative (Requirement: L2)
    Steps:
      1. Enter malformed email 'invalidemail'
      2. Enter valid password
      3. Tap 'Log In' button
    Expected Result:
      User remains on Login screen; error message 'Enter a valid email address' is displayed;
      navigation is blocked.
    """
    login_page = LoginPage(driver)
    login_page.enter_email("invalidemail")
    login_page.enter_password(test_credentials["password"])
    login_page.tap_login_button()

    assert login_page.is_error_displayed(timeout=3), "Expected error message displayed for invalid email format"
    assert login_page.get_error_message() == "Enter a valid email address", (
        f"Expected 'Enter a valid email address', got '{login_page.get_error_message()}'"
    )
    catalog_page = CatalogPage(driver)
    assert not catalog_page.is_loaded(timeout=1), "Navigation should be blocked for invalid email format"


def test_tc_log_005_reject_login_with_incorrect_password(driver, test_credentials):
    """
    TC-LOG-005: Reject login with incorrect password.
    Category: Negative (Regression: BUG-003)
    Steps:
      1. Enter valid email
      2. Enter incorrect password 'wrongpassword'
      3. Tap 'Log In' button
    Expected Result:
      User remains on Login screen; error message 'Invalid email or password' is displayed;
      navigation to catalog is blocked.
    """
    login_page = LoginPage(driver)
    login_page.enter_email(test_credentials["email"])
    login_page.enter_password("wrongpassword")
    login_page.tap_login_button()

    assert login_page.is_error_displayed(timeout=3), "Expected error message displayed for incorrect password"
    assert login_page.get_error_message() == "Invalid email or password", (
        f"Expected 'Invalid email or password', got '{login_page.get_error_message()}'"
    )
    catalog_page = CatalogPage(driver)
    assert not catalog_page.is_loaded(timeout=1), "Navigation should be blocked for incorrect password"


def test_tc_log_006_reject_login_with_unregistered_email(driver, test_credentials):
    """
    TC-LOG-006: Reject login with unregistered email.
    Category: Negative (Regression: BUG-003)
    Steps:
      1. Enter unregistered email 'unregistered@techshop.com'
      2. Enter valid password
      3. Tap 'Log In' button
    Expected Result:
      User remains on Login screen; error message 'Invalid email or password' is displayed;
      navigation is blocked.
    """
    login_page = LoginPage(driver)
    login_page.enter_email("unregistered@techshop.com")
    login_page.enter_password(test_credentials["password"])
    login_page.tap_login_button()

    assert login_page.is_error_displayed(timeout=3), "Expected error message displayed for unregistered email"
    assert login_page.get_error_message() == "Invalid email or password", (
        f"Expected 'Invalid email or password', got '{login_page.get_error_message()}'"
    )
    catalog_page = CatalogPage(driver)
    assert not catalog_page.is_loaded(timeout=1), "Navigation should be blocked for unregistered email"


def test_tc_log_007_password_field_is_secure(driver):
    """
    TC-LOG-007 / BUG-001: Password input characters must use secure text entry.
    Category: Edge / Attribute Assertion
    Steps:
      1. Inspect element 'type' attribute of 'login-password'
    Expected Result:
      Element type must be 'XCUIElementTypeSecureTextField', not 'XCUIElementTypeTextField'.
      Catches BUG-001 where plain TextField was used in the broken build.
    """
    login_page = LoginPage(driver)
    field_type = login_page.get_password_field_type()
    assert field_type != "XCUIElementTypeTextField", (
        "BUG-001: Password field is a plain XCUIElementTypeTextField (shows plaintext)"
    )
    assert field_type == "XCUIElementTypeSecureTextField", (
        f"Expected 'XCUIElementTypeSecureTextField', got '{field_type}' (BUG-001)"
    )


def test_tc_log_008_ensure_tab_bar_hidden_while_unauthenticated(driver):
    """
    TC-LOG-008: Ensure tab bar navigation is hidden while unauthenticated.
    Category: Edge (Regression: BUG-015)
    Steps:
      1. Inspect bottom area of screen on fresh launch before authentication
      2. Attempt to locate Products or Cart tabs
    Expected Result:
      Tab bar (Products and Cart tabs) is hidden and inaccessible prior to authentication.
    """
    login_page = LoginPage(driver)
    assert not login_page.is_tab_bar_visible(), (
        "Expected tab bar navigation (Products/Cart tabs) to be hidden prior to authentication (BUG-015)"
    )


def test_tc_log_009_retain_authenticated_session_across_app_backgrounding(driver, test_credentials):
    """
    TC-LOG-009: Retain authenticated session across app backgrounding.
    Category: Edge (Requirement: L8)
    Steps:
      1. Authenticate with valid credentials to reach Catalog screen
      2. Send app to background for 5 seconds
      3. Restore app to foreground
    Expected Result:
      App restores state on Catalog screen without redirecting back to Login screen.
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    assert catalog_page.is_loaded(timeout=10), "Expected to be on catalog screen before backgrounding"

    catalog_page.background_app(seconds=5)

    assert catalog_page.is_loaded(timeout=10), "Expected user session to be retained on catalog after backgrounding"


def test_login_button_has_stable_id(driver):
    """
    BUG-016: Verify Login button has a stable accessibility identifier ('login-submit').
    Category: Testability Defect (Regression: BUG-016)
    Steps:
      1. Check if element with accessibility identifier 'login-submit' exists
    Expected Result:
      Element with ID 'login-submit' must exist on the Login screen.
      Catches BUG-016 where the login button lacks an accessibility identifier.
    """
    login_page = LoginPage(driver)
    assert login_page.has_login_submit_id(), (
        "BUG-016: Login button lacks accessibilityIdentifier 'login-submit'"
    )
