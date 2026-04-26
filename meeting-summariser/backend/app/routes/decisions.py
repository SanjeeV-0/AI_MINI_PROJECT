from fastapi import APIRouter
from backend.app.services import store
from backend.app.services.llm import generate_answer

router = APIRouter()

@router.get("/decisions")
def get_decisions():
    if store.vector_store is None:
        return {"error": "No transcript uploaded yet"}

    context = "\n".join(store.vector_store.text_chunks)

    prompt = f"""
Extract key decisions made in the meeting:

{context}
"""

    result = generate_answer(context, prompt)

    return {
        "decisions": result
    }