# Stage 3 Prompt: Write PetInfoPage Class Locators

Based on HTML analysis of the pet information page, write the following locators into the PetInfoPage class file.

## File Location
The locators should be added to the PetInfoPage class (file path to be determined in your project structure).

## HTML Analysis Summary

The pet info page contains a simple registration form with the following structure:
- Form ID: `reg-flow-register`
- Dog radio button ID: `dog`
- Cat radio button ID: `cat`
- Pet name input ID: `pet-name`
- State dropdown ID: `state`
- Radio buttons grouped in a `fieldset` with `role="group"`
- Submit button has `type="submit"` within the form

## Locators to Add

### 1. pet_info_page_dog_radio_button
**Locator Strategy:** ID (highest priority - element has unique ID)

**HTML Structure:**
```html
<label for="dog" class="flex items-center gap-2 rounded-lg bg-cream px-4 py-4">
  <input id="dog" name="pet_type" type="radio" class="" value="dog">
  <p>Dog</p>
</label>
```

**Python Selenium Code:**
```python
DOG_RADIO_BUTTON = (By.ID, "dog")
```

---

### 2. pet_info_page_cat_radio_button
**Locator Strategy:** ID (highest priority - element has unique ID)

**HTML Structure:**
```html
<label for="cat" class="flex items-center gap-2 rounded-lg bg-cream px-4 py-4">
  <input id="cat" name="pet_type" type="radio" class="" value="cat">
  <p>Cat</p>
</label>
```

**Python Selenium Code:**
```python
CAT_RADIO_BUTTON = (By.ID, "cat")
```

---

### 3. pet_info_page_pet_type_radio_group
**Locator Strategy:** XPath (no ID on fieldset, using role attribute)

**HTML Structure:**
```html
<form id="reg-flow-register">
  <fieldset role="group" class="rounded-xl border-[1.25px] border-cream bg-white px-4 py-3 md:p-4">
    <legend>What kind of pet do you have? <span>*</span></legend>
    <div class="mt-2 grid grid-cols-2 gap-x-4">
      <label for="dog">...</label>
      <label for="cat">...</label>
    </div>
  </fieldset>
</form>
```

**Python Selenium Code:**
```python
PET_TYPE_RADIO_GROUP = (By.XPATH, "//form[@id='reg-flow-register']//fieldset[@role='group']")
```

**Alternative (if you need just the container div):**
```python
PET_TYPE_RADIO_GROUP = (By.XPATH, "//fieldset[@role='group']//div[@class='mt-2 grid grid-cols-2 gap-x-4']")
```

---

### 4. pet_info_page_pet_name_input
**Locator Strategy:** ID (highest priority - element has unique ID)

**HTML Structure:**
```html
<div class="input-wrapper input relative w-full rounded-xl border-[1.25px] border-cream bg-white px-4 py-3 md:p-4">
  <label for="pet-name">What's your pet's name?</label>
  <input id="pet-name" required="" type="text" placeholder="Enter pet's name" value="">
</div>
```

**Python Selenium Code:**
```python
PET_NAME_INPUT = (By.ID, "pet-name")
```

---

### 5. pet_info_page_state_dropdown
**Locator Strategy:** ID (highest priority - element has unique ID)

**HTML Structure:**
```html
<div class="rounded-xl border-[1.25px] border-cream bg-white px-4 py-3 md:p-4">
  <label for="state">What state does your pet live in?</label>
  <select id="state" class="cursor-pointer w-full bg-light-cream border-cream !outline-none text-gray-400">
    <option disabled="" selected="" value="">Choose pet's home state</option>
    <option value="AL">Alabama</option>
    <!-- more states -->
  </select>
</div>
```

**Python Selenium Code:**
```python
STATE_DROPDOWN = (By.ID, "state")
```

---

### 6. pet_info_page_continue_button
**Locator Strategy:** XPath (no ID on button, using form context and type)

