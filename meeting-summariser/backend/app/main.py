from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from backend.app.data.pipeline import process_dataset
from backend.app.routes import upload
from backend.app.routes import upload, query
from backend.app.routes import summary, action_items, decisions



app = FastAPI(title="Meeting Summariser API")

app.include_router(upload.router)
app.include_router(query.router)

app.include_router(summary.router)
app.include_router(action_items.router)
app.include_router(decisions.router)

app.include_router(upload.router)
@app.on_event("startup")
def load_data():
    print("Loading dataset...")
    process_dataset("backend/app/datasets/meetings", limit=3)
    print("Dataset loaded.")

@app.get("/")
def root():
    return {"message": "API is running"}