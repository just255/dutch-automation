# Payment Component Locator Analysis - Stage 2 Output

## Analysis Summary
This document contains the exact locators for all 17 elements in the Dutch.com Payment Component. The component uses Stripe's payment processing infrastructure with a custom implementation. Note that this appears to be a read-only email state initially - the actual email input may only be editable before reaching this payment screen.

---

## Element Locators (Ready-to-Use Python Selenium Code)

### 1. payment_component_email_display
**Element Type:** Read-only text display (not an input field)
**Visual Context:** Shows "just_255@yahoo.com" with envelope icon
**HTML Snippet:**
```html
<div class="ReadOnlyFormField-title">just_255@yahoo.com</div>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By class name (most specific for this read-only field)
email_display = (By.CLASS_NAME, "ReadOnlyFormField-title")

# Option 2: By XPath using parent container
email_display = (By.XPATH, "//div[@class='ReadOnlyFormField-email']//div[@class='ReadOnlyFormField-title']")

# Option 3: By XPath using form structure
email_display = (By.XPATH, "//form[@id='payment-form']//div[@class='ReadOnlyFormField-title']")
```

**Important Note:** This is NOT an editable input field. It's a read-only display. Email is likely set in a previous step.

---

### 2. payment_component_email_continue_link
**Element Type:** Button (styled as link)
**Visual Context:** "Continue with Link" button next to email
**HTML Snippet:**
```html
<button class="Button ReadOnlyFormField-actionButton Button--link Button--checkoutSecondaryLink Button--sm" type="button" style="line-height: 1.3;">
  <div class="flex-container justify-content-center align-items-center">Continue with Link</div>
</button>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By class combination (most specific)
continue_link = (By.CLASS_NAME, "ReadOnlyFormField-actionButton")

# Option 2: By XPath with text content (NOT RECOMMENDED but included for reference)
# Note: Avoid text-based XPaths as per requirements, but this is the most reliable
continue_link = (By.XPATH, "//button[@class='Button ReadOnlyFormField-actionButton Button--link Button--checkoutSecondaryLink Button--sm']")

# Option 3: By CSS Selector
continue_link = (By.CSS_SELECTOR, "button.ReadOnlyFormField-actionButton")
```

---

### 3. payment_component_phone_input
**Element Type:** Input field (tel)
**Visual Context:** Phone number field with country selector and placeholder "(201) 555-0123"
**HTML Snippet:**
```html
<input class="CheckoutInput PhoneNumberInput-input FormFieldGroup-bottomChild CheckoutInput--hasPlaceholderIcon Input Input--empty"
       autocomplete="tel"
       autocorrect="off"
       spellcheck="false"
       id="phoneNumber"
       name="phoneNumber"
       type="tel"
       aria-required="true"
       placeholder="(201) 555-0123"
       aria-invalid="false"
       data-1p-ignore="false"
       data-lp-ignore="false"
       value="">
```

**Recommended Locators (in priority order):**
```python
# Option 1: By ID (BEST - unique identifier)
phone_input = (By.ID, "phoneNumber")

# Option 2: By name attribute
phone_input = (By.NAME, "phoneNumber")

# Option 3: By XPath using ID
phone_input = (By.XPATH, "//input[@id='phoneNumber']")

# Option 4: By type attribute
phone_input = (By.CSS_SELECTOR, "input[type='tel']")
```

---

### 4. payment_component_phone_info_icon
**Element Type:** SVG Icon (within tooltip context)
**Visual Context:** Information icon (i) on the right side of phone field
**HTML Snippet:**
```html
<div class="Tooltip-Context PhoneNumberInput-tooltipIconWrapper" style="padding: 12px; margin: -12px;">
  <svg class="InlineSVG Icon PhoneNumberInput-tooltipIcon Icon--sm Icon--square" focusable="false" width="12" height="12" viewBox="0 0 12 12" fill="none">
    <path d="M6 12C9.28235 12 12 9.28235..." fill="currentColor"></path>
  </svg>
</div>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By class name (most specific)
info_icon = (By.CLASS_NAME, "PhoneNumberInput-tooltipIcon")

# Option 2: By XPath using parent wrapper
info_icon = (By.XPATH, "//div[@class='Tooltip-Context PhoneNumberInput-tooltipIconWrapper']//svg")

# Option 3: By CSS Selector
info_icon = (By.CSS_SELECTOR, "svg.PhoneNumberInput-tooltipIcon")
```

