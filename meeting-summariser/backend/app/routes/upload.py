from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.extractor import extract_meeting_info
from backend.app.utils.chunking import chunk_text
from backend.app.utils.embeddings import get_embeddings
from backend.app.services.retriever import VectorStore
from backend.app.services import store
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

class TranscriptRequest(BaseModel):
    transcript: str
    meeting_id: str

@router.post("/upload")
async def upload_transcript(request: TranscriptRequest):
    try:
        text = request.transcript.strip()

        if not text:
            logger.warning(f"Empty transcript received for meeting_id: {request.meeting_id}")
            return {"error": "Transcript cannot be empty"}

        logger.info(f"Starting upload process for meeting_id: {request.meeting_id}")

        #  chunk + embeddings
        chunks = chunk_text(text)
        embeddings = get_embeddings(chunks)

        dim = embeddings.shape[1]

        
        if store.vector_store is None:
            logger.info("Initializing VectorStore.")
            store.vector_store = VectorStore(dim)

        #  metadata
        metadata = [
            {
                "type": "discussion",
                "meeting_id": request.meeting_id
            }
            for _ in chunks
        ]

        #  add to vector DB
        store.vector_store.add(embeddings, chunks, metadata)
        logger.info(f"Added {len(chunks)} chunks to vector store for meeting_id: {request.meeting_id}")

        # Step 4: structured extraction
        structured_data = await extract_meeting_info(text)

        store.structured_data_store[request.meeting_id] = structured_data
        logger.info(f"Structured data extraction complete for meeting_id: {request.meeting_id}")

        return {
            "message": "Processed",
            "meeting_id": request.meeting_id,
            "structured_data": structured_data
        }
    except Exception as e:
        logger.error(f"Error uploading transcript for meeting_id {request.meeting_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during upload")