from models import Session, Solution
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os, time


load_dotenv()

def token_count(text):
    return len(text.split())

if __name__ == "__main__":
    session = Session()
    hf_token = os.getenv("HUGGINGFACE_TOKEN")

    if not hf_token:
        raise ValueError("HUGGINGFACE_TOKEN environment variable not set")
    
    client = InferenceClient(api_key=hf_token, provider="auto")
    chunk = 100
    current_page = 0

    while True:
        solutions = session.query(Solution).limit(chunk).offset(current_page * chunk)
        if not solutions:
            break
        
        for solution in solutions:
            
            code = solution.code
            embedding = client.feature_extraction(code, model="microsoft/codebert-base")   
            #convert embedding to string
            embedding_str = ','.join(map(str, embedding[0]))
            solution.embedding = embedding_str
            session.commit()
            time.sleep(1)
            print("genereated embeddings for this ...........")
        time.sleep(30)
        current_page += 1