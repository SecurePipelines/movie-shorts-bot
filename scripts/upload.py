import google_auth_oauthlib.flow
import googleapiclient.discovery

def upload_video(file, title, desc):

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        ["https://www.googleapis.com/auth/youtube.upload"]
    )

    creds = flow.run_console()

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title[:90],
                "description": desc,
                "tags": ["shorts"],
                "categoryId": "24"
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=file
    )

    request.execute()