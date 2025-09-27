import argparse, os
from models import Session, Solution, Question

def load_answers(f_path:str):
    missing_questions = []
    
    for directory in os.listdir(f_path):
        full_path = os.path.join(f_path, directory)
        if not os.path.isdir(full_path):
            continue
        slug = "-".join((directory.split(".")[1].lower().split()))
        print(slug)
        question = session.query(Question).filter_by(slug=slug).first()
        if not question:
            print(f"Question with slug {slug} not found")
            missing_questions.append(f"{slug}")
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


def get_overlooked_solutions(f_path):
    seen = dict()
    session = Session()
    try:
        with open('./questions_without_answers.txt', 'r') as fh:
            for line in fh:
                question_id = int(line.split('-')[0])
                seen[question_id] = (line.split('/')[-1]).strip()
    except:
        pass
    
    for directory in os.listdir(f_path):
        full_path = os.path.join(f_path, directory)
        if not os.path.isdir(full_path):
            continue

        question_id = int(directory.split('.')[0])
        if question_id == 1393:
            print(question_id in seen, question_id, seen)
        if not question_id in seen:
            continue
        print("over <<<<<<<<<<")
        question = session.query(Question).filter(Question.slug == seen[question_id]).first()
        print(question)
        if not question:
            print(f"....... {seen[question_id]}")
            return
        for file in os.listdir(full_path):
            answer_path = os.path.join(full_path, file)
            if file.split('.')[-1] not in ['java', 'py', 'cpp']:
                continue
            answer_content = open(answer_path, 'r').read()
            q_solution = Solution(
                question_id = question.id,
                language = file.split('.')[-1],
                code = answer_content
            )
            session.add(q_solution)
            session.commit()
            print(f'added solution for {question.slug}')
            

if __name__ == "__main__":
    session = Session()
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--dir", '-d', type=str, required=True, help="Directory to load answers from")
    args = argument_parser.parse_args()
    

    get_overlooked_solutions(args.dir)
