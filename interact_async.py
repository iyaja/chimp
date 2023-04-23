import random
import asyncio
from playwright.async_api import async_playwright, Page


async def interact_with_elements(page: Page, element, fill_text=None, type_text=None):
    aria_role = await element.get_attribute("role")

    if aria_role == "button":
        await element.click()
    elif aria_role == "textbox":
        if fill_text:
            await element.fill(fill_text)
        else:
            await element.fill("Sample text")
    elif aria_role == "checkbox":
        await element.check()
    elif aria_role == "combobox" or aria_role == "listbox":
        options = await element.query_selector_all("option")
        if options:
            await random.choice(options).click()
    elif aria_role == "radio":
        await element.check()
    elif aria_role == "searchbox":
        if type_text:
            await element.type(type_text, delay=random.randint(30, 100))
        else:
            await element.type("Search query", delay=random.randint(30, 100))
    # Add more conditions for other roles and actions as needed

    print(f"Done interacting with element with role {aria_role}...")

    # Scroll the element into view and add some random mouse movement
    await element.scroll_into_view_if_needed()
    # await page.mouse.move(
    #     random.randint(0, 800), random.randint(0, 600), steps=random.randint(5, 20)
    # )

    # Wait for a random time between 0.5 and 2.0 seconds
    await asyncio.sleep(random.uniform(0.5, 2.0))


async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # Load the webpage by link
    await page.goto("https://www.facebook.com")

    # Get elements with ARIA labels and roles
    elements = await get_elements_with_aria_labels_and_roles(page)

    # Interact with the elements based on their roles
    # Interact with the elements based on their roles
    for _ in range(5):
        # Interact with the elements
        element = random.sample(elements, 1)[0]
        await interact_with_elements(
            page, element, fill_text="Custom text", type_text="Custom search query"
        )

        # Extract the new ARIA labels and roles
        elements = await get_elements_with_aria_labels_and_roles(page)

    # Close the browser after completing the tasks
    await browser.close()


async def get_elements_with_aria_labels_and_roles(page):
    return await page.query_selector_all("[aria-label], [role]")


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
