import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.service_account import Credentials

class YouTubeUploader:
    def __init__(self):

        # Use the client_secrets file downloaded from your project
        self.client_secrets_file = "client_secrets.json"

        # Use the YouTube Data API v3
        self.api_service_name = "youtube"
        self.api_version = "v3"

        self.youtube = None

    def get_authenticated_service(self):
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, ["https://www.googleapis.com/auth/youtube.upload"])
        credentials = flow.run_local_server()
        credentials = Credentials.from_service_account_file(
            self.client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )
        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials)
        return youtube

    def upload_video(self,file_path, title, description, category, privacy):
        self.youtube = self.get_authenticated_service()

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": category,
                    "description": description,
                    "title": title
                },
                "status": {
                    "privacyStatus": privacy
                }
            },
            media_body=googleapiclient.http.MediaFileUpload(file_path)
        )
        response = request.execute()
        return response
    

