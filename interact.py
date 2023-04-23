import random
import time
from playwright.sync_api import ElementHandle, Page, sync_playwright
from playwright.sync_api import sync_playwright
from typing import List


def get_elements_with_aria_labels_and_roles(page: Page) -> List[ElementHandle]:
    # Find elements with ARIA labels and roles
    elements_with_aria_label = page.query_selector_all("[aria-label]")
    elements_with_aria_role = page.query_selector_all("[role]")

    # Combine the lists and remove duplicates
    all_elements = list(set(elements_with_aria_label + elements_with_aria_role))

    return all_elements


def interact_with_element(page: Page, element, fill_text=None, type_text=None):
    aria_role = element.get_attribute("role")

    print(f"Interacting with element with role {aria_role}...")

    if aria_role == "button":
        element.click()
    elif aria_role == "textbox":
        if fill_text:
            element.fill(fill_text)
        else:
            element.fill("Sample text")
    elif aria_role == "checkbox":
        element.check()
    elif aria_role == "combobox" or aria_role == "listbox":
        options = element.query_selector_all("option")
        if options:
            random.choice(options).click()
    elif aria_role == "radio":
        element.check()
    elif aria_role == "searchbox":
        if type_text:
            element.type(type_text, delay=random.randint(30, 100))
        else:
            element.type("Search query", delay=random.randint(30, 100))

    # Add more conditions for other roles and actions as needed

    print(f"Done interacting with element with role {aria_role}...")

    # Scroll the element into view and add some random mouse movement
    element.scroll_into_view_if_needed()
    page.mouse.move(
        random.randint(0, 800), random.randint(0, 600), steps=random.randint(5, 20)
    )


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Load the webpage by link
    page.goto("https://www.facebook.com")

    # Get elements with ARIA labels and roles
    elements = get_elements_with_aria_labels_and_roles(page)

    # Interact with the elements based on their roles
    for _ in range(5):
        # Interact with the elements
        element = random.sample(elements, 1)[0]
        interact_with_element(
            page, element, fill_text="Custom text", type_text="Custom search query"
        )
        # Wait for 2 seconds before interacting with the next element
        time.sleep(2)

        # Extract the new ARIA labels and roles
        elements = get_elements_with_aria_labels_and_roles(page)

    # Close the browser after completing the tasks
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
