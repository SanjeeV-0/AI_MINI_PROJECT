from fastapi import APIRouter, HTTPException
from backend.app.services import store
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/action-items")
def get_action_items():
    try:
        logger.info("Fetching action items...")
        if not store.structured_data_store:
            logger.warning("Action items requested but no transcript uploaded yet.")
            return {"error": "No transcript uploaded yet"}

        all_action_items = []
        for data in store.structured_data_store.values():
            items = data.get("action_items", [])
            for item in items:
                if isinstance(item, dict):
                    task = item.get("task", "Unknown Task")
                    owner = item.get("owner", "Unassigned")
                    deadline = item.get("deadline", "No deadline")
                    all_action_items.append(f"{task} (Owner: {owner}, Due: {deadline})")
                elif isinstance(item, str):
                    all_action_items.append(item)

        logger.info(f"Found {len(all_action_items)} action items.")
        return {
            "action_items": all_action_items
        }
    except Exception as e:
        logger.error(f"Error fetching action items: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error fetching action items")