"""
DetailsComponent Module

This module contains the DetailsComponent class for the order details panel
that displays pricing breakdown, line items, and total calculations.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DetailsComponent(BasePage):
    """
    Page Object Model for the Order Details Component.

    This component displays pricing breakdown for Dutch.com memberships including:
    - Product/membership information
    - Initiation fees
    - Subtotal, tax, and total calculations
    - Promotion code input

    This is a Stripe-hosted component.
    """

    # ==================== COMPONENT LOCATORS ====================

    # Container
    details_component_main_container = (
        By.CSS_SELECTOR,
        "section[data-testid='order-details-mobile']"
    )

    # Header Elements
    details_component_close_button = (
        By.CSS_SELECTOR,
        "button.u-screenReaderOnly"
    )

    # Line Items
    details_component_product_icon = (
        By.CSS_SELECTOR,
        "div[data-testid='line-item-image'] img.LineItem-image"
    )

    details_component_product_name_text = (
        By.CSS_SELECTOR,
        "div.LineItem-productName[data-testid='line-item-product-name']"
    )

    details_component_billing_frequency_text = (
        By.CSS_SELECTOR,
        "span[data-testid='line-item-billing-interval']"
    )

    details_component_product_price_text = (
        By.XPATH,
        "(//div[@data-testid='line-item-total-amount'])[1]"
    )

    details_component_initiation_fee_label_text = (
        By.XPATH,
        "(//div[@data-testid='line-item-product-name'])[2]"
    )

    details_component_initiation_fee_amount_text = (
        By.XPATH,
        "(//div[@data-testid='line-item-total-amount'])[2]"
    )

    # Footer - Subtotal Section
    details_component_subtotal_label_text = (
        By.XPATH,
        "//div[contains(@class, 'Subtotal')]//span[contains(@class, 'Text-fontWeight--500')]"
    )

    details_component_subtotal_amount_text = (
        By.CSS_SELECTOR,
        "span[data-testid='order-details-footer-subtotal-amount']"
    )

    # Promotion Code
    details_component_add_promotion_code_label = (
        By.CSS_SELECTOR,
        "div[class*='PromotionCodeEntry-label']"
    )

    details_component_add_promotion_code_input = (
        By.ID,
        "promotionCode"
    )

    # Tax Section
    details_component_tax_label_text = (
        By.CSS_SELECTOR,
        "span.OrderDetails-subtotalItemLabel-Text"
    )

    details_component_tax_info_icon = (
        By.CSS_SELECTOR,
        "span.OrderDetails-subtotalItemLabel-Text svg.Icon"
    )

    details_component_tax_placeholder_text = (
        By.XPATH,
        "//div[contains(@class, 'OrderDetailsSubtotalItem')]//span[contains(@class, 'Text-color--gray400') and contains(@class, 'Text--tabularNumbers')]"
    )

    # Total
    details_component_total_due_label_text = (
        By.XPATH,
        "//div[contains(@class, 'OrderDetails-total')]//span[contains(@class, 'Text-fontWeight--500')]"
    )

    details_component_total_due_amount_text = (
        By.ID,
        "OrderDetails-TotalAmount"
    )

    # ==================== COMPONENT METHODS ====================

    def is_details_component_visible(self) -> bool:
        """
        Check if details component is visible.

        Returns:
            True if visible, False otherwise
        """
        return self.is_element_visible(self.details_component_main_container)

    def click_close_button(self) -> None:
        """Close the details component panel."""
        self.click_element(self.details_component_close_button)

    def get_product_name(self) -> str:
        """
        Get the product/membership name.

        Returns:
            Product name text
        """
        return self.get_element_text(self.details_component_product_name_text)

    def get_billing_frequency(self) -> str:
        """
        Get the billing frequency text.

        Returns:
            Billing frequency (e.g., "Billed annually")
        """
        return self.get_element_text(self.details_component_billing_frequency_text)

    def get_product_price(self) -> str:
        """
        Get the product price.

        Returns:
            Product price text
        """
        return self.get_element_text(self.details_component_product_price_text)

    def get_initiation_fee(self) -> str:
        """
        Get the initiation fee amount.

        Returns:
            Initiation fee text
        """
        return self.get_element_text(self.details_component_initiation_fee_amount_text)

    def get_subtotal(self) -> str:
        """
        Get the subtotal amount.

        Returns:
            Subtotal text
        """
        return self.get_element_text(self.details_component_subtotal_amount_text)

    def get_total_due(self) -> str:
        """
        Get the total due amount.

        Returns:
            Total due text
        """
        return self.get_element_text(self.details_component_total_due_amount_text)

    def enter_promotion_code(self, code: str) -> None:
        """
        Enter a promotion code.

        Args:
            code: Promotion code to enter
        """
        self.enter_text(self.details_component_add_promotion_code_input, code)

    def click_promotion_code_label(self) -> None:
        """Click the promotion code label to expand input."""
        self.click_element(self.details_component_add_promotion_code_label)

    def verify_details_component_loaded(self) -> bool:
        """
        Verify details component has loaded completely.

        Returns:
            True if loaded, False otherwise
        """
        return (self.is_element_visible(self.details_component_main_container) and
                self.is_element_visible(self.details_component_total_due_amount_text))

    def wait_for_component_load(self, timeout: int = 15) -> bool:
        """
        Wait for details component to fully load.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if component loaded, False otherwise
        """
        return self.wait_for_element_visible(self.details_component_total_due_amount_text, timeout)
