from .base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object representing the TechShop Login screen.
    """

    EMAIL_INPUT = "login-email"
    PASSWORD_INPUT = "login-password"
    LOGIN_BUTTON_LABEL = "Log In"
    LOGIN_BUTTON_ID = "login-submit"
    ERROR_MESSAGE_ID = "login-error"

    def is_loaded(self, timeout=5):
        """Checks if Login screen is rendered."""
        return self.exists(self.EMAIL_INPUT, timeout=timeout)

    def enter_email(self, email):
        """Types email into the email input field."""
        self.type_into(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password):
        """Types password into the password input field."""
        self.type_into(self.PASSWORD_INPUT, password)
        return self

    def tap_login_button(self):
        """
        Taps the Login button using stable ID 'login-submit' when available,
        falling back to visible label 'Log In' for BUG-016 cross-build compatibility.
        """
        if self.exists(self.LOGIN_BUTTON_ID, timeout=2):
            self.click_id(self.LOGIN_BUTTON_ID)
        else:
            self.click_by_label(self.LOGIN_BUTTON_LABEL)
        return self

    def login(self, email="", password=""):
        """Convenience helper to enter email, password, and tap Log In."""
        if email:
            self.enter_email(email)
        if password:
            self.enter_password(password)
        self.tap_login_button()
        return self

    def get_error_message(self, timeout=3):
        """Gets text of the error message if displayed."""
        if self.exists(self.ERROR_MESSAGE_ID, timeout=timeout):
            return self.get_text(self.ERROR_MESSAGE_ID, timeout=timeout)
        return ""

    def is_error_displayed(self, timeout=3):
        """Checks if error label is visible."""
        return self.exists(self.ERROR_MESSAGE_ID, timeout=timeout)

    def get_password_field_type(self):
        """Returns the XCUI element type for the password field (BUG-001 check)."""
        return self.get_attribute(self.PASSWORD_INPUT, "type")

    def has_login_submit_id(self):
        """Checks if login button has stable accessibility identifier 'login-submit' (BUG-016 check)."""
        return self.exists(self.LOGIN_BUTTON_ID, timeout=2)

    def is_tab_bar_visible(self):
        """Checks if tab bar items (Products/Cart) are present on screen (BUG-015 check)."""
        return self.text_visible("Products", timeout=1) or self.text_visible("Cart", timeout=1)
