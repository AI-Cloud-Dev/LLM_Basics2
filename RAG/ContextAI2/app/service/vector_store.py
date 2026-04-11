import faiss
import numpy as np

# session_id → index + documents
vector_store = {}

DIMENSION = 384


def get_or_create_index(session_id: str):
    if session_id not in vector_store:
        vector_store[session_id] = {
            "index": faiss.IndexFlatL2(DIMENSION),
            "documents": []
        }
    return vector_store[session_id]


def add_embeddings(session_id: str, embeddings, chunks):
    store = get_or_create_index(session_id)

    vectors = np.array(embeddings).astype("float32")
    faiss.normalize_L2(vectors)

    store["index"].add(vectors)
    store["documents"].extend(chunks)


def search(session_id: str, query_embedding, k=3):
    store = get_or_create_index(session_id)

    query_vector = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(query_vector)

    distances, indices = store["index"].search(query_vector, k)

    docs = store["documents"]

    return [docs[i] for i in indices[0] if i < len(docs)]