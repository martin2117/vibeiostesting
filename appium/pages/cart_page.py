from .base_page import BasePage


class CartPage(BasePage):
    """
    Page Object representing the TechShop Shopping Cart screen.
    """

    EMPTY_CART_ID = "cart-empty"
    DISCOUNT_INPUT_ID = "discount-input"
    ORDER_TOTAL_ID = "order-total"
    CART_MESSAGE_ID = "cart-message"
    PROCEED_CHECKOUT_ID = "proceed-checkout"

    def is_empty(self, timeout=3):
        """Checks if the empty cart state message is visible."""
        return self.exists(self.EMPTY_CART_ID, timeout=timeout)

    def get_empty_cart_text(self, timeout=3):
        """Returns the text displayed when the cart is empty."""
        return self.get_text(self.EMPTY_CART_ID, timeout=timeout)

    def has_item(self, product_id="p1", timeout=5):
        """Checks if an item with the given product ID is present in the cart."""
        return self.exists(f"qty-{product_id}", timeout=timeout)

    def get_quantity(self, product_id="p1", timeout=3):
        """Returns the quantity text for a given product ID in the cart."""
        return self.get_text(f"qty-{product_id}", timeout=timeout)

    def increment_quantity(self, product_id="p1"):
        """Taps the '+' increment button for a given product ID."""
        self.click_id(f"qty-increment-{product_id}")
        return self

    def decrement_quantity(self, product_id="p1"):
        """Taps the '−' decrement button for a given product ID."""
        self.click_id(f"qty-decrement-{product_id}")
        return self

    def get_line_total(self, product_id="p1", timeout=3):
        """Returns the line total text (e.g. 'Line: $60') for a product."""
        return self.get_text(f"line-total-{product_id}", timeout=timeout)

    def apply_discount(self, code):
        """Enters a discount code into the discount text field and submits."""
        self.type_into(self.DISCOUNT_INPUT_ID, code)
        return self

    def get_order_total(self, timeout=3):
        """Returns the Order Total text (e.g. 'Order Total: $60')."""
        return self.get_text(self.ORDER_TOTAL_ID, timeout=timeout)

    def get_cart_message(self, timeout=3):
        """Returns error or status message (e.g. 'Minimum order value is $10.00')."""
        return self.get_text(self.CART_MESSAGE_ID, timeout=timeout)

    def has_cart_message(self, timeout=2):
        """Checks if a cart status/error message is visible."""
        return self.exists(self.CART_MESSAGE_ID, timeout=timeout)

    def proceed_to_checkout(self):
        """Taps the 'Proceed to Checkout' button."""
        self.click_id(self.PROCEED_CHECKOUT_ID)
        return self
