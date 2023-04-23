import asyncio
import random
from playwright.async_api import ElementHandle, Page, async_playwright

from agents import UserAgent

MAX_ELEMENTS = 100


async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # Load the webpage by link
    await page.goto("https://news.ycombinator.com")

    # Setup the user agent
    agent = UserAgent(
        "Dave is a tech savy coder who is looking for a new job.", model="gpt-4"
    )

    # Get elements with ARIA labels and roles
    elements = await get_visible_and_interactable_elements_with_aria_labels_and_roles(
        page
    )

    # Interact with the elements based on their roles
    # Interact with the elements based on their roles
    for _ in range(5):
        # Pass content from the page to the agent as a dict
        state = await get_page_data(page)
        # state_ack = agent.update_state(state)
        # print(f"State Acknowledgement: \n\n {state_ack}")

        # Pass the action dict to the agent and get the selected action
        element_dict = {await e.get_attribute("id"): e for e in elements[:MAX_ELEMENTS]}

        print(element_dict)

        # element_id = agent.select_action(element_dict)
        # element = element_dict[element_id]

        # select random element
        element_id = random.choice(list(element_dict.keys()))
        element = element_dict[element_id]

        print(f"Selected element with id {element_id}...")
        # print(f"Explanation: \n\n {agent.get_explantion()}")

        # Interact with the elements
        await interact_with_elements(
            page, element, fill_text="Custom text", type_text="Custom search query"
        )

        # Extract the new ARIA labels and roles
        elements = (
            await get_visible_and_interactable_elements_with_aria_labels_and_roles(page)
        )

    # Close the browser after completing the tasks
    await browser.close()


async def get_page_data(page: Page) -> dict:
    title = await page.title()

    try:
        description_elem = await page.query_selector('meta[name="description"]')
        description = await description_elem.content() if description_elem else None

        meta_data = await page.eval_on_selector_all(
            "meta",
            'els => els.map(el => ({name: el.getAttribute("name"), content: el.content}))',
        )

        small_content = await page.eval_on_selector(
            "body", "el => el.textContent.slice(0, 100)"
        )
    except Exception:
        description = None
        meta_data = None
        small_content = None

    data = {
        "title": title,
        "description": description,
        "metadata": meta_data,
        "small_content": small_content,
    }
    return data


async def interact_with_elements(page: Page, element, fill_text=None, type_text=None):
    aria_role = await element.get_attribute("role")
    tag_name = await element.get_attribute("tagName")

    try:
        if tag_name:
            if tag_name.lower() == "a" and await element.get_attribute("href"):
                await element.click()
        elif aria_role == "button":
            element.click()
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
        await page.mouse.move(
            random.randint(0, 800), random.randint(0, 600), steps=random.randint(5, 20)
        )

        # Wait for a random time between 0.5 and 2.0 seconds
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        if "Element is not attached to the DOM" in str(e):
            print("Element is not attached to the DOM. Skipping...")
        else:
            raise


async def is_element_visible(element: ElementHandle) -> bool:
    bounding_box = await element.bounding_box()
    return bounding_box is not None


async def is_element_interactable(element):
    try:
        await element.wait_for_element_state(
            "enabled", timeout=5000
        )  # Increased timeout to 5000 milliseconds
        return True
    except Exception:
        return False


async def get_visible_and_interactable_elements_with_aria_labels_and_roles(page: Page):
    all_elements = await page.query_selector_all("[aria-label], [role], a[href]")
    visible_and_interactable_elements = []

    for element in all_elements:
        if await is_element_visible(element) and await is_element_interactable(element):
            visible_and_interactable_elements.append(element)

    return visible_and_interactable_elements


if __name__ == "__main__":

    async def main():
        async with async_playwright() as playwright:
            await run(playwright)

    asyncio.run(main())
