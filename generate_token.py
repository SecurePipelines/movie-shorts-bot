from google_auth_oauthlib.flow import InstalledAppFlow

# Scope for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    # Load client secrets
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        SCOPES
    )

    # Use local server for browser-based authentication
    creds = flow.run_local_server(port=0)

    # Save credentials to token.json
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())

    print("✅ token.json generated successfully")

if __name__ == "__main__":
    main()