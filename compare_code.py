from models import Session, Solution
import numpy as np

def cosine_similarity(e1, e2):
    # Example embeddings (NumPy arrays)
    embedding_1 = np.array([0.5, 0.8, 0.2])
    embedding_2 = np.array([0.4, 0.9, 0.1])

    # Calculate the dot product
    dot_product = np.dot(embedding_1, embedding_2)

    # Calculate the magnitudes (L2 norm)
    magnitude_1 = np.linalg.norm(embedding_1)
    magnitude_2 = np.linalg.norm(embedding_2)


    # Calculate cosine similarity
    cosine_similarity = dot_product / (magnitude_1 * magnitude_2)
    return cosine_similarity

if __name__ == "__main__":
    session = Session()
    solutions = session.query(Solution).filter(Solution.question_id == 1).all()
    
    embeddings = []
    for solution in solutions:
        arr = list(map(lambda x: float(x),solution.embedding.split(',')))
        embeddings.append(np.array(arr))
    
    print(cosine_similarity(embeddings[2], embeddings[1]))