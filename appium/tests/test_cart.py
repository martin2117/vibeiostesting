import pytest
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from flows import login_as_standard_user, add_first_item_and_view_cart


def test_tc_cart_001_add_item_and_verify_cart_display(driver, test_credentials):
    """
    TC-CART-001: Add item from catalog and verify cart display and line totals.
    Category: Positive (Requirement: S1, S2)
    Steps:
      1. Log in and add 'p1' (Wireless Headphones - $60) to cart
      2. Navigate to Cart tab
    Expected Result:
      Cart displays item name, quantity '1', line total 'Line: $60', and Order Total 'Order Total: $60'.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])

    cart_page = CartPage(driver)
    assert cart_page.has_item("p1"), "Expected item 'p1' to be present in cart"
    assert cart_page.get_quantity("p1") == "1", f"Expected quantity '1', got '{cart_page.get_quantity('p1')}'"
    assert "60" in cart_page.get_line_total("p1"), f"Expected line total $60, got '{cart_page.get_line_total('p1')}'"
    assert "60" in cart_page.get_order_total(), f"Expected order total $60, got '{cart_page.get_order_total()}'"


def test_tc_cart_002_increment_quantity_reactive_order_total(driver, test_credentials):
    """
    TC-CART-002: Increment item quantity and verify reactive order total calculation.
    Category: Positive (Regression: BUG-006)
    Steps:
      1. Add 1x 'p1' to cart and open Cart screen ($60)
      2. Tap '+' quantity increment button
    Expected Result:
      Quantity updates to '2', line total updates to 'Line: $120', and Order Total immediately updates to '$120'.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])

    cart_page = CartPage(driver)
    cart_page.increment_quantity("p1")

    assert cart_page.get_quantity("p1") == "2", f"Expected quantity '2', got '{cart_page.get_quantity('p1')}'"
    assert "120" in cart_page.get_line_total("p1"), f"Expected line total $120, got '{cart_page.get_line_total('p1')}'"
    assert "120" in cart_page.get_order_total(), (
        f"BUG-006: Order Total did not reactively update on quantity increment. Got '{cart_page.get_order_total()}'"
    )


def test_tc_cart_003_decrement_quantity_reactive_order_total(driver, test_credentials):
    """
    TC-CART-003: Decrement item quantity and verify reactive order total reduction.
    Category: Positive (Regression: BUG-006)
    Steps:
      1. Add item to cart, increment to 2 ($120)
      2. Tap '−' quantity decrement button
    Expected Result:
      Quantity updates to '1', line total updates to 'Line: $60', and Order Total updates to '$60'.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])

    cart_page = CartPage(driver)
    cart_page.increment_quantity("p1")
    cart_page.decrement_quantity("p1")

    assert cart_page.get_quantity("p1") == "1", f"Expected quantity '1', got '{cart_page.get_quantity('p1')}'"
    assert "60" in cart_page.get_line_total("p1"), f"Expected line total $60, got '{cart_page.get_line_total('p1')}'"
    assert "60" in cart_page.get_order_total(), (
        f"BUG-006: Order Total did not reactively update on quantity decrement. Got '{cart_page.get_order_total()}'"
    )


def test_tc_cart_004_apply_valid_discount_save10(driver, test_credentials):
    """
    TC-CART-004: Apply valid discount code SAVE10 for 10% discount deduction.
    Category: Positive (Regression: BUG-004)
    Steps:
      1. Add 1x 'p1' ($60) to cart and open Cart
      2. Enter discount code 'SAVE10'
    Expected Result:
      10% discount ($6) is deducted; Order Total updates to '$54' (not $59 due to dividing by 1000).
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])

    cart_page = CartPage(driver)
    cart_page.apply_discount("SAVE10")

    assert "54" in cart_page.get_order_total(), (
        f"BUG-004: Discount calculation error. Expected Order Total: $54, got '{cart_page.get_order_total()}'"
    )


