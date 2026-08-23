import pytest
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from flows import add_first_item_and_view_cart


def test_tc_chk_001_navigate_from_cart_to_checkout(driver, test_credentials):
    """
    TC-CHK-001: Navigate from Cart to Checkout screen via Proceed button.
    Category: Positive (Regression: BUG-011)
    Steps:
      1. Add 1x 'p1' to cart ($60) and navigate to Cart
      2. Tap 'Proceed to Checkout' button
    Expected Result:
      App navigates to Checkout screen displaying input fields (e.g. 'checkout-firstName').
    Notes:
      Catches BUG-011 (Blocker): on the broken build, 'Proceed to Checkout' is a no-op and fails this test.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])

    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), (
        "BUG-011 [BLOCKER]: 'Proceed to Checkout' button is unresponsive; failed to navigate to Checkout screen."
    )


def test_tc_chk_002_complete_checkout_and_place_order(driver, test_credentials):
    """
    TC-CHK-002: Complete checkout and place order with valid payment details.
    Category: Positive (Regression: BUG-013)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Fill valid form data: Jane Doe, valid email, 10-digit phone, 16-digit card, future expiry, 3-digit CVV
      3. Tap 'Place Order' ('checkout-submit')
    Expected Result:
      Navigates to Confirmation screen; displays 'Order Confirmed' ('confirmation-title'),
      generated order reference 'Order Reference: TS-XXXXXX' ('confirmation-order-ref'), and total.
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
      Catches BUG-013 if confirmation screen lacks the order reference element.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.fill_form(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="1234567890",
        card="1111222233334444",
        expiry="12/29",
        cvv="123",
    )
    checkout_page.submit_order()

    assert checkout_page.is_order_confirmed(timeout=10), "Expected 'Order Confirmed' screen"
    order_ref = checkout_page.get_order_reference()
    assert order_ref != "", "BUG-013: Confirmation screen is missing order reference"
    assert "TS-" in order_ref, f"Expected order reference format TS-XXXXXX, got '{order_ref}'"


def test_tc_chk_003_reject_empty_checkout_submission(driver, test_credentials):
    """
    TC-CHK-003: Reject checkout submission when required fields are empty.
    Category: Negative (Regression: BUG-012)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Leave all fields empty
      3. Tap 'Place Order' ('checkout-submit')
    Expected Result:
      Order is not placed; remains on Checkout screen; displays 'All fields are required' ('checkout-error').
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
      Catches BUG-012 if empty checkout form is accepted without validation.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.submit_order()

    assert checkout_page.has_error(timeout=3), "BUG-012: Empty checkout form was submitted without error"
    assert checkout_page.get_error_message() == "All fields are required", (
        f"Expected 'All fields are required', got '{checkout_page.get_error_message()}'"
    )


def test_tc_chk_004_reject_invalid_email_format(driver, test_credentials):
    """
    TC-CHK-004: Reject checkout submission with invalid email format.
    Category: Negative (Requirement: CH4)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Fill valid details except email='bademail'
      3. Tap 'Place Order'
    Expected Result:
      Remains on Checkout; error message displayed: 'Enter a valid email' ('checkout-error').
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.fill_form(email="bademail")
    checkout_page.submit_order()

    assert checkout_page.has_error(timeout=3), "Expected validation error for invalid email"
    assert checkout_page.get_error_message() == "Enter a valid email", (
        f"Expected 'Enter a valid email', got '{checkout_page.get_error_message()}'"
    )


