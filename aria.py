from typing import List

from playwright.sync_api import ElementHandle, Page, sync_playwright


def get_elements_with_aria_labels_and_roles(page: Page) -> List[ElementHandle]:
    # Find elements with ARIA labels and roles
    elements_with_aria_label = page.query_selector_all("[aria-label]")
    elements_with_aria_role = page.query_selector_all("[role]")

    # Combine the lists and remove duplicates
    all_elements = list(set(elements_with_aria_label + elements_with_aria_role))

    return all_elements


def extract_aria_labels_and_roles(page):
    # Find elements with ARIA labels and roles
    elements_with_aria_label = page.query_selector_all("[aria-label]")
    elements_with_aria_role = page.query_selector_all("[role]")

    # Extract ARIA labels and roles from elements
    aria_labels_and_roles = []

    for element in elements_with_aria_label:
        aria_label = element.get_attribute("aria-label")
        aria_role = element.get_attribute("role")
        aria_labels_and_roles.append((aria_label, aria_role))

    for element in elements_with_aria_role:
        if element not in elements_with_aria_label:
            aria_label = element.get_attribute("aria-label")
            aria_role = element.get_attribute("role")
            aria_labels_and_roles.append((aria_label, aria_role))

    return aria_labels_and_roles


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Load the webpage by link
    page.goto("https://facebook.com")

    # Get elements with ARIA labels and roles
    elements = get_elements_with_aria_labels_and_roles(page)


    print("Elements with ARIA labels and/or roles:")
    for element in elements:
        element_id = element.get_attribute("id")
        aria_label = element.get_attribute("aria-label")
        aria_role = element.get_attribute("role")
        bounding_box = element.bounding_box()
        if bounding_box:
            x = bounding_box["x"]
            y = bounding_box["y"]
            print(f"Element ID: {element_id}, Label: {aria_label}, Role: {aria_role}, Position: (x={x}, y={y})")
        else:
            print(f"Element ID: {element_id}, Label: {aria_label}, Role: {aria_role}, Position: Not available")


    # # Extract ARIA labels and roles
    # aria_labels_and_roles = extract_aria_labels_and_roles(page)

    # print("ARIA labels and roles:")
    # for label, role in aria_labels_and_roles:
    #     print(f"Label: {label}, Role: {role}")

    # Close the browser after completing the tasks
    browser.close()


with sync_playwright() as playwright:
    run(playwright)