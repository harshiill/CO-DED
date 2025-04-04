import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-l6-v2')

def vec_store(sdata):
    texts = [item["content"] for item in sdata]
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings, texts

def retrieval(index, embeddings, texts, query_text, top=3):
    query_embedding = embedding_model.encode([query_text])
    distances, indices = index.search(query_embedding, top)
    retrieved = [texts[idx] for idx in indices[0]]
    return "\n\n".join(retrieved)
