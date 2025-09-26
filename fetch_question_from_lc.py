def fetch_question_from_lec(url: str) -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Wait for the question content to load
        page.wait_for_selector('.question-content')

        # Extract the question text
        question_text = page.inner_html('.question-content')

        browser.close()
        return question_text
    
if __name__ == "__main__":
    # this file will take a url and fetch the question from leetcode using playwright
    pass