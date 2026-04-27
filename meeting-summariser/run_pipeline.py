from dotenv import load_dotenv
load_dotenv()

import asyncio
from backend.app.data.pipeline import process_dataset

asyncio.run(process_dataset("backend/app/datasets/meetings", limit=3))

