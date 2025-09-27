import json
from html.parser import HTMLParser
from models import Session, Question, TopicTag

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        # Collect non-whitespace data
        if data.strip():
            self.text.append(data.strip())
            
    def handle_endtag(self, tag):
        # Add a space or newline after block-level tags like <p>, <div>, <li>, <pre>
        if tag in ('p', 'div', 'li', 'pre'):
             self.text.append('\n')

    def get_text(self):
        # Join collected data, replace multiple newlines/spaces with a single one
        return ' '.join(self.text).replace(' \n', '\n').strip()



def fetch_question_from_lec(url: str) -> str:
    parser = TextExtractor()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        selector = 'div[data-track-load="description_content"]'
        # Wait for the question content to load
        page.wait_for_selector(selector)

        # Extract the question text
        question_text = page.inner_html(selector)

        browser.close()
        parser.feed(question_text)
        return parser.get_text()


def save_question_to_db(q_text:str, row: dict):
    session = Session()
    q_res = session.query(Question).filter(Question.slug == row.get('titleSlug')).all()
    if q_res:
        print(f"skipped: {row.get('titleSlug')}")
        return
    question = Question(
        text=q_text,
        title=row.get("title", ""),
        slug=row.get("titleSlug", ""),
        difficulty=row.get("difficulty", ""),
        # question_id=int(row.get("frontendQuestionId", 0)) if row.get("frontendQuestionId", "0").isdigit() else 0,
        likes= 0,
        dislikes=0,
        acceptance=row.get("acRate", "")
    )

    session.add(question)
    session.commit()
    for tag in row.get('topicTags', []):
        topic_tag = session.query(TopicTag).filter_by(name=tag).first()
        if not topic_tag:
            topic_tag = TopicTag(name=tag)
            session.add(topic_tag)
        question.topic_tags.append(topic_tag)
    session.commit()


if __name__ == "__main__":
    # this file will take a url and fetch the question from leetcode using playwright
    
    with open('missing_questions.json') as fh:
        data = json.load(fh)
    for item in data[:]:
        url = f"https://leetcode.com/problems/{item['titleSlug']}/description"
    
        question = fetch_question_from_lec(url)
        save_question_to_db(question, item)
        print(f"processed: {item.get('titleSlug')}")
    

