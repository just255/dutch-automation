"""
CheckoutPage Module

This module contains the CheckoutPage class for the plan selection/checkout page.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CheckoutPage(BasePage):
    """Page Object Model for Dutch.com Checkout/Plan Selection Page."""

    # Plan Selection Radio Buttons
    checkout_page_plan_1year_radio = (By.ID, "product-7034225590448")
    checkout_page_plan_2years_radio = (By.ID, "product-7705825673392")

    # Continue Button
    checkout_page_continue_button = (By.ID, "register-plan-selection-cta")

    # Promotional Elements
    checkout_page_promo_banner = (By.ID, "pencil-banner-wrapper")

    # FAQ Accordions
    checkout_page_faq_vet_calls = (By.ID, "radix-vue-accordion-trigger-v-0")
    checkout_page_faq_medication_cost = (By.ID, "radix-vue-accordion-trigger-v-2")

    def select_1year_plan(self) -> None:
        """Select the 1-year subscription plan."""
        # Click the parent label since radio button is hidden
        label = self.driver.find_element(By.XPATH, "//label[@for='product-7034225590448']")
        label.click()
        logger.info("1-year plan selected")

    def select_2year_plan(self) -> None:
        """Select the 2-year subscription plan."""
        # Click the parent label since radio button is hidden
        label = self.driver.find_element(By.XPATH, "//label[@for='product-7705825673392']")
        label.click()
        logger.info("2-year plan selected")

    def click_continue(self) -> None:
        """Click the continue button to proceed to next step."""
        self.click_element(self.checkout_page_continue_button)
        logger.info("Plan selection submitted")

    def get_promo_code(self) -> str:
        """
        Get the promo code from the banner.

        Returns:
            Promo code text
        """
        return self.get_element_text(self.checkout_page_promo_banner)

    def verify_checkout_page_loaded(self) -> bool:
        """
        Verify checkout page has loaded.

        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.checkout_page_plan_1year_radio)

    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for checkout/plan selection page to fully load.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if page loaded, False otherwise
        """
        loaded = self.wait_for_element_visible(self.checkout_page_continue_button, timeout)
        if loaded:
            logger.info("Checkout/plan selection page loaded")
        return loaded
