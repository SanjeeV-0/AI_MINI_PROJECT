from fastapi import APIRouter, HTTPException
from backend.app.services import store
from backend.app.services.llm import generate_answer
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/decisions")
async def get_decisions():
    try:
        logger.info("Generating key decisions...")
        if store.vector_store is None:
            logger.warning("Decisions requested but no transcript uploaded yet.")
            return {"error": "No transcript uploaded yet"}

        context = "\n".join(store.vector_store.text_chunks)

        prompt = f"""
Extract key decisions made in the meeting:

{context}
"""

        result = await generate_answer(context, prompt)
        logger.info("Decisions generated successfully.")

        return {
            "decisions": result
        }
    except Exception as e:
        logger.error(f"Error generating decisions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error generating decisions")