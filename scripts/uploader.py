from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(file_path, title):
    print(f"📤 Uploading: {file_path}")

    youtube = get_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "Auto generated shorts #shorts",
                "tags": ["shorts", "viral"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(file_path)
    )

    response = request.execute()
    print("✅ Uploaded:", response["id"])