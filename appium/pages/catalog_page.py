import time
from .base_page import BasePage


class CatalogPage(BasePage):
    """
    Page Object representing the TechShop Product Catalog screen.
    """

    PRODUCT_NAME_P1 = "product-name-p1"
    ADD_BUTTON_P1 = "add-p1"
    CART_TAB_LABEL = "Cart"
    PRODUCTS_TAB_LABEL = "Products"

    def is_loaded(self, timeout=5):
        """Checks if the catalog screen is rendered by verifying the first product."""
        return self.exists(self.PRODUCT_NAME_P1, timeout=timeout)

    def has_product(self, product_id="p1", timeout=5):
        """Checks if a product with the specified ID exists in the catalog list."""
        return self.exists(f"product-name-{product_id}", timeout=timeout)

    def get_product_name(self, product_id="p1", timeout=5):
        """Returns the product name text for the given product ID."""
        return self.get_text(f"product-name-{product_id}", timeout=timeout)

    def get_product_name_height(self, product_id="p3"):
        """Returns the bounding box height of a product title element (for BUG-007 check)."""
        element = self.by_id(f"product-name-{product_id}")
        return element.size["height"]

    def get_badge_text(self, product_id="p4", timeout=3):
        """Returns the text of the badge for a product (e.g. 'Out of Stock')."""
        return self.get_text(f"badge-{product_id}", timeout=timeout)

    def is_add_button_enabled(self, product_id="p4"):
        """Checks whether the Add button for a product is enabled."""
        element = self.by_id(f"add-{product_id}")
        return element.is_enabled() and element.get_attribute("enabled") in ("true", "1", True)

    def add_to_cart(self, product_id="p1"):
        """Taps the Add button for a specific product."""
        elem = self.by_id(f"add-{product_id}", timeout=5)
        time.sleep(0.3)
        elem.click()
        time.sleep(0.3)
        return self

    def navigate_to_cart(self):
        """Taps the Cart tab in the tab bar."""
        if self.exists("tab-cart", timeout=2):
            self.click_id("tab-cart")
        else:
            self.click_by_label(self.CART_TAB_LABEL)
        self.exists("order-total", timeout=5)
        return self

    def navigate_to_products(self):
        """Taps the Products tab in the tab bar."""
        if self.exists("tab-products", timeout=2):
            self.click_id("tab-products")
        else:
            self.click_by_label(self.PRODUCTS_TAB_LABEL)
        self.is_loaded(timeout=5)
        return self

    def get_navigation_title(self, timeout=3):
        """Returns the navigation title (e.g., 'Products' vs 'Untitled' for BUG-014)."""
        if self.text_visible("Products", timeout=timeout):
            return "Products"
        if self.text_visible("Untitled", timeout=timeout):
            return "Untitled"
        return ""
