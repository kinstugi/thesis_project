import csv
from models import Session, Question, TopicTag, Solution


if __name__ == "__main__":
    session = Session()

    
    total_cnt = 0
    with open("leetcode_questions.csv", "r") as file:
        reader = csv.DictReader(file)
        seen_tags = set()
        for row in reader:
            total_cnt += 1
            question = Question(
                text=row.get("Question Text", ""),
                title=row.get("Question Title", ""),
                slug=row.get("Question Slug", ""),
                difficulty=row.get("Difficulty", ""),
                question_id=int(row.get("Question ID", 0)) if row.get("Question ID", "0").isdigit() else 0,
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