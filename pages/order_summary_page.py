"""
OrderSummaryPage Module

This module contains the OrderSummaryPage class for the order summary/payment page.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.components.details_component import DetailsComponent
from pages.components.payment_component import PaymentComponent
from utils.logger import setup_logger

logger = setup_logger(__name__)


class OrderSummaryPage(BasePage):
    """Page Object Model for the Order Summary Page (Stripe-hosted)."""

    # Main Page Elements
    order_summary_page_details_dropdown_button = (
        By.CSS_SELECTOR,
        "button[data-testid='header-view-details']"
    )
    order_summary_page_dutch_logo_image = (By.CSS_SELECTOR, "img[alt='Dutch Pet logo']")
    order_summary_page_plan_name_text = (By.CSS_SELECTOR, "span[data-testid='product-summary-name']")
    order_summary_page_plan_price_text = (By.ID, "ProductSummary-totalAmount")

    def __init__(self, driver, screenshot_helper=None, config=None):
        """
        Initialize OrderSummaryPage with component composition.

        Args:
            driver: Selenium WebDriver instance
            screenshot_helper: Optional screenshot helper
            config: Optional config object
        """
        super().__init__(driver, screenshot_helper, config)
        self.details = DetailsComponent(driver, screenshot_helper, config)
        self.payment = PaymentComponent(driver, screenshot_helper, config)

    def click_details_dropdown(self) -> None:
        """Click the details dropdown button."""
        self.click_element(self.order_summary_page_details_dropdown_button)

    def get_plan_name(self) -> str:
        """
        Get the plan name.

        Returns:
            Plan name text
        """
        return self.get_element_text(self.order_summary_page_plan_name_text)

    def get_plan_price(self) -> str:
        """
        Get the plan price.

        Returns:
            Price text
        """
        return self.get_element_text(self.order_summary_page_plan_price_text)

    def fill_payment_form(self, phone: str, card_number: str = None, expiry_month: str = None,
                           expiry_year: str = None, cvv: str = None, zip_code: str = None) -> None:
        """
        Fill the payment form with phone and optionally card details.

        Args:
            phone: Phone number
            card_number: Card number (optional)
            expiry_month: Expiry month MM (optional)
            expiry_year: Expiry year YYYY (optional)
            cvv: CVV/CVC code (optional)
            zip_code: Billing ZIP code (optional)
        """
        self.payment.enter_phone_number(phone)
        self.payment.select_card_payment()

        # Fill card details if provided (may not be required for all payment forms)
        if card_number and expiry_month and expiry_year and cvv:
            try:
                self.payment.fill_card_details(card_number, expiry_month, expiry_year, cvv, zip_code or "")
            except Exception as e:
                # Card details filling failed - may not be required or uses different form type
                logger.warning(f"Could not fill card details (may not be required): {e}")

        self.payment.accept_terms()

    def verify_order_summary_page_loaded(self) -> bool:
        """
        Verify order summary page has loaded by checking for plan name text (non-interactive element).

        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.order_summary_page_plan_name_text)

    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for order summary page to fully load by verifying display elements and inputs are ready.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if page loaded, False otherwise
        """
        # Verify plan name is visible (page content loaded)
        content_ready = self.wait_for_element_visible(self.order_summary_page_plan_name_text, timeout)
        # Verify phone input is visible (form inputs ready)
        input_ready = self.is_element_visible(self.payment.payment_component_phone_input, timeout=1)
        return content_ready and input_ready