---

### 5. payment_component_text_updates_dropdown
**Element Type:** Select dropdown
**Visual Context:** Dropdown with label "Text me with updates from vets and other offers"
**HTML Snippet:**
```html
<select id="cstm_fld_TGJZYOzkWaUTMh" name="smsoptin" class="Select-source">
  <option value="" disabled="" hidden=""></option>
  <option value="yes">Yes</option>
  <option value="no">No</option>
</select>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By ID (BEST)
text_updates_dropdown = (By.ID, "cstm_fld_TGJZYOzkWaUTMh")

# Option 2: By name attribute
text_updates_dropdown = (By.NAME, "smsoptin")

# Option 3: By XPath using ID
text_updates_dropdown = (By.XPATH, "//select[@id='cstm_fld_TGJZYOzkWaUTMh']")

# Option 4: By data-qa on parent container
text_updates_dropdown = (By.XPATH, "//div[@data-qa='FormFieldGroup-cstm_fld_TGJZYOzkWaUTMh']//select")
```

---

### 6. payment_component_card_payment_radio
**Element Type:** Radio button
**Visual Context:** "Card" radio with credit card brand icons (Visa, MC, Amex, etc.)
**HTML Snippet:**
```html
<input id="payment-method-accordion-item-title-card"
       aria-checked="false"
       name="payment-method-accordion-item-title"
       type="radio"
       class="RadioButton PaymentMethodFormAccordionItemTitle-radio"
       tabindex="-1"
       value="card">
```

**Recommended Locators (in priority order):**
```python
# Option 1: By ID (BEST)
card_radio = (By.ID, "payment-method-accordion-item-title-card")

# Option 2: By value attribute
card_radio = (By.XPATH, "//input[@type='radio' and @value='card']")

# Option 3: By name and value
card_radio = (By.XPATH, "//input[@name='payment-method-accordion-item-title' and @value='card']")

# Option 4: By data-testid on parent container
card_radio = (By.XPATH, "//div[@data-testid='card-accordion-item']//input[@type='radio']")
```

---

### 7. payment_component_klarna_payment_radio
**Element Type:** Radio button
**Visual Context:** "Klarna" radio with Klarna logo
**HTML Snippet:**
```html
<input id="payment-method-accordion-item-title-klarna"
       aria-checked="false"
       name="payment-method-accordion-item-title"
       type="radio"
       class="RadioButton PaymentMethodFormAccordionItemTitle-radio"
       tabindex="-1"
       value="klarna">
```

**Recommended Locators (in priority order):**
```python
# Option 1: By ID (BEST)
klarna_radio = (By.ID, "payment-method-accordion-item-title-klarna")

# Option 2: By value attribute
klarna_radio = (By.XPATH, "//input[@type='radio' and @value='klarna']")

# Option 3: By name and value
klarna_radio = (By.XPATH, "//input[@name='payment-method-accordion-item-title' and @value='klarna']")

# Option 4: By data-testid on parent container
klarna_radio = (By.XPATH, "//div[@data-testid='klarna-accordion-item']//input[@type='radio']")
```

---

### 8. payment_component_amazon_pay_radio
**Element Type:** Radio button
**Visual Context:** "Amazon Pay" radio with Amazon Pay logo
**HTML Snippet:**
```html
<input id="payment-method-accordion-item-title-amazon_pay"
       aria-checked="false"
       name="payment-method-accordion-item-title"
       type="radio"
       class="RadioButton PaymentMethodFormAccordionItemTitle-radio"
       tabindex="-1"
       value="amazon_pay">
```

