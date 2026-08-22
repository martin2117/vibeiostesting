import pytest
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from flows import login_as_standard_user


def test_tc_cat_001_catalog_navigation_title_displays_products(driver, test_credentials):
    """
    TC-CAT-001: Verify catalog navigation title displays 'Products'.
    Category: Positive (Regression: BUG-014)
    Steps:
      1. Log in with valid credentials
      2. Observe top navigation bar title on Catalog screen
    Expected Result:
      Navigation title displays 'Products' (not 'Untitled').
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    assert catalog_page.is_loaded(timeout=5), "Expected Catalog page to load after login"

    nav_title = catalog_page.get_navigation_title()
    assert nav_title != "Untitled", "BUG-014: Catalog navigation title is 'Untitled' instead of 'Products'"
    assert nav_title == "Products", f"Expected navigation title 'Products', got '{nav_title}'"


def test_tc_cat_002_truncate_long_product_titles_without_overflow(driver, test_credentials):
    """
    TC-CAT-002: Truncate long product titles without overflowing cell bounds.
    Category: Edge (Regression: BUG-007)
    Steps:
      1. Log in with valid credentials
      2. Locate Product 3 ('Ultra-Wide Curved 49-inch Professional Gaming Monitor with HDR')
      3. Inspect title element bounding box height
    Expected Result:
      Title is single-line truncated with ellipsis (height ~19-24px, not 76px multiline overflow).
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    assert catalog_page.has_product("p3"), "Expected Product 3 to exist in catalog"

    height = catalog_page.get_product_name_height("p3")
    assert height < 40, f"BUG-007: Product 3 title overflows cell bounds (height: {height}px, expected < 40px)"


def test_tc_cat_003_out_of_stock_badge_and_disabled_add_button(driver, test_credentials):
    """
    TC-CAT-003: Display status badge and disable Add button for out-of-stock item.
    Category: Edge (Regression: BUG-008)
    Steps:
      1. Log in with valid credentials
      2. Locate Product 4 (USB-C Hub)
      3. Inspect badge text and Add button enabled state
    Expected Result:
      Badge displays 'Out of Stock' and Add button 'add-p4' is disabled.
    """
    catalog_page = login_as_standard_user(driver, email=test_credentials["email"], password=test_credentials["password"])
    assert catalog_page.has_product("p4"), "Expected Product 4 to exist in catalog"

    badge_text = catalog_page.get_badge_text("p4")
    assert badge_text == "Out of Stock", f"Expected badge 'Out of Stock', got '{badge_text}'"

    is_enabled = catalog_page.is_add_button_enabled("p4")
    assert not is_enabled, "BUG-008: 'add-p4' button is enabled for an out-of-stock product"


def test_tc_log_008_no_tab_bar_before_auth(driver):
    """
    TC-LOG-008: Ensure tab bar navigation is hidden while unauthenticated.
    Category: Edge (Regression: BUG-015)
    Steps:
      1. Fresh app launch on Login screen
      2. Inspect bottom tab bar area
    Expected Result:
      Tab bar (Products / Cart tabs) is completely hidden prior to authentication.
    """
    login_page = LoginPage(driver)
    assert not login_page.is_tab_bar_visible(), (
        "BUG-015: Tab bar is visible and interactive before user authentication"
    )