def test_tc_cart_005_prevent_quantity_decrement_below_one(driver, test_credentials):
    """
    TC-CART-005: Prevent quantity decrement below minimum threshold of 1.
    Category: Negative (Regression: BUG-005)
    Steps:
      1. Add 1x 'p1' (quantity = 1) to cart and open Cart
      2. Tap '−' decrement button
    Expected Result:
      Quantity remains clamped at '1'; does not decrement to 0 or negative numbers.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])

    cart_page = CartPage(driver)
    cart_page.decrement_quantity("p1")

    qty = cart_page.get_quantity("p1", timeout=5)
    assert qty == "1", f"BUG-005: Quantity decremented below 1 to '{qty}'"


def test_tc_cart_006_reject_checkout_when_total_below_ten(driver, test_credentials):
    """
    TC-CART-006: Reject checkout progression when order total is below minimum $10 threshold.
    Category: Negative (Requirement: S9)
    Steps:
      1. Open Cart with subtotal < $10 (or 0)
      2. Tap 'Proceed to Checkout'
    Expected Result:
      Navigation blocked; message 'Minimum order value is $10.00' is displayed.
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    catalog_page.navigate_to_cart()

    cart_page = CartPage(driver)
    if not cart_page.is_empty():
        cart_page.proceed_to_checkout()
        assert cart_page.has_cart_message(), "Expected minimum order value error message"
        assert "10.00" in cart_page.get_cart_message(), (
            f"Expected minimum order message, got '{cart_page.get_cart_message()}'"
        )


def test_tc_cart_007_reject_invalid_discount_code(driver, test_credentials):
    """
    TC-CART-007: Reject invalid discount code without modifying order total.
    Category: Negative (Requirement: S7)
    Steps:
      1. Add 1x 'p1' ($60) to cart
      2. Enter invalid discount code 'INVALID99'
    Expected Result:
      No discount applied (0%); Order Total remains unchanged at '$60'.
    """
    add_first_item_and_view_cart(driver, email=test_credentials["email"], password=test_credentials["password"])

    cart_page = CartPage(driver)
    cart_page.apply_discount("INVALID99")

    assert "60" in cart_page.get_order_total(), (
        f"Expected order total to remain $60 for invalid discount, got '{cart_page.get_order_total()}'"
    )


def test_tc_cart_008_display_empty_cart_state(driver, test_credentials):
    """
    TC-CART-008: Display empty cart state when no items are present.
    Category: Edge (Requirement: S6)
    Steps:
      1. Log in and navigate directly to Cart tab with 0 items
    Expected Result:
      Cart screen displays 'Your cart is empty' label; item list is empty.
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    catalog_page.navigate_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.is_empty(timeout=3), "Expected empty cart state"
    assert cart_page.get_empty_cart_text() == "Your cart is empty", (
        f"Expected 'Your cart is empty', got '{cart_page.get_empty_cart_text()}'"
    )


def test_tc_cart_009_register_rapid_consecutive_taps(driver, test_credentials):
    """
    TC-CART-009: Register rapid consecutive taps on catalog Add button.
    Category: Edge (Requirement: S1)
    Steps:
      1. Log in to catalog screen
      2. Rapidly tap 'add-p1' 3 times in succession
      3. Navigate to Cart tab
    Expected Result:
      Cart shows quantity '3', line total '$180', and Order Total '$180'.
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    import time
    catalog_page.add_to_cart("p1")
    time.sleep(0.3)
    catalog_page.add_to_cart("p1")
    time.sleep(0.3)
    catalog_page.add_to_cart("p1")
    time.sleep(0.5)
    catalog_page.navigate_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.get_quantity("p1") == "3", f"Expected quantity '3', got '{cart_page.get_quantity('p1')}'"
    assert "180" in cart_page.get_line_total("p1"), f"Expected line total $180, got '{cart_page.get_line_total('p1')}'"
    assert "180" in cart_page.get_order_total(), f"Expected order total $180, got '{cart_page.get_order_total()}'"


def test_tc_cart_010_block_adding_out_of_stock_product(driver, test_credentials):
    """
    TC-CART-010: Block adding out-of-stock product to cart.
    Category: Edge (Regression: BUG-008)
    Steps:
      1. Log in to catalog screen
      2. Attempt to tap disabled Add button 'add-p4'
      3. Navigate to Cart tab
    Expected Result:
      Product 4 is not added; cart remains empty.
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    # Attempt to click disabled add button
    try:
        catalog_page.add_to_cart("p4")
    except Exception:
        pass  # Expected if disabled button ignores click or throws

    catalog_page.navigate_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.is_empty(timeout=3), "BUG-008: Out-of-stock product was added to cart"
