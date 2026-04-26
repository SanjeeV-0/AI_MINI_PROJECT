from fastapi import APIRouter
from backend.app.services import store
from backend.app.services.llm import generate_answer

router = APIRouter()

@router.get("/summary")
def get_summary():
    if store.vector_store is None:
        return {"error": "No transcript uploaded yet"}

    # Combine all chunks
    context = "\n".join(store.vector_store.text_chunks)

    prompt = f"""
Summarize the following meeting clearly:

{context}
"""

    summary = generate_answer(context, prompt)

    return {
        "summary": summary
    }