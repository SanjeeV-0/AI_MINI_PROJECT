from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.utils.embeddings import get_embeddings
from backend.app.services import store
from backend.app.services.llm import generate_answer
from backend.app.utils.intent import detect_intent
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def query_data(request: QueryRequest):
    try:
        logger.info(f"Received query: '{request.question}'")
        if store.vector_store is None:
            logger.warning("Query attempted but no transcript uploaded yet.")
            return {"error": "No transcript uploaded yet"}

        intent = detect_intent(request.question)
        logger.info(f"Detected intent: {intent}")

        
        if intent == "action_item":
            return {
                "source": "structured",
                "answer": list(store.structured_data_store.values())
            }

        
        query_embedding = get_embeddings([request.question])[0]

        chunks = store.vector_store.search(query_embedding)

        context = "\n".join([chunk["text"] for chunk in chunks])

        answer, usage = generate_answer(context, request.question, return_usage=True)
        
        logger.info(f"Query processed successfully via RAG.")

        return {
            "source": "rag",
            "question": request.question,
            "answer": answer,
            "references": list(set([chunk["text"] for chunk in chunks])),
            "usage": usage
        }
    except Exception as e:
        logger.error(f"Error processing query '{request.question}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during query")