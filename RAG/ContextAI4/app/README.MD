In normal Chatbots the flow is:

User -> FastAPI -> Memory -> LLM -> Response

CONS: Only user conversation no function to upload the pdf or to inject the data. so to overcome we have to add upload functionilty to inject the context using retrieval.

BUT in RAG the system flow is :

User uploads PDF
       |
Extract Text
       |
Chunk Text
       |
Convert to Embeddings
       |
Store in vector DB
       |
User asks question
       |
Search relevant chunks
       |
Send chunks + question to LLM
       |
LLM generates grounded answer

LLM does NOT "learn" your PDF. It just retrieves + uses context dynamically


I replaced in-memory storage with Redis to enable distributed session memory. Chat history is stored per user using key-based design and trimmed to avoid context overflow.


User
 ↓
JWT Auth
 ↓
FastAPI
 ↓
Redis (chat memory)
 ↓
Chroma (vector DB)
 ↓
Ollama (LLM)


PRODUCTION ARCHITECTURE (FINAL)
User
 ↓
Streamlit (UI)
 ↓
FastAPI (Auth + RAG)
 ↓
Redis (memory + rate limit)
 ↓
Chroma (vector DB)
 ↓
Ollama / LLM

I deployed a full-stack AI RAG system with a decoupled architecture where Streamlit acts as frontend and FastAPI handles backend services including authentication, Redis caching, and Chroma vector storage.
