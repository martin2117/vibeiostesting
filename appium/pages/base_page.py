import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """
    Base Page Object providing explicit wait, locate, attribute inspection,
    and interaction helpers for iOS XCUITest automation.
    """

    def __init__(self, driver, default_timeout=10):
        self.driver = driver
        self.default_timeout = default_timeout

    def by_id(self, accessibility_id, timeout=None):
        """Locates an element by accessibility identifier with explicit wait."""
        wait_time = timeout if timeout is not None else self.default_timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
        )

    def by_predicate(self, predicate_string, timeout=None):
        """Locates an element using an iOS predicate string with explicit wait."""
        wait_time = timeout if timeout is not None else self.default_timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((AppiumBy.IOS_PREDICATE, predicate_string))
        )

    def exists(self, accessibility_id, timeout=5):
        """Checks if an element with the given accessibility identifier exists within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def text_visible(self, text, timeout=None):
        """Checks if an element with the visible text/label exists and is visible."""
        predicate = f'label == "{text}" OR name == "{text}" OR value == "{text}"'
        try:
            elem = self.by_predicate(predicate, timeout=timeout)
            return elem.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def type_into(self, accessibility_id, text, clear_first=False):
        """Locates an element by accessibility identifier, ensures focus, and types text into it."""
        element = self.by_id(accessibility_id)
        element.click()
        time.sleep(0.2)
        if clear_first:
            try:
                element.clear()
                time.sleep(0.1)
            except Exception:
                pass
        element.send_keys(text)
        time.sleep(0.1)
        return element

    def click_id(self, accessibility_id, timeout=None):
        """Locates an element by accessibility identifier and clicks it."""
        element = self.by_id(accessibility_id, timeout=timeout)
        time.sleep(0.1)
        element.click()
        return element

    def click_by_label(self, label, timeout=None):
        """Locates an element by visible label predicate and clicks it."""
        predicate = f'label == "{label}" OR name == "{label}"'
        element = self.by_predicate(predicate, timeout=timeout)
        time.sleep(0.1)
        element.click()
        return element

    def get_attribute(self, accessibility_id, attr_name, timeout=None):
        """Gets element attribute (e.g. 'type', 'value', 'label') by accessibility identifier."""
        element = self.by_id(accessibility_id, timeout=timeout)
        return element.get_attribute(attr_name)

    def get_text(self, accessibility_id, timeout=None):
        """Retrieves visible text/label/value of an element by accessibility identifier."""
        element = self.by_id(accessibility_id, timeout=timeout)
        return element.text or element.get_attribute("label") or element.get_attribute("value") or ""

    def background_app(self, seconds=5):
        """Sends the app to background for specified seconds, then brings it back."""
        self.driver.background_app(seconds)
