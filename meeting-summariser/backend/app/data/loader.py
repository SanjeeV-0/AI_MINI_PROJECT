import json
import os

def load_meetings(data_path):
    meetings = []

    for file in os.listdir(data_path):
        if file.endswith(".json"):
            path = os.path.join(data_path, file)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                meetings.append(data)

    return meetings

def build_transcript(meeting):
    segments = meeting.get("segments", [])

    full_text = " ".join(
        seg.get("text", "") for seg in segments
    )

    return full_text