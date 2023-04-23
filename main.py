# %%
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False) # You can use 'chromium', 'firefox', or 'webkit'
    context = browser.new_context()
    page = context.new_page()

    # Load the webpage by link
    page.goto("https://news.ycombinator.com")

    # Perform any other actions on the page (optional)
    # For example, you could take a screenshot:
    # page.screenshot(path="screenshot.png")

    # Wait for 5 seconds so you can see the result
    page.wait_for_timeout(5000)

    # Scroll to the bottom of the page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # Wait for 5 seconds so you can see the result
    page.wait_for_timeout(5000)

    # Close the browser after completing the tasks
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

# %%
