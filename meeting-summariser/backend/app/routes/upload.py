from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.extractor import extract_meeting_info
from backend.app.utils.chunking import chunk_text
from backend.app.utils.embeddings import get_embeddings
from backend.app.services.retriever import VectorStore
from backend.app.services import store

router = APIRouter()

class TranscriptRequest(BaseModel):
    transcript: str
    meeting_id: str

@router.post("/upload")
def upload_transcript(request: TranscriptRequest):
    text = request.transcript.strip()

    if not text:
        return {"error": "Transcript cannot be empty"}

    # Step 1: chunk + embeddings
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)

    dim = embeddings.shape[1]

    # ✅ IMPORTANT: only initialize once
    if store.vector_store is None:
        store.vector_store = VectorStore(dim)

    # Step 2: metadata
    metadata = [
        {
            "type": "discussion",
            "meeting_id": request.meeting_id
        }
        for _ in chunks
    ]

    # Step 3: add to vector DB
    store.vector_store.add(embeddings, chunks, metadata)

    # Step 4: structured extraction
    structured_data = extract_meeting_info(text)

    store.structured_data_store[request.meeting_id] = structured_data

    return {
        "message": "Processed",
        "meeting_id": request.meeting_id,
        "structured_data": structured_data
    }