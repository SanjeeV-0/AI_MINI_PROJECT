from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from backend.app.data.pipeline import process_dataset
from backend.app.routes import upload, query
from backend.app.routes import summary, action_items, decisions
from backend.app.utils.logger import get_logger


logger = get_logger(__name__)

app = FastAPI(title="Meeting Summariser API")

app.include_router(upload.router)
app.include_router(query.router)
app.include_router(summary.router)
app.include_router(action_items.router)
app.include_router(decisions.router)

@app.on_event("startup")
async def load_data():
    logger.info("Starting up API and loading dataset...")
    try:
        await process_dataset("backend/app/datasets/meetings", limit=3)
        logger.info("Dataset loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load dataset: {str(e)}")

@app.get("/")
def root():
    return {"message": "API is running"}