"""
NeedInfoComponent Module

This module contains the NeedInfoComponent class for the Washington state
veterinarian information requirement modal.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class NeedInfoComponent(BasePage):
    """
    Page Object Model for the Need Info component.

    This modal appears for Washington state users requiring vet information
    before prescribing medications.
    """

    # Container elements
    need_info_component_header_section = (
        By.XPATH,
        "//div[contains(@class, 'bg-cream') and contains(@class, 'border-b border-black')]"
    )

    need_info_component_content_container = (
        By.XPATH,
        "//div[contains(@class, 'space-y-4 p-6') and contains(@class, 'md:space-y-8')]"
    )

    # Navigation elements
    need_info_component_back_button = (
        By.XPATH,
        "//button[@title='Close' and @type='button']"
    )

    need_info_component_continue_button = (
        By.XPATH,
        "//button[@type='button' and contains(@class, 'bg-black') and contains(@class, 'rounded-full')]"
    )

    # Text elements
    need_info_component_main_heading_text = (
        By.XPATH,
        "//div[contains(@class, 'bg-cream')]//h2"
    )

    need_info_component_prescription_requirement_text = (
        By.XPATH,
        "//div[contains(@class, 'max-w-md text-center text-lg leading-snug')]//p[@class='mb-3 lg:mb-6']"
    )

    need_info_component_alternative_option_text = (
        By.XPATH,
        "//div[contains(@class, 'max-w-md text-center text-lg leading-snug')]//p[not(@class)]"
    )

    # Image elements
    need_info_component_pet_image = (
        By.XPATH,
        "//img[contains(@src, 'image_missing_vet_info')]"
    )

    def click_continue(self) -> None:
        """Click the continue button."""
        self.click_element(self.need_info_component_continue_button)

    def click_back(self) -> None:
        """Click the back button."""
        self.click_element(self.need_info_component_back_button)

    def is_component_visible(self) -> bool:
        """
        Check if component is visible.

        Returns:
            True if visible, False otherwise
        """
        return self.is_element_visible(self.need_info_component_header_section)

    def wait_for_component_load(self, timeout: int = 15) -> bool:
        """
        Wait for component to fully load.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if component loaded, False otherwise
        """
        return self.wait_for_element_visible(self.need_info_component_continue_button, timeout)
