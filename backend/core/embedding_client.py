from typing import List

_model = None

def get_model():
    global _model
    if _model is None:
        # pyrefly: ignore [missing-import]
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def generate_embedding(text: str) -> List[float]:
    model = get_model()
    embedding = model.encode(text)
    return embedding.tolist()
