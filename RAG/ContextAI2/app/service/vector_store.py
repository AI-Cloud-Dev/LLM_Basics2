import faiss
import numpy as np


dimension = 384 # for MiniLM model
index = faiss.IndexFlatL2(dimension)

documents = [] # store original text chunks

def add_embeddings(embeddings, chunks):
    global documents
    
    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)
    documents.extend(chunks)
    
def search(query_embedding, k=3):
    query_vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_vector, k)
    
    results = [documents[i] for i in indices[0] if i < len(documents)]
    return results