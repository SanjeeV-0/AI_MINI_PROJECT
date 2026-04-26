from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.utils.embeddings import get_embeddings
from backend.app.services import store
from backend.app.services.llm import generate_answer
from backend.app.utils.intent import detect_intent

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def query_data(request: QueryRequest):
    if store.vector_store is None:
        return {"error": "No transcript uploaded yet"}

    intent = detect_intent(request.question)

    # ✅ Structured routing
    if intent == "action_item":
        return {
            "source": "structured",
            "answer": list(store.structured_data_store.values())
        }

    # ✅ RAG
    query_embedding = get_embeddings([request.question])[0]

    chunks = store.vector_store.search(query_embedding)

    context = "\n".join([chunk["text"] for chunk in chunks])

    answer = generate_answer(context, request.question)

    return {
        "source": "rag",
        "question": request.question,
        "answer": answer,
        "references": list(set([chunk["text"] for chunk in chunks]))
    }