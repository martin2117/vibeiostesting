import os
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage


def login_as_standard_user(driver, email=None, password=None):
    """
    Shared flow: logs into TechShop using valid credentials and navigates to the Catalog.
    Reads credentials from environment variables if not explicitly provided.
    """
    user_email = email or os.environ.get("TEST_EMAIL", "demo@techshop.com")
    user_password = password or os.environ.get("TEST_PASSWORD", "password123")

    login_page = LoginPage(driver)
    login_page.login(email=user_email, password=user_password)

    catalog_page = CatalogPage(driver)
    catalog_page.is_loaded(timeout=10)
    return catalog_page


def add_first_item_and_view_cart(driver, email=None, password=None):
    """
    Shared flow: authenticates (if on login screen), adds the first catalog item (p1) to cart,
    and navigates to the Cart view.
    """
    login_page = LoginPage(driver)
    if login_page.is_loaded(timeout=5):
        catalog_page = login_as_standard_user(driver, email=email, password=password)
    else:
        catalog_page = CatalogPage(driver)
        if catalog_page.text_visible("Products", timeout=2):
            catalog_page.click_by_label("Products")
        catalog_page.is_loaded(timeout=5)

    catalog_page.is_loaded(timeout=5)
    catalog_page.add_to_cart("p1")
    catalog_page.navigate_to_cart()
