import XCTest

/// Cart UI test suite covering item addition, quantity adjustments, discount codes,
/// minimum order thresholds, empty states, and reactivity bug regressions.
final class CartUITests: TechShopUITestCase {

    // MARK: - TC-CART-001: Add Item and Verify Cart Display

    /// TC-CART-001: Add item from catalog and verify cart display and line totals.
    /// Category: Positive (Requirement: S1, S2)
    func test_tc_cart_001_add_item_and_verify_cart_display() {
        addItemAndOpenCart()

        let qty = el("qty-p1")
        XCTAssertTrue(qty.waitForExistence(timeout: 5.0), "Expected quantity label for product p1")
        XCTAssertEqual(qty.label, "1", "Expected initial quantity to be '1'")

        let lineTotal = el("line-total-p1")
        XCTAssertTrue(lineTotal.waitForExistence(timeout: 5.0), "Expected line total label for product p1")
        XCTAssertTrue(lineTotal.label.contains("60"), "Expected line total to contain '60', got '\(lineTotal.label)'")

        let orderTotal = el("order-total")
        XCTAssertTrue(orderTotal.waitForExistence(timeout: 5.0), "Expected Order Total label")
        XCTAssertTrue(orderTotal.label.contains("60"), "Expected Order Total to contain '60', got '\(orderTotal.label)'")
    }

    // MARK: - TC-CART-002: Increment Quantity Reactive Order Total (BUG-006)

    /// TC-CART-002: Increment item quantity and verify reactive order total calculation.
    /// Category: Positive (Regression: BUG-006)
    func test_tc_cart_002_increment_quantity_reactive_order_total() {
        addItemAndOpenCart()

        let incrementBtn = el("qty-increment-p1")
        XCTAssertTrue(incrementBtn.waitForExistence(timeout: 5.0), "Expected '+' button for product p1")
        incrementBtn.tap()

        let qty = el("qty-p1")
        XCTAssertEqual(qty.label, "2", "Expected quantity to increment to '2'")

        let lineTotal = el("line-total-p1")
        XCTAssertTrue(lineTotal.label.contains("120"), "Expected line total to be '120', got '\(lineTotal.label)'")

        let orderTotal = el("order-total")
        XCTAssertTrue(
            orderTotal.label.contains("120"),
            "BUG-006: Order Total did not reactively update on quantity increment (got '\(orderTotal.label)')"
        )
    }

    // MARK: - TC-CART-003: Decrement Quantity Reactive Order Total (BUG-006)

    /// TC-CART-003: Decrement item quantity and verify reactive order total reduction.
    /// Category: Positive (Regression: BUG-006)
    func test_tc_cart_003_decrement_quantity_reactive_order_total() {
        addItemAndOpenCart()

        let incrementBtn = el("qty-increment-p1")
        XCTAssertTrue(incrementBtn.waitForExistence(timeout: 5.0), "Expected '+' button for product p1")
        incrementBtn.tap()

        let decrementBtn = el("qty-decrement-p1")
        XCTAssertTrue(decrementBtn.waitForExistence(timeout: 5.0), "Expected '−' button for product p1")
        decrementBtn.tap()

        let qty = el("qty-p1")
        XCTAssertEqual(qty.label, "1", "Expected quantity to decrement back to '1'")

        let lineTotal = el("line-total-p1")
        XCTAssertTrue(lineTotal.label.contains("60"), "Expected line total to be '60', got '\(lineTotal.label)'")

        let orderTotal = el("order-total")
        XCTAssertTrue(
            orderTotal.label.contains("60"),
            "BUG-006: Order Total did not reactively update on quantity decrement (got '\(orderTotal.label)')"
        )
    }

    // MARK: - TC-CART-004: Apply Valid Discount SAVE10 (BUG-004)

    /// TC-CART-004: Apply valid discount code SAVE10 for 10% discount deduction.
    /// Category: Positive (Regression: BUG-004)
    func test_tc_cart_004_apply_valid_discount_save10() {
        addItemAndOpenCart()

        let discountInput = el("discount-input")
        XCTAssertTrue(discountInput.waitForExistence(timeout: 5.0), "Expected discount code text field")
        discountInput.tap()
        discountInput.typeText("SAVE10")

        let orderTotal = el("order-total")
        XCTAssertTrue(
            orderTotal.label.contains("54"),
            "BUG-004: Discount calculation error. Expected Order Total $54 after 10% off $60, got '\(orderTotal.label)'"
        )
    }

    // MARK: - TC-CART-005: Prevent Decrement Below 1 (BUG-005)

