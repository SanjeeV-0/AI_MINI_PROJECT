from dotenv import load_dotenv
load_dotenv()

from backend.app.data.pipeline import process_dataset

process_dataset("backend/app/datasets/meetings", limit=3)

