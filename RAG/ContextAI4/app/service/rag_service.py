from typing import List
from app.model.model import ChatMessage
from app.service.embedding_service import get_embedding
from app.service.vector_store import search
from app.service.service import get_llm_response
from app.memory.memory_store import memory_store


SYSTEM_PROMPT = """
You are a helpful AI assistant.

Rules:
1. Use ONLY the provided context.
2. If answer is not in context, say "I don't know".
3. Be concise and accurate.
"""


def get_rag_response(user_id: str, question: str, k: int = 3) -> str:

    # 1. Initialize memory
    if user_id not in memory_store:
        memory_store[user_id] = [
            ChatMessage(role="system", content="You are a helpful assistant.")
        ]

    messages: List[ChatMessage] = memory_store[user_id]

    # 2. Get embedding
    query_embedding = get_embedding(question)

    # 3. Retrieve chunks
    retrieved_chunks = search(user_id, query_embedding, k=k)

    # 4. If no context → fallback
    if not retrieved_chunks:
        messages.append(ChatMessage(role="user", content=question))
        response = get_llm_response(messages)
        messages.append(ChatMessage(role="assistant", content=response))
        return response

    # 5. Limit context size
    MAX_CONTEXT_CHARS = 2000
    context = ""

    for chunk in retrieved_chunks:
        if len(context) + len(chunk) > MAX_CONTEXT_CHARS:
            break
        context += chunk + "\n\n"

    # 6. Build RAG messages
    rag_messages = [
        ChatMessage(role="system", content=SYSTEM_PROMPT),
        ChatMessage(role="system", content=f"Context:\n{context}")
    ]

    # Add last few messages only (avoid overflow)
    rag_messages.extend(messages[-5:])

    # Add current question
    rag_messages.append(ChatMessage(role="user", content=question))

    # 7. Call LLM
    response = get_llm_response(rag_messages)

    # 8. Store in memory
    MAX_MESSAGES = 10
    messages.append(ChatMessage(role="user", content=question))
    messages.append(ChatMessage(role="assistant", content=response))
    
    if len(messages) > MAX_MESSAGES:
        memory_store[user_id] = messages[-MAX_MESSAGES:]

    return response