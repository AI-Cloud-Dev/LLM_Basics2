In normal Chatbots the flow is:

User -> FastAPI -> Memory -> LLM -> Response

CONS: Only user conversation no function to upload the pdf or to inject the data. so to overcome we have to add upload functionilty to inject the context using retrieval.

BUT in RAG the system flow is :

User uploads PDF ->
       |
Extract Text ->
       |
Chunk Text ->
       |
Convert to Embeddings ->
       |
Store in vector DB ->
       |
User asks question ->
       |
Search relevant chunks ->
       |
Send chunks + question to LLM ->
       |
LLM generates grounded answer

LLM does NOT "learn" your PDF. It just retrieves + uses context dynamically
