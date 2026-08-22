import XCTest

/// General and Catalog UI test suite covering catalog layout, navigation titles,
/// out-of-stock badges, and unauthenticated tab bar isolation.
final class GeneralUITests: TechShopUITestCase {

    // MARK: - TC-CAT-001: Navigation Title (BUG-014)

    /// TC-CAT-001: Verify catalog navigation title displays 'Products'.
    /// Category: Positive (Regression: BUG-014)
    func test_tc_cat_001_catalog_navigation_title_displays_products() {
        login()

        let firstProduct = el("product-name-p1")
        XCTAssertTrue(firstProduct.waitForExistence(timeout: 5.0), "Expected catalog screen to be loaded")

        // Catch BUG-014 where navigationTitle is set to "Untitled" instead of "Products"
        XCTAssertFalse(
            app.navigationBars["Untitled"].exists || app.staticTexts["Untitled"].exists,
            "BUG-014: Catalog navigation title is 'Untitled' instead of 'Products'"
        )
        XCTAssertTrue(
            app.navigationBars["Products"].exists || app.staticTexts["Products"].exists,
            "Expected navigation title 'Products'"
        )
    }

    // MARK: - TC-CAT-002: Title Bounds Truncation (BUG-007)

    /// TC-CAT-002: Truncate long product titles without overflowing cell bounds.
    /// Category: Edge (Regression: BUG-007)
    func test_tc_cat_002_truncate_long_product_titles_without_overflow() {
        login()

        let product3 = el("product-name-p3")
        XCTAssertTrue(product3.waitForExistence(timeout: 5.0), "Expected product p3 to exist in catalog")

        // In the broken build (BUG-007), missing .lineLimit causes the title to wrap into ~76px height.
        // In the fixed build, single line truncation keeps height around ~19-24px (< 40px).
        XCTAssertLessThan(
            product3.frame.height,
            40.0,
            "BUG-007: Product 3 title overflows cell bounds (height: \(product3.frame.height)px, expected < 40px)"
        )
    }

    // MARK: - TC-CAT-003: Out of Stock Badge and Disabled Add Button (BUG-008)

    /// TC-CAT-003: Display red badge and disable Add button for out-of-stock item.
    /// Category: Edge (Regression: BUG-008)
    func test_tc_cat_003_out_of_stock_badge_and_disabled_add_button() {
        login()

        let badge = el("badge-p4")
        XCTAssertTrue(badge.waitForExistence(timeout: 5.0), "Expected out-of-stock badge for product p4")
        XCTAssertEqual(badge.label, "Out of Stock", "Expected badge text 'Out of Stock'")

        let addButton = el("add-p4")
        XCTAssertTrue(addButton.waitForExistence(timeout: 5.0), "Expected Add button for product p4")
        XCTAssertFalse(
            addButton.isEnabled,
            "BUG-008: 'add-p4' button is enabled for an out-of-stock product"
        )
    }

    // MARK: - TC-LOG-008: Tab Bar Hidden Before Auth (BUG-015)

    /// TC-LOG-008: Ensure tab bar navigation is hidden while unauthenticated.
    /// Category: Edge (Regression: BUG-015)
    func test_tc_log_008_no_tab_bar_before_auth() {
        // Fresh unauthenticated launch: verify Products and Cart tabs are hidden
        XCTAssertFalse(
            app.tabBars.buttons["Products"].exists || app.buttons["Products"].exists,
            "BUG-015: Products tab is visible and interactive before user authentication"
        )
        XCTAssertFalse(
            app.tabBars.buttons["Cart"].exists || app.buttons["Cart"].exists,
            "BUG-015: Cart tab is visible and interactive before user authentication"
        )
    }
}