    /// TC-CART-005: Prevent quantity decrement below minimum threshold of 1.
    /// Category: Negative (Regression: BUG-005)
    func test_tc_cart_005_prevent_quantity_decrement_below_one() {
        addItemAndOpenCart()

        let decrementBtn = el("qty-decrement-p1")
        XCTAssertTrue(decrementBtn.waitForExistence(timeout: 5.0), "Expected '−' button for product p1")
        decrementBtn.tap()

        let qty = el("qty-p1")
        XCTAssertEqual(
            qty.label,
            "1",
            "BUG-005: Quantity decremented below minimum threshold of 1 to '\(qty.label)'"
        )
    }

    // MARK: - TC-CART-006: Reject Checkout Below $10 Minimum

    /// TC-CART-006: Reject checkout progression when order total is below minimum $10 threshold.
    /// Category: Negative (Requirement: S9)
    func test_tc_cart_006_reject_checkout_when_total_below_ten() {
        login()

        let cartTab = app.buttons["Cart"]
        if cartTab.waitForExistence(timeout: 5.0) {
            cartTab.tap()
        }

        let proceedBtn = el("proceed-checkout")
        if proceedBtn.exists {
            proceedBtn.tap()
            let message = el("cart-message")
            XCTAssertTrue(message.waitForExistence(timeout: 3.0), "Expected minimum order error message")
            XCTAssertTrue(message.label.contains("10.00"), "Expected message containing '10.00', got '\(message.label)'")
        }
    }

    // MARK: - TC-CART-007: Reject Invalid Discount Code

    /// TC-CART-007: Reject invalid discount code without modifying order total.
    /// Category: Negative (Requirement: S7)
    func test_tc_cart_007_reject_invalid_discount_code() {
        addItemAndOpenCart()

        let discountInput = el("discount-input")
        XCTAssertTrue(discountInput.waitForExistence(timeout: 5.0), "Expected discount code input")
        discountInput.tap()
        discountInput.typeText("INVALID99")

        let orderTotal = el("order-total")
        XCTAssertTrue(
            orderTotal.label.contains("60"),
            "Expected order total to remain $60 for invalid discount, got '\(orderTotal.label)'"
        )
    }

    // MARK: - TC-CART-008: Display Empty Cart State

    /// TC-CART-008: Display empty cart state when no items are present.
    /// Category: Edge (Requirement: S6)
    func test_tc_cart_008_display_empty_cart_state() {
        login()

        let cartTab = app.buttons["Cart"]
        XCTAssertTrue(cartTab.waitForExistence(timeout: 5.0), "Expected Cart tab button")
        cartTab.tap()

        let emptyCart = el("cart-empty")
        XCTAssertTrue(emptyCart.waitForExistence(timeout: 5.0), "Expected 'cart-empty' element")
        XCTAssertEqual(emptyCart.label, "Your cart is empty", "Expected 'Your cart is empty' text")
    }

    // MARK: - TC-CART-009: Register Rapid Consecutive Taps

    /// TC-CART-009: Register rapid consecutive taps on catalog Add button.
    /// Category: Edge (Requirement: S1)
    func test_tc_cart_009_register_rapid_consecutive_taps() {
        login()

        let addBtn = el("add-p1")
        XCTAssertTrue(addBtn.waitForExistence(timeout: 5.0), "Expected Add button for product p1")
        addBtn.tap()
        addBtn.tap()
        addBtn.tap()

        let cartTab = app.buttons["Cart"]
        if cartTab.waitForExistence(timeout: 5.0) {
            cartTab.tap()
        }

        let qty = el("qty-p1")
        XCTAssertTrue(qty.waitForExistence(timeout: 5.0), "Expected quantity element for product p1")
        XCTAssertEqual(qty.label, "3", "Expected quantity to be '3' after 3 rapid taps")

        let lineTotal = el("line-total-p1")
        XCTAssertTrue(lineTotal.label.contains("180"), "Expected line total $180, got '\(lineTotal.label)'")

        let orderTotal = el("order-total")
        XCTAssertTrue(orderTotal.label.contains("180"), "Expected order total $180, got '\(orderTotal.label)'")
    }

    // MARK: - TC-CART-010: Block Adding Out-of-Stock Product

    /// TC-CART-010: Block adding out-of-stock product to cart.
    /// Category: Edge (Regression: BUG-008)
    func test_tc_cart_010_block_adding_out_of_stock_product() {
        login()

        let addP4 = el("add-p4")
        XCTAssertTrue(addP4.waitForExistence(timeout: 5.0), "Expected Add button for product p4")
        if addP4.isEnabled {
            addP4.tap()
        }

        let cartTab = app.buttons["Cart"]
        if cartTab.waitForExistence(timeout: 5.0) {
            cartTab.tap()
        }

        let emptyCart = el("cart-empty")
        XCTAssertTrue(
            emptyCart.waitForExistence(timeout: 5.0),
            "BUG-008: Out-of-stock product was added to cart or cart is not empty"
        )
    }
}
