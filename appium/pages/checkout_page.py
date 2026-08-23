import time
from .base_page import BasePage


class CheckoutPage(BasePage):
    """
    Page Object representing the TechShop Checkout & Confirmation screens.
    """

    FIRST_NAME_INPUT = "checkout-firstName"
    LAST_NAME_INPUT = "checkout-lastName"
    EMAIL_INPUT = "checkout-email"
    PHONE_INPUT = "checkout-phone"
    CARD_INPUT = "checkout-card"
    EXPIRY_INPUT = "checkout-expiry"
    CVV_INPUT = "checkout-cvv"
    ERROR_MESSAGE = "checkout-error"
    SUBMIT_BUTTON = "checkout-submit"

    # Confirmation screen locators
    CONFIRMATION_TITLE = "confirmation-title"
    CONFIRMATION_ORDER_REF = "confirmation-order-ref"
    CONFIRMATION_TOTAL = "confirmation-total"

    def is_loaded(self, timeout=10):
        """Checks if the checkout form is loaded."""
        return self.exists(self.FIRST_NAME_INPUT, timeout=timeout)

    def enter_first_name(self, value):
        self.type_into(self.FIRST_NAME_INPUT, value)
        return self

    def enter_last_name(self, value):
        self.type_into(self.LAST_NAME_INPUT, value)
        return self

    def enter_email(self, value):
        self.type_into(self.EMAIL_INPUT, value)
        return self

    def enter_phone(self, value):
        self.type_into(self.PHONE_INPUT, value)
        return self

    def enter_card(self, value):
        self.type_into(self.CARD_INPUT, value)
        return self

    def enter_expiry(self, value):
        self.type_into(self.EXPIRY_INPUT, value)
        return self

    def enter_cvv(self, value):
        self.type_into(self.CVV_INPUT, value)
        return self

    def fill_form(self, first_name="Jane", last_name="Doe", email="jane.doe@example.com",
                  phone="1234567890", card="1111222233334444", expiry="12/29", cvv="123"):
        """Fills all fields in the checkout form."""
        if first_name is not None:
            self.enter_first_name(first_name)
        if last_name is not None:
            self.enter_last_name(last_name)
        if email is not None:
            self.enter_email(email)
        if phone is not None:
            self.enter_phone(phone)
        if card is not None:
            self.enter_card(card)
        if expiry is not None:
            self.enter_expiry(expiry)
        if cvv is not None:
            self.enter_cvv(cvv)
        return self

    def dismiss_keyboard_if_present(self):
        """Dismisses software keyboard if open."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        try:
            if self.exists("checkout-heading", timeout=1):
                self.click_id("checkout-heading")
        except Exception:
            pass
        return self

    def submit_order(self):
        """Taps the 'Place Order' submit button."""
        self.dismiss_keyboard_if_present()
        try:
            self.click_id(self.SUBMIT_BUTTON, timeout=5)
        except Exception:
            try:
                self.driver.execute_script("mobile: scroll", {"direction": "down"})
            except Exception:
                pass
            self.click_id(self.SUBMIT_BUTTON, timeout=10)
        return self

    def get_error_message(self, timeout=5):
        """Returns the checkout validation error message text."""
        return self.get_text(self.ERROR_MESSAGE, timeout=timeout)

    def has_error(self, timeout=5):
        """Checks if a checkout validation error is displayed."""
        return self.exists(self.ERROR_MESSAGE, timeout=timeout)

    def is_order_confirmed(self, timeout=10):
        """Checks if the confirmation screen is displayed."""
        return self.exists(self.CONFIRMATION_TITLE, timeout=timeout)

    def get_order_reference(self, timeout=5):
        """Returns the order reference string (e.g. 'Order Reference: TS-XXXXXX')."""
        return self.get_text(self.CONFIRMATION_ORDER_REF, timeout=timeout)

    def get_total_paid(self, timeout=5):
        """Returns the total paid text on the confirmation screen."""
        return self.get_text(self.CONFIRMATION_TOTAL, timeout=timeout)