**Recommended Locators (in priority order):**
```python
# Option 1: By ID (BEST)
amazon_pay_radio = (By.ID, "payment-method-accordion-item-title-amazon_pay")

# Option 2: By value attribute
amazon_pay_radio = (By.XPATH, "//input[@type='radio' and @value='amazon_pay']")

# Option 3: By name and value
amazon_pay_radio = (By.XPATH, "//input[@name='payment-method-accordion-item-title' and @value='amazon_pay']")

# Option 4: By data-testid on parent container
amazon_pay_radio = (By.XPATH, "//div[@data-testid='amazon_pay-accordion-item']//input[@type='radio']")
```

---

### 9. payment_component_terms_checkbox
**Element Type:** Checkbox
**Visual Context:** Checkbox with label "I agree to Dutch Pet's Terms of Service and Privacy Policy"
**HTML Snippet:**
```html
<input id="termsOfServiceConsentCheckbox"
       name="termsOfServiceConsentCheckbox"
       type="checkbox"
       class="Checkbox-Input">
```

**Recommended Locators (in priority order):**
```python
# Option 1: By ID (BEST)
terms_checkbox = (By.ID, "termsOfServiceConsentCheckbox")

# Option 2: By name attribute
terms_checkbox = (By.NAME, "termsOfServiceConsentCheckbox")

# Option 3: By XPath using ID
terms_checkbox = (By.XPATH, "//input[@id='termsOfServiceConsentCheckbox']")

# Option 4: By type and class
terms_checkbox = (By.CSS_SELECTOR, "input[type='checkbox'].Checkbox-Input")
```

---

### 10. payment_component_terms_of_service_link
**Element Type:** Hyperlink (anchor tag)
**Visual Context:** "Terms of Service" link within checkbox label
**HTML Snippet:**
```html
<a class="Link TermsOfServiceConsentCheckbox-customMessageLink Link--checkout--secondary"
   href="https://www.dutchpet.com/pages/terms-and-conditions"
   target="_blank"
   rel="noopener">Terms of Service</a>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By href attribute (BEST - most unique)
terms_link = (By.XPATH, "//a[@href='https://www.dutchpet.com/pages/terms-and-conditions']")

# Option 2: By class name
terms_link = (By.CLASS_NAME, "TermsOfServiceConsentCheckbox-customMessageLink")

# Option 3: By CSS Selector with href
terms_link = (By.CSS_SELECTOR, "a[href*='terms-and-conditions']")

# Option 4: By partial link text (if needed, though not recommended)
# terms_link = (By.PARTIAL_LINK_TEXT, "Terms of Service")
```

---

### 11. payment_component_privacy_policy_link
**Element Type:** Hyperlink (anchor tag)
**Visual Context:** "Privacy Policy" link within checkbox label
**HTML Snippet:**
```html
<a class="Link TermsOfServiceConsentCheckbox-customMessageLink Link--checkout--secondary"
   href="https://www.dutch.com/pages/privacy-policy"
   target="_blank"
   rel="noopener">Privacy Policy</a>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By href attribute (BEST - most unique)
privacy_link = (By.XPATH, "//a[@href='https://www.dutch.com/pages/privacy-policy']")

# Option 2: By CSS Selector with href
privacy_link = (By.CSS_SELECTOR, "a[href*='privacy-policy']")

# Option 3: By class and href combination
privacy_link = (By.XPATH, "//a[@class='Link TermsOfServiceConsentCheckbox-customMessageLink Link--checkout--secondary' and contains(@href, 'privacy-policy')]")
```

---

