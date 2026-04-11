from typing import List
from app.model.model import ChatMessage
from app.service.embedding_service import get_embedding
from app.service.vector_store import search
from app.service.service import get_llm_response
from app.memory.memory_store import memory_store


SYSTEM_PROMPT = "You are a helpful AI assistant. Use the provided context to answer accurately. If the answer is not in the context, say you don't know."


def get_rag_response(session_id: str, question: str, k: int = 3) -> str:
    
    # 1. Get memory
    messages: List[ChatMessage] = memory_store.get(session_id, [])

    # 2. Convert question → embedding
    query_embedding = get_embedding(question)

    # 3. Search vector DB
    retrieved_chunks = search(query_embedding, k=k)

    # 4. Handle NO CONTEXT (your Q8 answer implementation)
    if not retrieved_chunks:
        # fallback to normal LLM
        messages.append(ChatMessage(role="user", content=question))
        response = get_llm_response(messages)
        messages.append(ChatMessage(role="assistant", content=response))
        memory_store[session_id] = messages
        return response

    # 5. Build context string
    context = "\n\n".join(retrieved_chunks)

    # 6. Build final messages for LLM
    rag_messages = []

    # System instruction
    rag_messages.append(ChatMessage(
        role="system",
        content=SYSTEM_PROMPT
    ))

    # Context injected as system (important trick)
    rag_messages.append(ChatMessage(
        role="system",
        content=f"Context:\n{context}"
    ))

    # Add limited memory (last few messages only)
    rag_messages.extend(messages[-5:])  # limit memory

    # Add current question
    rag_messages.append(ChatMessage(
        role="user",
        content=question
    ))

    # 7. Call LLM
    response = get_llm_response(rag_messages)

    # 8. Store in memory
    messages.append(ChatMessage(role="user", content=question))
    messages.append(ChatMessage(role="assistant", content=response))

    memory_store[session_id] = messages

    return response