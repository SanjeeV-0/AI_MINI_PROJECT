from backend.app.data.loader import load_meetings, build_transcript
from backend.app.routes.upload import upload_transcript, TranscriptRequest

def process_dataset(data_path, limit=3):
    meetings = load_meetings(data_path)

    for i, meeting in enumerate(meetings[:limit]):
        transcript = build_transcript(meeting)

        # ✅ ADD HERE (inside loop)
        meeting_id = meeting.get("meeting_id", f"m{i}")

        request = TranscriptRequest(
            transcript=transcript,
            meeting_id=meeting_id
        )

        response = upload_transcript(request)

        print(f"Processed meeting {meeting_id}")