### 12. payment_component_subscribe_button
**Element Type:** Submit button
**Visual Context:** Large purple button with "Subscribe" text
**HTML Snippet:**
```html
<button class="SubmitButton SubmitButton--incomplete"
        type="submit"
        data-testid="hosted-payment-submit-button"
        style="background-color: rgb(88, 41, 78); color: rgb(255, 255, 255);">
  <div class="SubmitButton-Shimmer"...></div>
  <div class="SubmitButton-TextContainer">
    <span class="SubmitButton-Text SubmitButton-Text--current Text Text-color--default Text-fontWeight--500 Text--truncate"
          aria-hidden="false">Subscribe</span>
    <span class="SubmitButton-Text SubmitButton-Text--pre Text Text-color--default Text-fontWeight--500 Text--truncate"
          aria-hidden="true"
          data-testid="submit-button-processing-label">Processing...</span>
  </div>
  ...
</button>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By data-testid (BEST - explicit test attribute)
subscribe_button = (By.CSS_SELECTOR, "[data-testid='hosted-payment-submit-button']")

# Option 2: By type and class
subscribe_button = (By.CSS_SELECTOR, "button[type='submit'].SubmitButton")

# Option 3: By class name
subscribe_button = (By.CLASS_NAME, "SubmitButton")

# Option 4: By XPath using data-testid
subscribe_button = (By.XPATH, "//button[@data-testid='hosted-payment-submit-button']")
```

---

### 13. payment_component_authorization_disclaimer_text
**Element Type:** Text container (div)
**Visual Context:** "By subscribing, you authorize Dutch Pet to charge you according to the terms until you cancel."
**HTML Snippet:**
```html
<div class="D_NDnqWc__ConfirmTerms--item Text Text-color--gray600 Text-fontSize--13">
  <div>By subscribing, you authorize Dutch Pet to charge you according to the terms until you cancel.</div>
  <div></div>
</div>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By unique class name
disclaimer_text = (By.CLASS_NAME, "D_NDnqWc__ConfirmTerms--item")

# Option 2: By XPath using parent container
disclaimer_text = (By.XPATH, "//div[@class='B4eU5jRx__ConfirmTerms']//div[@class='D_NDnqWc__ConfirmTerms--item Text Text-color--gray600 Text-fontSize--13']")

# Option 3: By CSS Selector with partial class match
disclaimer_text = (By.CSS_SELECTOR, "div[class*='ConfirmTerms--item']")
```

---

### 14. payment_component_stripe_powered_by_link
**Element Type:** Hyperlink with SVG logo
**Visual Context:** "Powered by stripe" text with Stripe logo at bottom
**HTML Snippet:**
```html
<a class="Link Link--primary" href="https://stripe.com" target="_blank" rel="noopener">
  <div class="Text Text-color--gray400 Text-fontSize--12 Text-fontWeight--400">
    Powered by
    <span>
      <svg class="InlineSVG Icon BJN199Au__PoweredByStripe-icon Icon--md" focusable="false" width="33" height="15" role="img" aria-labelledby="stripe-title">
        <title id="stripe-title">Stripe</title>
        ...
      </svg>
    </span>
  </div>
</a>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By href to stripe.com
powered_by_link = (By.XPATH, "//a[@href='https://stripe.com']")

# Option 2: By class on SVG
powered_by_link = (By.XPATH, "//svg[contains(@class, 'PoweredByStripe-icon')]/ancestor::a")

# Option 3: By CSS Selector
powered_by_link = (By.CSS_SELECTOR, "a[href='https://stripe.com']")
```

---

### 15. payment_component_stripe_terms_link
**Element Type:** Hyperlink
**Visual Context:** "Terms" link in footer next to Stripe branding
**HTML Snippet:**
```html
<a class="Link _0wMrLFZH__FooterLink Link--primary"
   href="https://stripe.com/legal/end-users"
   target="_blank"
   rel="noopener">
  <span class="Text Text-color--gray400 Text-fontSize--12 Text-fontWeight--400">Terms</span>
</a>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By href attribute (BEST)
stripe_terms_link = (By.XPATH, "//a[@href='https://stripe.com/legal/end-users']")

# Option 2: By class combination
stripe_terms_link = (By.CLASS_NAME, "_0wMrLFZH__FooterLink")

# Option 3: By CSS Selector
stripe_terms_link = (By.CSS_SELECTOR, "a[href*='stripe.com/legal/end-users']")
```

