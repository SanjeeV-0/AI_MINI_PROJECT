from fastapi import APIRouter
from backend.app.services import store

router = APIRouter()

@router.get("/action-items")
def get_action_items():
    if not store.structured_data_store:
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

    return {
        "action_items": all_action_items
    }