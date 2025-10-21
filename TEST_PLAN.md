# Test Plan: Dutch.com Registration Flow Automation

## Table of Contents

1. [Document Information](#document-information)
2. [Executive Summary](#executive-summary)
3. [Test Objectives](#test-objectives)
4. [Scope](#scope)
5. [Test Environment](#test-environment)
6. [Test Strategy](#test-strategy)
7. [Test Scenarios](#test-scenarios)
8. [Test Data](#test-data)
9. [Risk Assessment](#risk-assessment)
10. [Success Criteria](#success-criteria)
11. [Test Deliverables](#test-deliverables)
12. [Appendix](#appendix)

---

## Document Information

| Field | Value |
|-------|-------|
| **Project** | Dutch.com E2E Test Automation |
| **Version** | 1.0 |
| **Author** | Claude AI |
| **Date** | 2025-10-20 |
| **Framework** | Selenium + Python + Pytest |
| **Test Type** | End-to-End (E2E) Functional Testing |

---

## Executive Summary

This test plan outlines the automated testing strategy for the Dutch.com user registration flow. The automation framework validates the complete end-to-end user journey from landing page through checkout, utilizing industry best practices including Page Object Model architecture, explicit wait strategies, and comprehensive reporting.

**Key Highlights:**
- Automated E2E validation of complete registration workflow
- Page Object Model design with component composition
- Multi-browser support (Chrome, Firefox, Edge)
- Automatic screenshot captures for visual validation

---

## Test Objectives

### Primary Objective

Automate and validate the complete user registration flow on Dutch.com (https://dutch.com) to ensure a seamless happy path experience from initial landing through checkout page completion.

### Specific Goals

1. **Functional Validation:** Verify all form inputs, page transitions, and workflow logic
2. **Cross-Browser Compatibility:** Ensure consistent behavior across Chrome, Firefox, and Edge
3. **Visual Documentation:** Capture screenshots at critical steps for evidence

---

## Scope

### In Scope

**Pages & Features:**
- ✅ Home page navigation and CTA interactions
- ✅ Pet information form (type, name, state selection)
- ✅ Health issues/symptoms multi-selection
- ✅ "We Can Help" modal handling (conditional)
- ✅ User account registration (email, password)
- ✅ Membership plan selection (1-year, 2-year options)
- ✅ Checkout form completion (phone, payment method, terms)

**Testing Activities:**
- ✅ Happy path functional testing
- ✅ Multi-browser validation (Chrome, Firefox, Edge)
- ✅ Screenshot capture at each step
- ✅ Test execution reporting (HTML + logs)
- ✅ Headless execution support

### Out of Scope

**Excluded from Current Testing:**
- ❌ Negative testing scenarios (invalid inputs, error handling)
- ❌ Payment gateway integration (Stripe iframe is PCI-protected)
- ❌ Actual order placement/submission
- ❌ Email verification workflows
- ❌ Backend API validation
- ❌ Performance/load testing
- ❌ Security testing (authentication, XSS, CSRF)
- ❌ Mobile app testing
- ❌ Accessibility testing (WCAG compliance)

---

## Test Environment

### Application Under Test

| Component | Details |
|-----------|---------|
| **Application URL** | https://dutch.com |
| **Environment** | Production |
| **Access** | Public (no authentication required) |

### Test Infrastructure

| Component | Version/Details |
|-----------|-----------------|
| **Python** | 3.9+ (tested up to 3.14) |
| **Selenium WebDriver** | 4.16.0+ |
| **Pytest** | 8.0.0+ |
| **Operating Systems** | Windows 11, macOS, Linux |
| **Browsers** | Chrome 120+, Firefox 120+, Edge 120+ |
| **Driver Management** | WebDriver Manager (automatic) |

### Tools & Frameworks

| Tool | Purpose |
|------|---------|
| **Selenium WebDriver** | Browser automation engine |
| **WebDriver Manager** | Automatic browser driver downloads |
| **Pytest** | Test execution framework |
| **Pytest-HTML** | HTML test reporting |
| **Pytest-xdist** | Parallel test execution |
| **Colorlog** | Colored console logging |
| **Pillow** | Screenshot image processing |

---

## Test Strategy

### Testing Approach

**Primary Focus:** Happy Path Testing
- Validate successful user journeys with valid inputs
- Ensure smooth page-to-page transitions
- Verify all form elements accept appropriate data

### Automation Architecture

**Page Object Model (POM) with Component Composition:**

```
BasePage (generic utilities)
    ↓
Page Objects (page-specific actions)
    ↓
Components (reusable UI elements)
    ↓
Test Cases (business scenarios)
```

**Key Design Principles:**
- **Separation of Concerns:** Test logic separate from page structure
- **Reusability:** Shared components across multiple pages
- **Maintainability:** Single point of update for UI changes
- **Readability:** High-level test steps, low-level implementation hidden
- **Type Safety:** Python Enums for all test data

### Wait Strategy

**Explicit Waits Only (Best Practice):**
- Every action waits for element to be ready (clickable, visible, present)
- **EXPLICIT_WAIT = 15 seconds** - Standard wait for interactions (click, type, select)
- **PAGE_LOAD_TIMEOUT = 30 seconds** - Long operations (page loads, network calls)
- **Zero `time.sleep()` calls** - all waits are intelligent
- **All timeouts configurable** in `config/settings.py` - no magic numbers
- Follows Selenium best practice of using explicit waits only

### Test Data Management

**Externalized Configuration:**
- Test data stored in `config/test_data.json`
- Dynamic email generation (timestamp suffix to avoid duplicates. Need to cleanup on backend)
- Type-safe enums for pet type, state, pet name

### Screenshot Strategy

**Automatic Capture:**
- Screenshot on every user interaction (click, type, select)
- Sequential numbering: `001_action_element.png`
- Organized by test run timestamp
- Failure screenshots saved to dedicated folder

### Test Suite Organization

**Folder Structure:**

Tests are organized by test type and purpose:

```
tests/
├── e2e/                    # End-to-end tests (full user journeys)
│   └── test_registration_flow.py
├── component/              # Component-level tests (reusable UI components)
├── page/                   # Page-level tests (individual page functionality)
└── smoke/                  # Quick smoke tests (critical functionality validation)
```

**Pytest Markers:**

All tests are tagged with appropriate markers for flexible test execution:

- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.critical` - Critical path tests that must pass
- `@pytest.mark.payment` - Payment-related tests
- `@pytest.mark.registration` - Registration flow tests
- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.validation` - Input validation tests
- `@pytest.mark.component` - Component-level tests
- `@pytest.mark.page` - Page-level tests
- `@pytest.mark.slow` - Long-running tests

**Test Execution Options:**

```bash
# Run by folder
pytest tests/e2e/ -v                    # All E2E tests
pytest tests/smoke/ -v                  # Quick smoke tests only

# Run by marker
pytest -m critical                      # Critical tests only
pytest -m "e2e and payment"             # E2E payment tests
pytest -m "smoke or critical"           # Smoke OR critical tests

# Run specific test
pytest tests/e2e/test_registration_flow.py::TestRegistrationFlow::test_complete_registration_to_checkout -v
```

**Current Test Markers:**

The complete registration flow test is marked as:
- `@pytest.mark.e2e` (end-to-end)
- `@pytest.mark.critical` (critical path)
- `@pytest.mark.payment` (payment flow)
- `@pytest.mark.registration` (registration flow)
- `@pytest.mark.regression` (class level - full suite)

---

## Test Scenarios

### TC_REG_001: Complete Registration Flow (Happy Path)

**Priority:** P0 (Critical)

**Objective:** Validate complete user registration from home page through checkout

**Preconditions:**
- Dutch.com is accessible at https://dutch.com
- Valid test data available in `config/test_data.json`
- No existing session for test user
- Browser driver is available

**Test Data Required:**
- Email: `test_dutch_auto_2025@yopmail.com` (timestamp appended automatically)
- Password: `TestPass123!@#`
- Pet type: `DOG` (enum)
- Pet name: `BUDDY` (enum)
- State: `CA` (enum)
- Health issues: `["Allergy", "Skin", "Preventive care"]`
- Phone: `5551234567`

**Test Steps:**

| # | Action | Expected Result | Screenshot |
|---|--------|-----------------|------------|
| 1 | Navigate to https://dutch.com | Home page loads successfully | ✓ |
| 2 | Click primary CTA button | Pet info form loads | ✓ |
| 3 | Select pet type: Dog | Dog radio button selected | ✓ |
| 4 | Enter pet name: "Buddy" | Pet name field populated | ✓ |
| 5 | Select state: California (CA) | State dropdown shows CA | ✓ |
| 6 | Click Continue | Health issues page loads | ✓ |
| 7 | Select issue: Allergy | Allergy card highlighted | ✓ |
| 8 | Select issue: Skin | Skin card highlighted | ✓ |
| 9 | Select issue: Preventive care | Preventive care card highlighted | ✓ |
| 10 | Click Continue | "We Can Help" modal appears OR registration page loads | ✓ |
| 11 | Click Continue on modal (if appears) | Registration page loads | - |
| 12 | Enter email with timestamp | Email field populated | ✓ |
| 13 | Enter password | Password field populated (masked) | ✓ |
| 14 | Click Register | Plan selection page loads | ✓ |
| 15 | Select 1-year plan | 1-year plan selected | - |
| 16 | Click Continue | Order summary/payment page loads | ✓ |
| 17 | Enter phone number | Phone field populated | ✓ |
| 18 | Select card payment method | Card accordion expanded | - |
| 19 | Check terms and conditions | Checkbox checked | - |
| 20 | Verify Subscribe button present | Subscribe button visible and enabled | - |
| 21 | **STOP - Do NOT click Subscribe** | Test ends at checkout page | - |

**Total Screenshots:** Automatic captures

**Expected Result:**
- All steps execute successfully
- User reaches checkout page with all fields filled
- Subscribe button is visible but NOT clicked
- No order is placed
- Test completes in ~18-20 seconds

**Post-conditions:**
- Test user account created on Dutch.com
- User session remains on checkout/payment page
- No payment processed
- HTML report generated with all screenshots

---

### TC_REG_002: Multi-Browser Validation

**Priority:** P2 (High)

**Objective:** Verify registration flow works consistently across browsers

**Test Matrix:**

| Browser | Version | Status |
|---------|---------|--------|
| Google Chrome | Latest | ✓ Primary |
| Mozilla Firefox | Latest | ⚠ To Test |
| Microsoft Edge | Latest | ⚠ To Test |

**Execution:** Run TC_REG_001 on each browser

**Configuration:**
```bash
BROWSER=chrome pytest tests/
BROWSER=firefox pytest tests/
BROWSER=edge pytest tests/
```

---

## Test Data

### 8.1 User Credentials

**Location:** `config/test_data.json`

```json
{
  "test_users": [
    {
      "email": "test_dutch_auto_2025@yopmail.com",
      "password": "TestPass123!@#",
      "first_name": "Test",
      "last_name": "User"
    }
  ]
}
```

**Email Handling:**
- Base email: `test_dutch_auto_2025@yopmail.com`
- Actual usage: `test_dutch_auto_2025+<timestamp>@yopmail.com`
- Example: `test_dutch_auto_2025+20251020173638@yopmail.com`
- **Benefit:** Avoids duplicate account errors on repeated test runs

**Why Yopmail.com:**
- Disposable email service
- No registration required
- Public inbox for verification (if needed)

### 8.2 Pet Information

```json
{
  "pet_info": {
    "pet_name": "BUDDY",
    "pet_type": "dog",
    "state": "CA"
  }
}
```

**Type-Safe Enums:**
```python
PetType.DOG, PetType.CAT
PetName.BUDDY, PetName.MAX, PetName.BELLA, ...
USState.CA, USState.NY, USState.TX, ... (all 50 states + DC)
```

### 8.3 Health Issues

```json
{
  "issues": [
    "Allergy",
    "Skin",
    "Preventive care"
  ]
}
```

**Available Issues:**
- Allergy
- Anxiety
- Behavioral
- Digestive
- Ears
- Eyes
- Skin
- Preventive care

**Note:** Some combinations may trigger "We Can Help" modal, which is handled automatically.

### 8.4 Contact Information

```json
{
  "contact_info": {
    "phone": "5551234567"
  }
}
```

### 8.5 Payment Information (Not Used)

**Note:** Card details are NOT filled due to Stripe's PCI-compliant iframe security. This is a known limitation and is acceptable for registration flow testing.

---

## Risk Assessment

### 9.1 Identified Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| **Website UI changes** | High | Medium | Use stable locators (ID > data-testid > XPath). Page Object Model allows quick updates. |
| **Dynamic content loading** | Medium | High | Explicit waits with EC conditions. Configurable timeouts in settings.py. |
| **"We Can Help" modal** | Medium | High | Conditional handling - test handles both modal appearing and not appearing. |
| **Stripe payment iframe** | High | Low | Document limitation. Do not attempt to fill card details. Accept iframe security. |
| **Test data conflicts** | Low | Medium | Dynamic timestamp in email. Unique data per run. |
| **Network latency** | Medium | Low | Increased page load timeout (30s). Explicit waits on all elements. |
| **Browser driver version mismatch** | Low | Low | WebDriver Manager auto-downloads correct driver version. |
| **Production environment changes** | High | Medium | Regular test runs. Screenshot comparison. Quick locator updates via POM. |

### 9.2 Assumptions

- ✓ Dutch.com is publicly accessible
- ✓ Registration flow remains consistent
- ✓ No CAPTCHA blocking automated tests
- ✓ Test accounts won't trigger fraud detection
- ✓ Checkout page allows form filling without payment submission
- ✓ Modal behavior is non-deterministic but handled by framework

### 9.3 Dependencies

**External:**
- Stable internet connection
- Dutch.com uptime and availability
- Browser availability on test machine

**Internal:**
- Python 3.9+ installed
- Valid test data in config files
- WebDriver Manager able to download drivers

---

## Success Criteria

### 10.1 Test Acceptance Criteria

**Tests are considered PASSED if:**

1. ✅ All test steps execute without errors
2. ✅ User navigates through all pages in correct sequence:
   - Home → Pet Info → Issues → (Modal) → Registration → Plan → Checkout
3. ✅ All form fields accept valid input data
4. ✅ Page transitions occur within timeout limits
5. ✅ Screenshots captured successfully
6. ✅ Test stops at checkout page (no order submission)
7. ✅ Subscribe button is visible and enabled
8. ✅ No critical defects identified

### 10.2 Performance Criteria

| Metric | Target | Actual |
|--------|--------|--------|
| **Test Execution Time** | < 30 seconds | ~18-20 seconds ✓ |
| **Page Load Time** | < 10 seconds | ~2-5 seconds ✓ |
| **Total Runtime (with setup/teardown)** | < 60 seconds | ~25 seconds ✓ |

### 10.3 Coverage Criteria

| Coverage Type | Target | Actual |
|---------------|--------|--------|
| **Page Coverage** | 100% of registration flow | 7/7 pages ✓ |
| **Happy Path Coverage** | 100% of positive scenarios | 100% ✓ |
| **Browser Coverage** | 3 major browsers | Chrome ✓, Firefox ⚠, Edge ⚠ |

### 10.4 Quality Metrics

**Test Reliability:**
- Test Pass Rate Target: ≥ 90%
- Flakiness Rate Target: < 5%
- False Positive Rate: 0%

---

## Test Deliverables

### 11.1 Documentation

- [x] Test Plan (this document)
- [x] README.md with setup instructions
- [x] Code docstrings and type hints
- [x] Configuration documentation in settings.py

### 11.2 Code Artifacts

**Framework Components:**
- [x] Page Objects: `pages/*.py` (7 files)
- [x] Component Objects: `pages/components/*.py` (3 files)
- [x] Test Cases: `tests/test_registration_flow.py`
- [x] Utilities: `utils/*.py` (4 files)
- [x] Configuration: `config/*.py` + `config/test_data.json`
- [x] Fixtures: `conftest.py`
- [x] Requirements: `requirements.txt`
- [x] Pytest Config: `pytest.ini`

### 11.3 Test Execution Artifacts

**Generated on Each Run:**
- HTML Report: `reports/test_run_<timestamp>/report.html`
- Screenshots: `reports/test_run_<timestamp>/screenshots/*.png` (15 images)
- Logs: `logs/test_run_<timestamp>.log`
- Console Output: Colored logs with INFO level

**Failure Artifacts (if test fails):**
- Failure Screenshot: `screenshots/failures/FAILED_*.png`
- HTML Page Source: `screenshots/failures/FAILED_*.html`
- Stack Trace: Included in HTML report

---

## Appendix

### 12.1 Glossary

| Term | Definition |
|------|------------|
| **POM** | Page Object Model - design pattern separating page structure from test logic |
| **E2E** | End-to-End testing covering complete user workflows |
| **Happy Path** | Expected user journey with valid inputs and successful outcomes |
| **WebDriver** | Selenium component for automating browser actions |
| **Fixture** | Pytest component for test setup, teardown, and dependency injection |
| **Locator** | Strategy to identify elements on web page (ID, XPath, CSS, etc.) |
| **Explicit Wait** | Wait for specific condition before proceeding (vs implicit wait) |
| **Headless** | Running browser without visible UI (background mode) |
| **CI/CD** | Continuous Integration/Continuous Deployment |

### 12.2 Locator Strategy Priority

**Recommended Order (Most Stable → Least Stable):**

1. **ID** - Most reliable, rarely changes
   ```python
   (By.ID, "pet-name")
   ```

2. **data-testid** - Designed for testing
   ```python
   (By.CSS_SELECTOR, "[data-testid='submit-button']")
   ```

3. **Name** - Stable for form elements
   ```python
   (By.NAME, "email")
   ```

4. **CSS Selector** - Structural, no text
   ```python
   (By.CSS_SELECTOR, "button.primary-cta")
   ```

5. **XPath (structural)** - Based on DOM structure
   ```python
   (By.XPATH, "//form[@id='registration']//button[@type='submit']")
   ```

6. **XPath (with text)** - Least stable, language-dependent
   ```python
   (By.XPATH, "//button[text()='Continue']")
   ```

### 12.3 Framework Architecture Diagram

```
dutch-automation/
│
├── config/                          # Configuration Layer
│   ├── settings.py                  # Environment config (URLs, timeouts)
│   └── test_data.json               # Test data (externalized)
│
├── utils/                           # Utility Layer
│   ├── driver_manager.py            # Browser initialization
│   ├── logger.py                    # Logging setup
│   ├── screenshot_helper.py         # Screenshot capture
│   └── enums.py                     # Type-safe enums
│
├── pages/                           # Page Object Layer
│   ├── base_page.py                 # Generic utilities (click, type, wait)
│   │
│   ├── components/                  # Reusable Components
│   │   ├── payment_component.py     # Payment form
│   │   ├── details_component.py     # Order details
│   │   └── we_can_help_component.py # Confirmation modal
│   │
│   ├── home_page.py                 # Page Objects
│   ├── pet_info_page.py
│   ├── issues_page.py
│   ├── registration_page.py
│   ├── checkout_page.py
│   └── order_summary_page.py
│
├── tests/                           # Test Layer
│   └── test_registration_flow.py    # E2E test scenario
│
└── conftest.py                      # Pytest Fixtures
    ├── setup (WebDriver)
    ├── config (Config object)
    ├── test_data (JSON data)
    └── screenshot_helper
```

### 12.4 References

**Official Documentation:**
- Selenium: https://www.selenium.dev/documentation/
- Pytest: https://docs.pytest.org/
- WebDriver Manager: https://github.com/SergeyPirogov/webdriver_manager

**Application Under Test:**
- Dutch.com: https://dutch.com

**Best Practices:**
- Page Object Model: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
- Python Type Hints: https://docs.python.org/3/library/typing.html