**HTML Structure:**
```html
<form id="reg-flow-register">
  <!-- form fields -->
  <div class="pt-2 text-center">
    <button type="submit" class="inline-block w-full px-8 py-3 text-center whitespace-nowrap transition-colors duration-300 rounded-full bg-black hover:bg-[#666666] text-white text-xl disabled:bg-cream disabled:text-[#666666]" disabled="">
      Continue
    </button>
  </div>
</form>
```

**Python Selenium Code:**
```python
CONTINUE_BUTTON = (By.XPATH, "//form[@id='reg-flow-register']//button[@type='submit']")
```

---

### 7. pet_info_page_form_container
**Locator Strategy:** ID (highest priority - form has unique ID)

**HTML Structure:**
```html
<form id="reg-flow-register" class="my-4 space-y-5 text-left">
  <fieldset>...</fieldset>
  <div>...</div>
  <!-- all form fields -->
</form>
```

**Python Selenium Code:**
```python
FORM_CONTAINER = (By.ID, "reg-flow-register")
```

---

### 8. pet_info_page_heading_text
**Locator Strategy:** XPath (no ID, using semantic heading tag and structure)

**HTML Structure:**
```html
<div class="px-5">
  <h2 class="font-sans text-[28px] font-normal leading-none sm:text-4xl">
    Let's get to know your pet
  </h2>
  <p>Enter a few basic details to get started with fast, affordable vet care from home.</p>
</div>
```

**Python Selenium Code:**
```python
HEADING_TEXT = (By.XPATH, "//h2[contains(@class, 'font-sans') and contains(@class, 'text-[28px]')]")
```

**Alternative (more specific, parent context):**
```python
HEADING_TEXT = (By.XPATH, "//form[@id='reg-flow-register']/preceding-sibling::div//h2")
```

---

### 9. pet_info_page_description_text
**Locator Strategy:** XPath (no ID, using semantic structure)

**HTML Structure:**
```html
<div class="px-5">
  <h2>Let's get to know your pet</h2>
  <p class="mt-2 text-base sm:mt-5 sm:text-xl">
    Enter a few basic details to get started with fast, affordable vet care from home.
  </p>
</div>
```

**Python Selenium Code:**
```python
DESCRIPTION_TEXT = (By.XPATH, "//p[@class='mt-2 text-base sm:mt-5 sm:text-xl']")
```

**Alternative (using parent h2 as reference):**
```python
DESCRIPTION_TEXT = (By.XPATH, "//h2[contains(@class, 'text-[28px]')]/following-sibling::p[1]")
```

---

### 10. pet_info_page_add_more_pets_note
**Locator Strategy:** XPath (no ID, using fieldset context and class attributes)

**HTML Structure:**
```html
<fieldset role="group">
  <legend>What kind of pet do you have? <span>*</span></legend>
  <div class="mt-2 grid grid-cols-2 gap-x-4">
    <!-- radio buttons -->
  </div>
  <p class="pt-2 text-sm leading-snug text-[#666666]">
    *You can add more pets after registration
  </p>
</fieldset>
```

**Python Selenium Code:**
```python
ADD_MORE_PETS_NOTE = (By.XPATH, "//fieldset[@role='group']//p[@class='pt-2 text-sm leading-snug text-[#666666]']")
```

---

### 11. pet_info_page_pet_type_label
**Locator Strategy:** XPath (no ID, using legend tag within fieldset)

**HTML Structure:**
```html
<fieldset role="group">
  <legend class="contents pr-8 text-left text-lg font-bold leading-tight">
    What kind of pet do you have? <span class="text-brown">*</span>
  </legend>
</fieldset>
```

**Python Selenium Code:**
```python
PET_TYPE_LABEL = (By.XPATH, "//fieldset[@role='group']//legend")
```

---

### 12. pet_info_page_pet_name_label
**Locator Strategy:** XPath (using for attribute pointing to pet-name input)

**HTML Structure:**
```html
<label for="pet-name" class="font-sans font-bold tracking-normal text-lg normal-case mb-3 mt-0 leading-none">
  What's your pet's name?
</label>
<input id="pet-name" required="" type="text" placeholder="Enter pet's name">
```