---

### 16. payment_component_stripe_privacy_link
**Element Type:** Hyperlink
**Visual Context:** "Privacy" link in footer next to Stripe branding
**HTML Snippet:**
```html
<a class="Link _0wMrLFZH__FooterLink Link--primary"
   href="https://stripe.com/privacy"
   target="_blank"
   rel="noopener">
  <span class="Text Text-color--gray400 Text-fontSize--12 Text-fontWeight--400">Privacy</span>
</a>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By href attribute (BEST)
stripe_privacy_link = (By.XPATH, "//a[@href='https://stripe.com/privacy']")

# Option 2: By CSS Selector
stripe_privacy_link = (By.CSS_SELECTOR, "a[href*='stripe.com/privacy']")

# Option 3: By XPath with text content (alternative)
stripe_privacy_link = (By.XPATH, "//footer//a[contains(@href, 'stripe.com/privacy')]")
```

---

### 17. payment_component_payment_method_section
**Element Type:** Container section (h2 heading + form section)
**Visual Context:** Section with "Payment method" heading containing payment radio buttons
**HTML Snippet:**
```html
<h2 class="PaymentMethod-Heading Text Text-color--gray800 Text-fontSize--16 Text-fontWeight--500">Payment method</h2>
```

**Recommended Locators (in priority order):**
```python
# Option 1: By class name for heading
payment_method_heading = (By.CLASS_NAME, "PaymentMethod-Heading")

# Option 2: By XPath for heading element
payment_method_heading = (By.XPATH, "//h2[@class='PaymentMethod-Heading Text Text-color--gray800 Text-fontSize--16 Text-fontWeight--500']")

# Option 3: For the entire payment method form section
payment_method_section = (By.CLASS_NAME, "PaymentMethodForm")

# Option 4: For the accordion container
payment_method_accordion = (By.CLASS_NAME, "PaymentMethodFormAccordion")
```

---

## Additional Important Notes

### Dynamic/Conditional Elements
The following elements are **NOT** present in the captured HTML but may appear when the Card radio button is selected:
- Credit card number input field
- CVV/CVC input field
- Expiration date input field
- Cardholder name input field

These fields are likely loaded dynamically via Stripe's iframe elements. Look for iframes with `name="__privateStripeFrame*"` when Card payment is selected.

### Iframe Elements
The HTML contains Stripe iframe elements for express checkout:
```html
<iframe name="__privateStripeFrame6926"
        frameborder="0"
        allowtransparency="true"
        scrolling="no"
        role="presentation"
        allow="payment *"
        src="https://js.stripe.com/v3/elements-inner-express-checkout-...">
</iframe>
```

These may require switching context in Selenium:
```python
# Switch to Stripe iframe
driver.switch_to.frame(driver.find_element(By.NAME, "__privateStripeFrame6926"))

# Interact with elements inside iframe

# Switch back to main content
driver.switch_to.default_content()
```

### Form Structure
- Main form ID: `payment-form`
- Form is marked with `novalidate=""` attribute
- Payment methods use accordion-style expansion

### Accessibility Attributes
Many elements include ARIA attributes for accessibility:
- `aria-required="true"` on phone input
- `aria-checked="false"` on radio buttons
- `aria-invalid="false"` on validated inputs
- `aria-hidden` for screen reader management

---

## Summary of Best Locators (Quick Reference)

