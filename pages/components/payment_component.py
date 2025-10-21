"""
PaymentComponent Module

This module contains the PaymentComponent class for the Stripe-powered
payment form component.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PaymentComponent(BasePage):
    """
    Page Object Model for the Payment Component (Stripe-powered).

    This component handles payment information collection including:
    - Email and phone
    - Payment method selection
    - Terms acceptance
    """

    # Contact Information
    payment_component_email_display = (By.CLASS_NAME, "ReadOnlyFormField-title")
    payment_component_email_continue_link = (By.CLASS_NAME, "ReadOnlyFormField-actionButton")
    payment_component_phone_input = (By.ID, "phoneNumber")
    payment_component_phone_info_icon = (By.CLASS_NAME, "PhoneNumberInput-tooltipIcon")
    payment_component_text_updates_dropdown = (By.ID, "cstm_fld_TGJZYOzkWaUTMh")

    # Payment Methods
    payment_component_card_payment_radio = (By.ID, "payment-method-accordion-item-title-card")
    payment_component_klarna_payment_radio = (By.ID, "payment-method-accordion-item-title-klarna")
    payment_component_amazon_pay_radio = (By.ID, "payment-method-accordion-item-title-amazon_pay")

    # Terms and Submission
    payment_component_terms_checkbox = (By.ID, "termsOfServiceConsentCheckbox")
    payment_component_terms_of_service_link = (
        By.XPATH,
        "//a[@href='https://www.dutchpet.com/pages/terms-and-conditions']"
    )
    payment_component_privacy_policy_link = (
        By.XPATH,
        "//a[@href='https://www.dutch.com/pages/privacy-policy']"
    )
    payment_component_subscribe_button = (
        By.CSS_SELECTOR,
        "[data-testid='hosted-payment-submit-button']"
    )
    payment_component_authorization_disclaimer_text = (
        By.CLASS_NAME,
        "D_NDnqWc__ConfirmTerms--item"
    )

    # Footer Links
    payment_component_stripe_powered_by_link = (By.XPATH, "//a[@href='https://stripe.com']")
    payment_component_stripe_terms_link = (
        By.XPATH,
        "//a[@href='https://stripe.com/legal/end-users']"
    )
    payment_component_stripe_privacy_link = (By.XPATH, "//a[@href='https://stripe.com/privacy']")

    # Section Headers
    payment_component_payment_method_heading = (By.CLASS_NAME, "PaymentMethod-Heading")

    def enter_phone_number(self, phone: str) -> None:
        """
        Enter phone number.

        Args:
            phone: Phone number to enter
        """
        self.enter_text(self.payment_component_phone_input, phone)
        logger.info(f"Phone number entered: {phone}")

    def select_card_payment(self) -> None:
        """Select card payment method using the accordion button."""
        # The radio input is covered by a button, so click the button instead
        try:
            button = self.driver.find_element(By.XPATH, "//button[@aria-label='Pay with card' or @data-testid='card-accordion-item-button']")
            # Use JavaScript click to avoid interception
            self.driver.execute_script("arguments[0].click();", button)
        except Exception:
            # Fallback to original method
            self.click_element(self.payment_component_card_payment_radio)

        logger.info("Card payment option selected")

    def accept_terms(self) -> None:
        """Check the terms and conditions checkbox."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.payment_component_terms_checkbox)
            )

            checkbox = self.driver.find_element(*self.payment_component_terms_checkbox)

            # Check if already selected
            if not checkbox.is_selected():
                # Use JavaScript click to avoid interception issues
                self.driver.execute_script("arguments[0].click();", checkbox)
        except Exception:
            # Fallback to original method
            if not self.is_element_selected(self.payment_component_terms_checkbox):
                self.click_element(self.payment_component_terms_checkbox)

        logger.info("Terms and conditions accepted")

    def click_subscribe(self) -> None:
        """Click the subscribe button."""
        self.click_element(self.payment_component_subscribe_button)

    def is_subscribe_button_enabled(self) -> bool:
        """
        Check if subscribe button is enabled.

        Returns:
            True if enabled, False otherwise
        """
        return self.is_element_enabled(self.payment_component_subscribe_button)

    def fill_card_details(self, card_number: str, expiry_month: str, expiry_year: str, cvv: str, zip_code: str = "") -> None:
        """
        Fill in card payment details in Stripe iframes.

        Args:
            card_number: Card number
            expiry_month: Expiry month (MM)
            expiry_year: Expiry year (YYYY)
            cvv: CVV/CVC code
            zip_code: Billing ZIP code (optional)
        """
        try:
            # Find and switch to card number iframe
            card_number_iframe = WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame'][title*='card number' i]"))
            )

            # Enter card number
            card_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "cardnumber"))
            )
            card_input.send_keys(card_number)

            # Switch back to main content
            self.driver.switch_to.default_content()

            # Find and switch to expiry iframe
            expiry_iframe = WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame'][title*='expiration' i]"))
            )

            # Enter expiry date (MM/YY format)
            expiry_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "exp-date"))
            )
            expiry_year_short = expiry_year[-2:]  # Get last 2 digits
            expiry_input.send_keys(f"{expiry_month}/{expiry_year_short}")

            # Switch back to main content
            self.driver.switch_to.default_content()

            # Find and switch to CVC iframe
            cvc_iframe = WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame'][title*='cvc' i]"))
            )

            # Enter CVC
            cvc_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "cvc"))
            )
            cvc_input.send_keys(cvv)

            # Switch back to main content
            self.driver.switch_to.default_content()

            # Fill ZIP code if present (may not be in iframe)
            if zip_code:
                try:
                    zip_input = self.driver.find_element(By.ID, "billingPostalCode")
                    zip_input.send_keys(zip_code)
                except:
                    pass  # ZIP field may not be required

        except Exception as e:
            # Make sure we're back to main content even if there's an error
            self.driver.switch_to.default_content()
            raise Exception(f"Error filling card details: {e}") from e

    def wait_for_component_load(self, timeout: int = 15) -> bool:
        """
        Wait for payment component to fully load.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if component loaded, False otherwise
        """
        return self.wait_for_element_visible(self.payment_component_phone_input, timeout)
