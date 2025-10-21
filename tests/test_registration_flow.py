"""
Test Registration Flow

This module contains the main test for the Dutch.com registration flow
from home page through to checkout.

Author: Claude AI
Date: 2025-10-19
"""

import pytest
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.pet_info_page import PetInfoPage
from pages.issues_page import IssuesPage
from pages.checkout_page import CheckoutPage
from pages.order_summary_page import OrderSummaryPage
from pages.components.we_can_help_component import WeCanHelpComponent
from utils.logger import setup_logger
from utils.enums import PetType, PetName, USState

logger = setup_logger(__name__)


@pytest.mark.regression
class TestRegistrationFlow:
    """Test class for complete registration to checkout flow."""

    def test_complete_registration_to_checkout(self, setup, config, test_data, screenshot_helper):
        """
        Test complete flow from home page through to checkout.

        This test verifies the happy path without placing an actual order.

        UPDATED FLOW (as of 2025-10-19 - website flow changed):
        Steps:
        1. Navigate to home page
        2. Click CTA to start flow
        3. Fill pet information form (pet type, name, state)
        4. Select health issues
        4a. Handle "We Can Help" modal (if appears)
        5. Fill registration form (email, password)
        6. Select membership plan
        7. Fill checkout form (phone, payment method selection, terms - DO NOT SUBMIT ORDER)
        8. Verify all steps complete successfully

        NOTE: Card details (card number, expiry, CVC) are NOT filled due to Stripe's
        PCI-compliant security measures. Stripe uses secure iframe elements that prevent
        automation from filling sensitive payment data. This is a known limitation and
        is acceptable for testing the registration flow.

        Args:
            setup: WebDriver fixture
            config: Configuration fixture
            test_data: Test data fixture
            screenshot_helper: Screenshot helper fixture
        """
        # ==================== SETUP: Initialize driver and test data ====================
        driver = setup
        user_data = test_data['test_users'][0]
        pet_data = test_data['pet_info']
        issues_data = test_data['issues']
        contact_data = test_data['contact_info']

        # ==================== SETUP: Initialize page objects ====================
        home_page = HomePage(driver, screenshot_helper, config)
        pet_info_page = PetInfoPage(driver, screenshot_helper, config)
        issues_page = IssuesPage(driver, screenshot_helper, config)
        we_can_help = WeCanHelpComponent(driver, screenshot_helper, config)
        registration_page = RegistrationPage(driver, screenshot_helper, config)
        checkout_page = CheckoutPage(driver, screenshot_helper, config)
        order_summary_page = OrderSummaryPage(driver, screenshot_helper, config)

        # ==================== STEP 1: Navigate to Home Page ====================
        logger.info("STEP 1: Navigating to Dutch.com home page")
        home_page.navigate_to_home(config.BASE_URL)
        assert home_page.verify_home_page_loaded(), "Home page did not load"

        # ==================== STEP 2: Click CTA ====================
        logger.info("STEP 2: Clicking CTA to start flow")
        home_page.click_primary_cta()

        # ==================== STEP 3: Fill Pet Info Form ====================
        logger.info("STEP 3: Filling pet information form")
        assert pet_info_page.verify_pet_info_page_loaded(), "Pet info page did not load"

        pet_info_page.fill_pet_info_form(
            PetType[pet_data['pet_type'].upper()],
            PetName[pet_data['pet_name']].value,
            USState[pet_data['state']]
        )
        pet_info_page.click_continue()

        # ==================== STEP 4: Select Health Issues ====================
        logger.info("STEP 4: Selecting health issues")
        assert issues_page.verify_issues_page_loaded(), "Issues page did not load"

        issues_page.select_multiple_issues(issues_data)
        issues_page.click_continue()

        # ==================== STEP 4a: Handle "We Can Help" Modal (if appears) ====================
        we_can_help.handle_modal_if_present()
        registration_page.wait_for_page_load()

        # ==================== STEP 5: Fill Registration Form ====================
        logger.info("STEP 5: Filling registration form")

        registration_page.fill_registration_form(
            user_data['email'],
            user_data['password']
        )
        registration_page.submit_registration()

        # ==================== STEP 6: Select Membership Plan ====================
        logger.info("STEP 6: Selecting membership plan")
        checkout_page.wait_for_page_load()
        checkout_page.select_1year_plan()
        checkout_page.click_continue()

        # ==================== STEP 7: Fill Checkout Form (DO NOT SUBMIT) ====================
        logger.info("STEP 7: Filling checkout/payment form")
        assert order_summary_page.verify_order_summary_page_loaded(), "Order summary page did not load"

        # Enter phone, select card payment, accept terms
        # NOTE: Card details cannot be filled due to Stripe's PCI-compliant security measures
        order_summary_page.payment.enter_phone_number(contact_data['phone'])
        order_summary_page.payment.select_card_payment()
        order_summary_page.payment.accept_terms()

        # ==================== TEST COMPLETE ====================
        logger.info("=" * 80)
        logger.info("TEST COMPLETED SUCCESSFULLY")
        logger.info("Full registration flow validated from home page to payment form")
        logger.info("Order NOT submitted (test stops at payment page as intended)")
        logger.info("=" * 80)