| Element | Best Locator Strategy | Locator Value |
|---------|----------------------|---------------|
| Email Display | CLASS_NAME | `ReadOnlyFormField-title` |
| Continue with Link Button | CLASS_NAME | `ReadOnlyFormField-actionButton` |
| Phone Input | ID | `phoneNumber` |
| Phone Info Icon | CLASS_NAME | `PhoneNumberInput-tooltipIcon` |
| Text Updates Dropdown | ID | `cstm_fld_TGJZYOzkWaUTMh` |
| Card Radio Button | ID | `payment-method-accordion-item-title-card` |
| Klarna Radio Button | ID | `payment-method-accordion-item-title-klarna` |
| Amazon Pay Radio Button | ID | `payment-method-accordion-item-title-amazon_pay` |
| Terms Checkbox | ID | `termsOfServiceConsentCheckbox` |
| Terms of Service Link | XPATH | `//a[@href='https://www.dutchpet.com/pages/terms-and-conditions']` |
| Privacy Policy Link | XPATH | `//a[@href='https://www.dutch.com/pages/privacy-policy']` |
| Subscribe Button | CSS_SELECTOR | `[data-testid='hosted-payment-submit-button']` |
| Authorization Disclaimer | CLASS_NAME | `D_NDnqWc__ConfirmTerms--item` |
| Powered by Stripe Link | XPATH | `//a[@href='https://stripe.com']` |
| Stripe Terms Link | XPATH | `//a[@href='https://stripe.com/legal/end-users']` |
| Stripe Privacy Link | XPATH | `//a[@href='https://stripe.com/privacy']` |
| Payment Method Section | CLASS_NAME | `PaymentMethod-Heading` |

---

## Implementation Example

Here's a complete example of how to use these locators in a Selenium Page Object:

```python
from selenium.webdriver.common.by import By

class PaymentComponentLocators:
    """Locators for Dutch.com Payment Component (Stripe-powered)"""

    # Contact Information
    EMAIL_DISPLAY = (By.CLASS_NAME, "ReadOnlyFormField-title")
    CONTINUE_WITH_LINK_BUTTON = (By.CLASS_NAME, "ReadOnlyFormField-actionButton")
    PHONE_INPUT = (By.ID, "phoneNumber")
    PHONE_INFO_ICON = (By.CLASS_NAME, "PhoneNumberInput-tooltipIcon")
    TEXT_UPDATES_DROPDOWN = (By.ID, "cstm_fld_TGJZYOzkWaUTMh")

    # Payment Methods
    CARD_RADIO = (By.ID, "payment-method-accordion-item-title-card")
    KLARNA_RADIO = (By.ID, "payment-method-accordion-item-title-klarna")
    AMAZON_PAY_RADIO = (By.ID, "payment-method-accordion-item-title-amazon_pay")

    # Terms and Submission
    TERMS_CHECKBOX = (By.ID, "termsOfServiceConsentCheckbox")
    TERMS_OF_SERVICE_LINK = (By.XPATH, "//a[@href='https://www.dutchpet.com/pages/terms-and-conditions']")
    PRIVACY_POLICY_LINK = (By.XPATH, "//a[@href='https://www.dutch.com/pages/privacy-policy']")
    SUBSCRIBE_BUTTON = (By.CSS_SELECTOR, "[data-testid='hosted-payment-submit-button']")
    AUTHORIZATION_DISCLAIMER = (By.CLASS_NAME, "D_NDnqWc__ConfirmTerms--item")

    # Footer Links
    POWERED_BY_STRIPE_LINK = (By.XPATH, "//a[@href='https://stripe.com']")
    STRIPE_TERMS_LINK = (By.XPATH, "//a[@href='https://stripe.com/legal/end-users']")
    STRIPE_PRIVACY_LINK = (By.XPATH, "//a[@href='https://stripe.com/privacy']")

    # Section Headers
    PAYMENT_METHOD_HEADING = (By.CLASS_NAME, "PaymentMethod-Heading")
```

---

## End of Stage 2 Analysis

All 17 elements have been located and documented with production-ready Selenium locators. The locators prioritize:
1. IDs (when available - most reliable)
2. Data attributes (data-testid, data-qa)
3. Unique class names
4. XPath without text() functions
5. CSS selectors as alternatives

**File analyzed:** `E:\Dutch Automation\page_analysis\components\payment\payment.html`
**Date:** 2025-10-18
**Framework:** Selenium with Python
**Locator Strategy:** ID-first, no text-based XPath
