"""
IssuesPage Module

This module contains the IssuesPage class for the pet health issues selection page.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List
from utils.logger import setup_logger

logger = setup_logger(__name__)


class IssuesPage(BasePage):
    """Page Object Model for Dutch.com Issues/Symptoms Selection Page."""

    # Issue Card Locators (22 total - using most common ones)
    issues_page_allergy_card = (By.ID, "Allergy")
    issues_page_anxiety_card = (By.ID, "Anxiety")
    issues_page_skin_card = (By.ID, "Skin")
    issues_page_digestive_card = (By.ID, "Digestive")
    issues_page_ears_card = (By.ID, "Ears")
    issues_page_eyes_card = (By.ID, "Eyes")
    issues_page_behavioral_card = (By.ID, "Behavioral")
    issues_page_preventive_care_card = (By.ID, "Preventive care")

    # Navigation & Control Locators
    issues_page_continue_button = (
        By.XPATH,
        "//form[@id='reg-flow-issues-form']//button[@type='submit']"
    )
    issues_page_cards_container = (By.XPATH, "//form[@id='reg-flow-issues-form']/ul")

    def select_issue_by_id(self, issue_name: str) -> None:
        """
        Select an issue by clicking its card (uses ID).

        Args:
            issue_name: Issue name (e.g., 'Allergy', 'Anxiety')
        """
        locator = (By.ID, issue_name)
        self.click_element(locator)

    def select_multiple_issues(self, issue_names: List[str]) -> None:
        """
        Select multiple issues by their names.

        Args:
            issue_names: List of issue names to select
        """
        for issue_name in issue_names:
            self.select_issue_by_id(issue_name)
        logger.info(f"Selected issues: {', '.join(issue_names)}")

    def is_issue_selected(self, issue_name: str) -> bool:
        """
        Check if an issue is selected.

        Args:
            issue_name: Issue name to check

        Returns:
            True if selected, False otherwise
        """
        checkbox_locator = (By.ID, f"checkbox-{issue_name}")
        return self.is_element_selected(checkbox_locator)

    def click_continue(self) -> None:
        """Click the continue button."""
        self.click_element(self.issues_page_continue_button)
        logger.info("Issues selection submitted")

    def is_continue_enabled(self) -> bool:
        """
        Check if continue button is enabled.

        Returns:
            True if enabled, False otherwise
        """
        return self.is_element_enabled(self.issues_page_continue_button)

    def verify_issues_page_loaded(self) -> bool:
        """
        Verify issues page has loaded by checking for Continue button.

        Returns:
            True if loaded, False otherwise
        """
        return self.is_element_visible(self.issues_page_continue_button)

    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for issues page to fully load by verifying button and issue cards are ready.

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if page loaded, False otherwise
        """
        # Verify button is visible (critical interactive element)
        button_ready = self.wait_for_element_visible(self.issues_page_continue_button, timeout)
        # Verify issue cards are visible (form inputs ready)
        cards_ready = self.is_element_visible(self.issues_page_allergy_card, timeout=1)
        return button_ready and cards_ready