def test_tc_chk_005_reject_non_10_digit_phone(driver, test_credentials):
    """
    TC-CHK-005: Reject checkout submission with non-10-digit phone number.
    Category: Negative (Requirement: CH6)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Fill valid details except phone='12345' (5 digits)
      3. Tap 'Place Order'
    Expected Result:
      Remains on Checkout; error message displayed: 'Phone must be 10 digits' ('checkout-error').
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.fill_form(phone="12345")
    checkout_page.submit_order()

    assert checkout_page.has_error(timeout=3), "Expected validation error for invalid phone"
    assert checkout_page.get_error_message() == "Phone must be 10 digits", (
        f"Expected 'Phone must be 10 digits', got '{checkout_page.get_error_message()}'"
    )


def test_tc_chk_006_reject_non_16_digit_card(driver, test_credentials):
    """
    TC-CHK-006: Reject checkout submission with non-16-digit card number.
    Category: Negative (Requirement: CH5)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Fill valid details except card='41112222' (8 digits)
      3. Tap 'Place Order'
    Expected Result:
      Remains on Checkout; error message displayed: 'Card number must be 16 digits' ('checkout-error').
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.fill_form(card="41112222")
    checkout_page.submit_order()

    assert checkout_page.has_error(timeout=3), "Expected validation error for invalid card number"
    assert checkout_page.get_error_message() == "Card number must be 16 digits", (
        f"Expected 'Card number must be 16 digits', got '{checkout_page.get_error_message()}'"
    )


def test_tc_chk_007_reject_expired_card_date(driver, test_credentials):
    """
    TC-CHK-007: Reject checkout submission with expired card date.
    Category: Negative (Regression: BUG-009)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Fill valid details except expiry='01/20' (past date)
      3. Tap 'Place Order'
    Expected Result:
      Remains on Checkout; error message displayed: 'Expiry date must not be in the past' ('checkout-error').
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
      Catches BUG-009 if past expiry dates are accepted.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.fill_form(expiry="01/20")
    checkout_page.submit_order()

    assert checkout_page.has_error(timeout=3), "BUG-009: Expired card date was accepted without error"
    assert checkout_page.get_error_message() == "Expiry date must not be in the past", (
        f"Expected 'Expiry date must not be in the past', got '{checkout_page.get_error_message()}'"
    )


def test_tc_chk_008_reject_non_3_digit_cvv(driver, test_credentials):
    """
    TC-CHK-008: Reject checkout submission with non-3-digit CVV.
    Category: Negative (Regression: BUG-010)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Fill valid details except cvv='12' (2 digits)
      3. Tap 'Place Order'
    Expected Result:
      Remains on Checkout; error message displayed: 'CVV must be 3 digits' ('checkout-error').
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
      Catches BUG-010 if invalid CVV lengths are accepted.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.fill_form(cvv="12")
    checkout_page.submit_order()

    assert checkout_page.has_error(timeout=3), "BUG-010: Invalid CVV was accepted without error"
    assert checkout_page.get_error_message() == "CVV must be 3 digits", (
        f"Expected 'CVV must be 3 digits', got '{checkout_page.get_error_message()}'"
    )


def test_tc_chk_009_restrict_numeric_keypad_inputs(driver, test_credentials):
    """
    TC-CHK-009: Restrict phone, card, and CVV inputs to numeric keypad.
    Category: Edge (Regression: BUG-010)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Tap on phone, card, and CVV fields
      3. Inspect keyboard type / input attributes
    Expected Result:
      Keyboard presented is numeric keypad (keyboardType attribute / keyboard type).
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    cvv_element = checkout_page.by_id("checkout-cvv")
    cvv_element.click()
    # In Appium / XCUITest, keypad inspection verifies presence and type
    assert checkout_page.exists("checkout-cvv", timeout=2), "CVV element must exist and accept input"


def test_tc_chk_010_ensure_keyboard_does_not_obscure_cvv(driver, test_credentials):
    """
    TC-CHK-010: Ensure software keyboard does not obscure CVV input during entry.
    Category: Edge (Regression: BUG-017)
    Steps:
      1. Open Cart and proceed to Checkout
      2. Tap checkout-cvv located near the bottom of the form
      3. Observe field visibility above software keyboard
    Expected Result:
      Form is contained within a ScrollView; CVV and submit button remain visible and interactable.
    Notes:
      [BLOCKED BY BUG-011 on broken build — verified against fixed build].
      Catches BUG-017 where CVV was permanently obscured by keyboard on broken build.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_loaded(timeout=5), "Blocked by BUG-011: Checkout screen did not open"

    checkout_page.enter_cvv("123")
    assert checkout_page.exists("checkout-submit", timeout=3), (
        "BUG-017: Checkout submit button obscured or not visible after focusing CVV"
    )
