import json
from backend.app.services.llm import generate_answer
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

async def extract_meeting_info(text):
    prompt = f"""
Extract structured information from the meeting.

Return STRICT JSON:

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

    result = await generate_answer(text, prompt, response_format={"type": "json_object"})

    try:
        parsed = json.loads(result)
        return parsed
    except Exception as e:
        logger.error(f"JSON Parsing failed during extraction: {str(e)}. Raw output: {result}")
        return {
            "error": "Parsing failed",
            "raw_output": result
        }