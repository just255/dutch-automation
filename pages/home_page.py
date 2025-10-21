"""
HomePage Module

This module contains the HomePage class representing the Dutch.com home page.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class HomePage(BasePage):
    """Page Object Model for Dutch.com home page."""

    # Navigation Elements
    home_page_logo_link = (By.CSS_SELECTOR, "#header a[href='https://www.dutch.com']")
    home_page_nav_login_link = (By.CSS_SELECTOR, "#header a[href='/account/login']")
    home_page_nav_signup_link = (By.CSS_SELECTOR, "#header a[href='/account/register'].button")

    # Call-to-Action Elements (Registration Flow)
    # Note: Website uses different URLs (A/B testing or geo-based):
    # - Some regions: href="/account/register"
    # - Other regions: href="https://register.dutch.com/"
    # Targeting the header Join Now button with specific classes to avoid hidden elements
    home_page_primary_cta_button = (By.XPATH, "//a[contains(@class, 'button') and contains(@class, 'px-4') and contains(text(), 'Join Now')]")
    home_page_get_started_button = (
        By.XPATH,
        "//a[@href='/account/register' and contains(@class, 'rounded-full') and contains(., 'Get started')]"
    )

    # Footer Elements
    home_page_footer_newsletter_email_input = (By.ID, "newsletter_footer-email")
    home_page_footer_newsletter_submit_button = (By.ID, "Subscribe")

    def click_primary_cta(self) -> None:
        """Click the main hero CTA button to start registration."""
        self.click_element(self.home_page_primary_cta_button)

    def click_nav_signup(self) -> None:
        """Click the signup link in the navigation header."""
        self.click_element(self.home_page_nav_signup_link)

    def verify_home_page_loaded(self) -> bool:
        """
        Verify home page has loaded.

        Returns:
            True if loaded, False otherwise
        """
        loaded = self.verify_url_contains("dutch.com")
        if loaded:
            logger.info("Home page loaded successfully")
        return loaded

    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for home page to fully load.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if page loaded, False otherwise
        """
        return self.wait_for_element_visible(self.home_page_primary_cta_button, timeout)

    def navigate_to_home(self, base_url: str) -> None:
        """
        Navigate to home page.

        Args:
            base_url: Base URL of the site
        """
        self.navigate_to(base_url)
