from backend.app.data.loader import load_meetings, build_transcript
from backend.app.routes.upload import upload_transcript, TranscriptRequest
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

def process_dataset(data_path, limit=3):
    try:
        meetings = load_meetings(data_path)
        logger.info(f"Found {len(meetings)} meetings. Processing up to {limit}.")

        for i, meeting in enumerate(meetings[:limit]):
            try:
                transcript = build_transcript(meeting)
                
                meeting_id = meeting.get("meeting_id", f"m{i}")

                request = TranscriptRequest(
                    transcript=transcript,
                    meeting_id=meeting_id
                )

                response = upload_transcript(request)
                logger.info(f"Processed meeting {meeting_id} successfully.")
            except Exception as e:
                logger.error(f"Error processing meeting {meeting.get('meeting_id', f'm{i}')}: {str(e)}")
    except Exception as e:
        logger.error(f"Critical error loading meetings from {data_path}: {str(e)}")