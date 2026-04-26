import json
import re
from backend.app.services.llm import generate_answer

def extract_meeting_info(text):
    prompt = f"""
Extract structured information from the meeting.

Return STRICT JSON (no markdown, no explanation):

{{
  "decisions": [],
  "action_items": [
    {{"task": "", "owner": "", "deadline": ""}}
  ],
  "discussions": []
}}

Meeting Transcript:
{text}
"""

    result = generate_answer(text, prompt)

    try:
        # 🔥 Remove ```json ``` if present
        cleaned = re.sub(r"```json|```", "", result).strip()

        parsed = json.loads(cleaned)
        return parsed

    except Exception as e:
        return {
            "error": "Parsing failed",
            "raw_output": result
        }