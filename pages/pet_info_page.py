"""
PetInfoPage Module

This module contains the PetInfoPage class for the pet information form.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import setup_logger
from utils.enums import PetType, USState

logger = setup_logger(__name__)


class PetInfoPage(BasePage):
    """Page Object Model for the Pet Information registration page."""

    # Radio Buttons - Pet Type Selection
    pet_info_page_dog_radio_button = (By.ID, "dog")
    pet_info_page_cat_radio_button = (By.ID, "cat")

    # Input Fields
    # NOTE: Dutch.com A/B testing serves different IDs: "pet-name" OR "petName"
    # Using XPath to match either variation
    pet_info_page_pet_name_input = (By.XPATH, "//input[@id='pet-name' or @id='petName']")
    pet_info_page_state_dropdown = (By.ID, "state")

    # Buttons
    # NOTE: Form and button lack unique IDs (preferred for stable locators)
    # Using text-based locator as website structure changed
    pet_info_page_continue_button = (
        By.XPATH,
        "//button[@type='submit' and contains(text(), 'Continue')]"
    )

    def select_dog(self) -> None:
        """Select dog as pet type."""
        self.click_element(self.pet_info_page_dog_radio_button)

    def select_cat(self) -> None:
        """Select cat as pet type."""
        self.click_element(self.pet_info_page_cat_radio_button)

    def enter_pet_name(self, name: str) -> None:
        """
        Enter pet name.

        Args:
            name: Pet's name
        """
        self.enter_text(self.pet_info_page_pet_name_input, name)

    def select_state(self, state: USState) -> None:
        """
        Select pet's home state.

        Args:
            state: US state (USState enum)
        """
        self.select_dropdown_by_value(self.pet_info_page_state_dropdown, state.value)

    def fill_pet_info_form(self, pet_type: PetType, pet_name: str, state: USState) -> None:
        """
        Fill complete pet info form.

        Args:
            pet_type: Pet type (PetType.DOG or PetType.CAT)
            pet_name: Pet's name
            state: US state (USState enum)
        """
        if pet_type == PetType.DOG:
            self.select_dog()
        elif pet_type == PetType.CAT:
            self.select_cat()
        else:
            raise ValueError(f"Invalid pet type: {pet_type}. Must be PetType.DOG or PetType.CAT")

        self.enter_pet_name(pet_name)
        self.select_state(state)
        logger.info(f"Pet info filled: {pet_name} ({pet_type.value}) in {state.value}")

    def click_continue(self) -> None:
        """Click the continue button."""
        self.click_element(self.pet_info_page_continue_button)
        logger.info("Pet info form submitted")

    def verify_pet_info_page_loaded(self) -> bool:
        """
        Verify pet info page has loaded by checking for Continue button.

        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.pet_info_page_continue_button)

    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for pet info page to fully load by verifying button and inputs are ready.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if page loaded, False otherwise
        """
        # Verify button is visible (critical interactive element)
        button_ready = self.wait_for_element_visible(self.pet_info_page_continue_button, timeout)
        # Verify dog radio and pet name input are visible (form inputs ready)
        input_ready = self.is_element_visible(self.pet_info_page_dog_radio_button, timeout=1)
        return button_ready and input_ready
