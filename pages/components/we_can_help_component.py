"""
WeCanHelpComponent Module

This module contains the WeCanHelpComponent class for the confirmation modal
that appears after selecting pet health issues.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import setup_logger

logger = setup_logger(__name__)


class WeCanHelpComponent(BasePage):
    """
    Page Object Model for the 'We Can Help' confirmation modal.

    This modal appears after selecting pet health issues to confirm that
    Dutch can help with the selected conditions.
    """

    # Modal Container Elements
    we_can_help_component_modal_container = (
        By.XPATH,
        "//div[contains(@class, 'vfm__content') and contains(@class, 'vfm-bounce-back')]"
    )

    # Navigation Elements
    we_can_help_component_back_button = (
        By.XPATH,
        "//div[contains(@class, 'flex') and contains(@class, 'cursor-pointer') and contains(@class, 'gap-3')]"
    )

    # Image Elements
    we_can_help_component_pet_image = (
        By.XPATH,
        "//img[contains(@class, 'h-[180px]') and contains(@class, 'w-[172px]')]"
    )

    we_can_help_component_checkmark_icon = (
        By.XPATH,
        "//svg[contains(@class, 'lucide-circle-check')]"
    )

    # Text Content Elements
    we_can_help_component_main_heading = (
        By.XPATH,
        "//h3[contains(@class, 'text-[28px]') and contains(@class, 'leading-none')]"
    )

    we_can_help_component_description_text = (
        By.XPATH,
        "//p[contains(@class, 'text-pretty') and contains(@class, 'leading-tight') and contains(@class, 'md:text-xl')]"
    )

    # Action Elements
    we_can_help_component_continue_button = (
        By.XPATH,
        "//div[contains(@class, 'vfm__content')]//button[contains(@class, 'rounded-full') and contains(@class, 'bg-black') and text()='Continue']"
    )

    def click_continue(self) -> None:
        """Click the continue button using JavaScript to avoid modal overlay issues."""
        # Wait for button to be present and visible (ensures modal animation completed)
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.we_can_help_component_continue_button)
        )

        # Use JavaScript click (no scrolling - button is already in modal view)
        self.driver.execute_script("arguments[0].click();", button)
        logger.info("'We Can Help' modal continue button clicked")

    def click_back(self) -> None:
        """Click the back button."""
        self.click_element(self.we_can_help_component_back_button)

    def is_modal_visible(self) -> bool:
        """
        Check if modal is visible.

        Returns:
            True if visible, False otherwise
        """
        visible = self.is_element_visible(self.we_can_help_component_modal_container)
        if visible:
            logger.info("'We Can Help' modal appeared")
        return visible

    def get_heading_text(self) -> str:
        """
        Get the heading text (includes dynamic pet name).

        Returns:
            Heading text
        """
        return self.get_element_text(self.we_can_help_component_main_heading)

    def wait_for_component_load(self, timeout: int = 15) -> bool:
        """
        Wait for component to fully load.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if component loaded, False otherwise
        """
        return self.wait_for_element_visible(self.we_can_help_component_continue_button, timeout)

    def handle_modal_if_present(self) -> bool:
        """
        Handle the 'We Can Help' modal if it appears by dismissing it.

        Returns:
            True if modal was handled, False if modal didn't appear
        """
        try:
            if self.is_modal_visible():
                self.click_continue()
                logger.info("'We Can Help' modal dismissed successfully")
                return True
            logger.info("'We Can Help' modal did not appear - continuing directly")
            return False
        except Exception as e:
            logger.warning(f"'We Can Help' modal not found or error: {e}")
            return False
