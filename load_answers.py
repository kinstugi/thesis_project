import argparse, os
from models import Session, Solution, Question


if __name__ == "__main__":
    session = Session()
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--dir", '-d', type=str, required=True, help="Directory to load answers from")
    args = argument_parser.parse_args()
    missing_questions = []

    for directory in os.listdir(args.dir):
        full_path = os.path.join(args.dir, directory)
        if not os.path.isdir(full_path):
            continue
        slug = "-".join((directory.split(".")[1].lower().split()))
        print(slug)
        question = session.query(Question).filter_by(slug=slug).first()

        if not question:
            print(f"Question with slug {slug} not found")
            missing_questions.append(f"https://leetcode.com/problems/{slug}")
            continue

        for filename in os.listdir(full_path):
            answer_path = os.path.join(full_path, filename)
            if not os.path.isfile(answer_path):
                continue
            with open(answer_path, "r") as f:
                answer_content = f.read()
                q_answer = Solution(
                    question_id=question.id,
                    language=filename.split(".")[-1],
                    code=answer_content
                )
                session.add(q_answer)
                session.commit()
                print(f"Added solution for question {question.title} in language {q_answer.language}")
        
    #save missing questions to a file
    if missing_questions:
        with open("missing_questions.txt", "w") as f:
            for mq in missing_questions:
                f.write(mq + "\n")
        print(f"Saved {len(missing_questions)} missing questions to missing_questions.txt")
