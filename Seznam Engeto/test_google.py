import pytest
from playwright.sync_api import sync_playwright, TimeoutError, Page

@pytest.fixture(scope="module")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)  # Set headless=True if you don't need to see the browser
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture(scope="module")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()
    

def test_google(page: Page):
    
    page.goto("https://www.google.com/")
    
    accept_button = page.locator("text=I agree").first
    if accept_button.is_visible():
        accept_button.click()

    assert page.locator("img[alt='Google']").first.is_visible(), "Logo is not visible."

def test_google_hledat(page: Page):
    
    page.goto("https://www.google.com/")
    
    accept_button = page.locator("text=I agree").first
    if accept_button.is_visible():
        accept_button.click()

    textarea_locator = page.locator('textarea.gLFyf[title="Hledat"][name="q"]')
    textarea_locator.click()
    textarea_locator.fill("engeto")
    textarea_locator.press("Enter")

    page.wait_for_selector("#search")
    assert page.locator("#search").is_visible(), "Search results are not visible."


def test_google_tel_cislo(page):
    page.goto("https://www.google.com/")
    accept_button = page.locator("text=I agree").first
    if accept_button.is_visible():
        accept_button.click()
    textarea_locator = page.locator('textarea[name="q"]')
    textarea_locator.click()
    textarea_locator.fill("engeto telefon")
    textarea_locator.press("Enter")
    page.wait_for_selector("#search")
    phone_element = page.query_selector('span[aria-label="Zavolat na číslo 773 087 597"]')
    assert phone_element is not None, "Phone number not found in search results."
    phone_number = phone_element.inner_text()
    expected_text = "773 087 597"
    assert phone_number == expected_text, f"Expected text: {expected_text}, but got: {phone_number}"






 