**Python Selenium Code:**
```python
PET_NAME_LABEL = (By.XPATH, "//label[@for='pet-name']")
```

---

### 13. pet_info_page_state_label
**Locator Strategy:** XPath (using for attribute pointing to state dropdown)

**HTML Structure:**
```html
<label for="state" class="font-sans font-bold tracking-normal text-lg normal-case mb-3 mt-0 leading-none">
  What state does your pet live in?
</label>
<select id="state" class="cursor-pointer w-full bg-light-cream border-cream !outline-none text-gray-400">
```

**Python Selenium Code:**
```python
STATE_LABEL = (By.XPATH, "//label[@for='state']")
```

---

## Complete Locator Block for PetInfoPage Class

Here's the complete set of locators ready to copy-paste into your PetInfoPage class:

```python
from selenium.webdriver.common.by import By


class PetInfoPage:
    """Page Object Model for the Pet Information registration page."""

    # Radio Buttons - Pet Type Selection
    DOG_RADIO_BUTTON = (By.ID, "dog")
    CAT_RADIO_BUTTON = (By.ID, "cat")
    PET_TYPE_RADIO_GROUP = (By.XPATH, "//form[@id='reg-flow-register']//fieldset[@role='group']")

    # Input Fields
    PET_NAME_INPUT = (By.ID, "pet-name")
    STATE_DROPDOWN = (By.ID, "state")

    # Buttons
    CONTINUE_BUTTON = (By.XPATH, "//form[@id='reg-flow-register']//button[@type='submit']")

    # Containers
    FORM_CONTAINER = (By.ID, "reg-flow-register")

    # Text Elements - Headings and Descriptions
    HEADING_TEXT = (By.XPATH, "//h2[contains(@class, 'font-sans') and contains(@class, 'text-[28px]')]")
    DESCRIPTION_TEXT = (By.XPATH, "//p[@class='mt-2 text-base sm:mt-5 sm:text-xl']")
    ADD_MORE_PETS_NOTE = (By.XPATH, "//fieldset[@role='group']//p[@class='pt-2 text-sm leading-snug text-[#666666]']")

    # Labels
    PET_TYPE_LABEL = (By.XPATH, "//fieldset[@role='group']//legend")
    PET_NAME_LABEL = (By.XPATH, "//label[@for='pet-name']")
    STATE_LABEL = (By.XPATH, "//label[@for='state']")
```

## Implementation Notes

1. **ID-based locators (Recommended):**
   - `DOG_RADIO_BUTTON`, `CAT_RADIO_BUTTON`, `PET_NAME_INPUT`, `STATE_DROPDOWN`, `FORM_CONTAINER` all use stable ID attributes
   - These are the most reliable and should be used wherever possible

2. **XPath locators (When no ID available):**
   - All XPath locators avoid using `text()` functions as requested
   - They rely on structural attributes like `@role`, `@for`, `@type`, and `@class`
   - XPath locators use form context (`//form[@id='reg-flow-register']`) when possible for stability

3. **Element Relationships:**
   - The radio buttons share `name="pet_type"` attribute
   - Labels use `for` attribute to associate with their inputs
   - The fieldset uses `role="group"` for semantic grouping

4. **Testing Recommendations:**
   - Test that radio buttons are mutually exclusive (same name attribute)
   - Verify the Continue button is initially disabled (has `disabled=""` attribute)
   - Check that pet name input has `required=""` attribute
   - Verify state dropdown has default placeholder option selected

## Additional Context

- **Form Validation:** The form appears to validate all three fields before enabling the Continue button
- **Required Fields:** Pet type (marked with *) and pet name (has required attribute) are explicitly required
- **State Options:** The dropdown includes all 50 US states plus DC and Puerto Rico
- **Radio Button Values:** Dog = "dog", Cat = "cat" (lowercase values)
- **Form Submit:** The Continue button is a submit button within the form `reg-flow-register`
