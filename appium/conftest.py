import os
import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions


@pytest.fixture(scope="session")
def test_credentials():
    """Reads test credentials from environment variables."""
    return {
        "email": os.environ.get("TEST_EMAIL", "demo@techshop.com"),
        "password": os.environ.get("TEST_PASSWORD", "password123"),
    }


@pytest.fixture(scope="function")
def driver():
    """
    Function-scoped driver fixture that launches the app fresh for each test.
    Connects to the Appium server using XCUITest automation for bundle com.techshop.ios.
    """
    appium_server_url = os.environ.get("APPIUM_SERVER", "http://127.0.0.1:4723")
    device_name = os.environ.get("IOS_DEVICE", "iPhone 15")
    platform_version = os.environ.get("IOS_VERSION")
    device_udid = os.environ.get("DEVICE_ID")

    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.bundle_id = "com.techshop.ios"
    options.device_name = device_name
    if device_udid:
        options.udid = device_udid
    if platform_version:
        options.platform_version = platform_version

    # Ensure clean state and fresh launch per test isolation rule
    options.no_reset = False
    options.full_reset = False
    options.new_command_timeout = 120

    app_driver = webdriver.Remote(command_executor=appium_server_url, options=options)
    # Ensure fresh process launch per test isolation rule
    try:
        app_driver.terminate_app("com.techshop.ios")
        app_driver.activate_app("com.techshop.ios")
    except Exception:
        pass
    # Implicit wait kept low; Page Object Model uses explicit WebDriverWait
    app_driver.implicitly_wait(1)

    yield app_driver

    try:
        app_driver.quit()
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = os.environ.get(
                "APPIUM_SCREENSHOT_DIR",
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-results", "appium-broken"))
            )
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            try:
                driver.save_screenshot(screenshot_path)
            except Exception:
                pass
