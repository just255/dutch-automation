"""
Pytest Configuration and Fixtures

This module contains pytest fixtures for test setup and teardown.

Author: Claude AI
Date: 2025-10-19
"""

import pytest
import json
import os
from datetime import datetime
from utils.driver_manager import DriverManager
from utils.logger import setup_logger
from utils.screenshot_helper import ScreenshotHelper


# Global variable to store test run timestamp
TEST_RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def pytest_configure(config):
    """
    Pytest hook to configure test run settings.
    Creates timestamped folder structure for this test run.
    """
    global TEST_RUN_TIMESTAMP

    # Create timestamped test run folder
    test_run_dir = os.path.join("reports", f"test_run_{TEST_RUN_TIMESTAMP}")
    os.makedirs(test_run_dir, exist_ok=True)

    # Create screenshots folder within this test run
    screenshots_dir = os.path.join(test_run_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Store paths in config for access by fixtures
    config.test_run_dir = test_run_dir
    config.screenshots_dir = screenshots_dir

    # Configure HTML report path if --html option was used
    if config.option.htmlpath:
        # Override HTML report path to be in timestamped folder
        htmlpath = os.path.join(test_run_dir, "report.html")
        config.option.htmlpath = htmlpath


@pytest.fixture(scope="session")
def test_run_dir(request):
    """
    Get the timestamped test run directory.

    Returns:
        Path to test run directory
    """
    return request.config.test_run_dir


@pytest.fixture(scope="session")
def config():
    """
    Load configuration settings.

    Returns:
        Configuration dictionary
    """
    from config.settings import Config
    return Config


@pytest.fixture(scope="session")
def test_data():
    """
    Load test data from JSON file and generate unique email for each test run.

    Returns:
        Test data dictionary with unique email
    """
    test_data_path = os.path.join("config", "test_data.json")
    with open(test_data_path, 'r') as f:
        data = json.load(f)

    # Generate unique email with timestamp using + notation (alias)
    if 'test_users' in data and len(data['test_users']) > 0:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        original_email = data['test_users'][0]['email']
        # Insert timestamp with + before @
        email_parts = original_email.split('@')
        data['test_users'][0]['email'] = f"{email_parts[0]}+{timestamp}@{email_parts[1]}"

    return data


@pytest.fixture(scope="function")
def setup(request, config):
    """
    Setup WebDriver for each test.

    Args:
        request: Pytest request object
        config: Configuration settings

    Yields:
        WebDriver instance
    """
    logger = setup_logger(__name__, config.LOG_LEVEL)
    logger.info("=" * 80)
    logger.info(f"Starting test: {request.node.name}")
    logger.info("=" * 80)

    # Initialize driver
    driver_manager = DriverManager(
        browser=config.BROWSER,
        headless=config.HEADLESS
    )
    driver = driver_manager.get_driver()

    # Set timeouts
    driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)

    # Initialize screenshot helper with timestamped folder
    screenshots_dir = request.config.screenshots_dir
    screenshot_helper = ScreenshotHelper(driver, screenshots_dir)

    # Make screenshot helper available to test
    request.node.screenshot_helper = screenshot_helper

    yield driver

    # Teardown
    logger.info("=" * 80)
    logger.info(f"Finishing test: {request.node.name}")
    logger.info("=" * 80)

    # Capture screenshot on failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_helper.capture_on_failure(request.node.name)

    driver_manager.quit_driver()


@pytest.fixture(scope="function")
def screenshot_helper(request):
    """
    Get screenshot helper instance for the test.

    Args:
        request: Pytest request object

    Returns:
        ScreenshotHelper instance
    """
    return request.node.screenshot_helper


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture test execution result and add screenshots to HTML report.

    This hook makes the test result available in fixtures and embeds screenshots in reports.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    # Add screenshots and HTML source to HTML report
    extra = getattr(rep, 'extra', [])

    if rep.when == 'call':
        # Add screenshots to report if test has screenshot helper
        if hasattr(item, 'screenshot_helper'):
            screenshots_dir = item.config.screenshots_dir

            # Find all screenshots for this test (if any were captured)
            if os.path.exists(screenshots_dir):
                screenshots = [
                    f for f in os.listdir(screenshots_dir)
                    if f.endswith('.png') and not f.startswith('FAILED_')
                ]

                # Add screenshots to HTML report
                for screenshot in sorted(screenshots):
                    screenshot_path = os.path.join(screenshots_dir, screenshot)
                    # Use relative path for HTML report
                    relative_path = os.path.join("screenshots", screenshot)

                    if hasattr(pytest, 'html'):
                        extra.append(pytest.html.div(
                            pytest.html.img(src=relative_path),
                            className="screenshot"
                        ))

            # Add HTML source files for failures
            failures_dir = os.path.join(screenshots_dir, "failures")
            if rep.failed and os.path.exists(failures_dir):
                html_files = [
                    f for f in os.listdir(failures_dir)
                    if f.endswith('.html')
                ]

                # Add HTML source files as links in report
                for html_file in sorted(html_files):
                    relative_path = os.path.join("screenshots", "failures", html_file)

                    if hasattr(pytest, 'html'):
                        extra.append(pytest.html.div(
                            pytest.html.p(
                                pytest.html.strong("HTML Source at Failure: "),
                                pytest.html.a(html_file, href=relative_path, target="_blank")
                            ),
                            className="html-source"
                        ))

        rep.extra = extra
