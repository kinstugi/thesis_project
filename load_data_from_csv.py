import csv
from models import Session, Question, TopicTag, Solution
import json
from sqlalchemy.orm import joinedload


def load_questions_from_csv_to_db():
    session = Session()

    total_cnt = 0
    with open("./data/leetcode_questions.csv", "r") as file:
        reader = csv.DictReader(file)
        seen_tags = set()
        for row in reader:
            if not row.get('Question Text'):
                continue
            total_cnt += 1
            question = Question(
                text=row.get("Question Text", ""),
                title=row.get("Question Title", ""),
                slug=row.get("Question Slug", ""),
                difficulty=row.get("Difficulty", ""),
                # question_id=int(row.get("Question ID", 0)) if row.get("Question ID", "0").isdigit() else 0,
                likes=int(row["Likes"]) if row["Likes"].isdigit() else 0,
                dislikes=int(row["Dislikes"]) if row["Dislikes"].isdigit() else 0,
                acceptance=row.get("Acceptance", "")
            )
            session.add(question)
            session.commit()
            tags = [tag.strip() for tag in row["Topic Tagged text"].split(",")]
            for tag in tags:
                if not tag:
                    continue
                topic_tag = session.query(TopicTag).filter_by(name=tag).first()
                if not topic_tag:
                    topic_tag = TopicTag(name=tag)
                    session.add(topic_tag)
                question.topic_tags.append(topic_tag)
            session.commit()
            
    print(f"Total questions processed: {total_cnt}")

def load_questions_csv(file_path: str):
    session = Session()
    missing = []

    with open(file_path, 'r') as fh:
        data = csv.DictReader(fh)
        for row in data:
            query_res = session.query(Question).filter(Question.slug == row['titleSlug']).all()
            if not query_res and row['paidOnly'] == 'False':
                missing.append(row)
    print(len(missing))
    with open('./missing_questions.json', 'w') as fh:
        json.dump(missing, fh, indent=4)

def check_questions_without_answers():
    session = Session()
    questions = session.query(Question).options(joinedload(Question.solutions)).all()
    num = 0
    missing = []

    for question in questions:
        if not question.solutions:
            num += 1
            missing.append(f"https://leetcode.com/problems/{question.slug}")
    
    with open('questions_without_answers.txt', 'w') as fh:
        for link in missing:
            fh.write(link + '\n')
    return num

if __name__ == "__main__":
    # load_questions_from_csv_to_db()
    res = check_questions_without_answers()
    print(res)