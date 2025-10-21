"""
RegistrationPage Module

This module contains the RegistrationPage class for the account registration page.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RegistrationPage(BasePage):
    """Page Object Model for Dutch.com Registration page."""

    # Form Input Fields
    registration_page_email_input = (By.ID, "input_1")
    registration_page_password_input = (By.ID, "input_2")

    # Buttons
    registration_page_register_button = (
        By.XPATH,
        "//button[@type='submit' and contains(text(), 'Register')]"
    )
    registration_page_google_signup_button = (
        By.XPATH,
        "//a[@role='link' and .//span[text()='Google']]"
    )

    # Links
    registration_page_terms_conditions_link = (By.XPATH, "//a[@href='/pages/terms-and-conditions']")
    registration_page_privacy_policy_link = (By.XPATH, "//a[@href='/pages/privacy-policy']")

    # Form Container
    registration_page_form_container = (By.ID, "input_0")

    def fill_registration_form(self, email: str, password: str) -> None:
        """
        Fill the registration form.

        Args:
            email: Email address
            password: Password
        """
        self.enter_text(self.registration_page_email_input, email)
        self.enter_text(self.registration_page_password_input, password)
        logger.info(f"Registration form filled: {email}")

    def submit_registration(self) -> None:
        """Submit the registration form."""
        self.click_element(self.registration_page_register_button)
        logger.info("Registration form submitted")

    def verify_registration_page_loaded(self) -> bool:
        """
        Verify registration page has loaded by checking for Register button.

        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.registration_page_register_button)

    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for registration page to fully load by verifying button and inputs are ready.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if page loaded, False otherwise
        """
        # Verify button is visible (critical interactive element)
        button_ready = self.wait_for_element_visible(self.registration_page_register_button, timeout)
        # Verify email input is visible (form inputs ready)
        input_ready = self.is_element_visible(self.registration_page_email_input, timeout=1)
        loaded = button_ready and input_ready
        if loaded:
            logger.info("Registration page loaded")
        return loaded
