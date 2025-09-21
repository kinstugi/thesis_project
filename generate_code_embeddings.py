from models import Session, Solution
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

def token_count(text):
    return len(text.split())

if __name__ == "__main__":
    session = Session()
    hf_token = os.getenv("HUGGINGFACE_TOKEN")

    if not hf_token:
        raise ValueError("HUGGINGFACE_TOKEN environment variable not set")
    
    client = InferenceClient(api_key=hf_token, provider="auto")
    solutions = session.query(Solution).all()

    for solution in solutions:
        # if solution.language == "cpp":
        #     continue
        code = solution.code
        embedding = len(code)
        if embedding > 1000:
            print(f"{code}")
            
        # embedding = client.feature_extraction(code, model="microsoft/codebert-base")   
        print(embedding)
        print("___________________________")