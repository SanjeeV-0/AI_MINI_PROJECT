from fastapi import APIRouter, HTTPException
from backend.app.services import store
from backend.app.services.llm import generate_answer
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/summary")
def get_summary():
    try:
        logger.info("Generating meeting summary...")
        if store.vector_store is None:
            logger.warning("Summary requested but no transcript uploaded yet.")
            return {"error": "No transcript uploaded yet"}

        
        context = "\n".join(store.vector_store.text_chunks)

        prompt = f"""
Summarize the following meeting clearly:

{context}
"""

        summary = generate_answer(context, prompt)
        logger.info("Summary generated successfully.")

        return {
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during summary generation")