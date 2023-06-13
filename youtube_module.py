import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class YouTubeUploader:
    def __init__(self, file_path, title, description, category, privacy):
        self.file_path = file_path
        self.title = title
        self.description = description
        self.category = category
        self.privacy = privacy

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
        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials)
        return youtube

    def upload_video(self):
        self.youtube = self.get_authenticated_service()

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": self.category,
                    "description": self.description,
                    "title": self.title
                },
                "status": {
                    "privacyStatus": self.privacy
                }
            },
            media_body=googleapiclient.http.MediaFileUpload(self.file_path)
        )
        response = request.execute()
        return response
    

uploader = YouTubeUploader(
    "sample.mp4", 
    "NFT CHEF: 4위로 입상한 TON Global HackaTON의 짱짱 프로젝트 데모", 
    '''이 영상에서는 최근 TON 글로벌 해커톤에서 크라우드 펀딩 분야 4위에 선정된 "NFT CHEF"의 데모를 살펴보겠습니다. NFT CHEF는 차세대 블록체인 기술과 NFT를 결합하여 창작자들에게 독특하고 혁신적인 금융 기회를 제공하는 플랫폼입니다. 블록체인과 NFT의 기능을 최대한 활용하여 공정하고 투명한 크라우드펀딩 환경을 제공하는 이 프로젝트를 통해, 창작자들은 자신의 작품을 새로운 방식으로 모니터링하고 수익을 창출할 수 있게 되었습니다. 이 영상을 통해 NFT CHEF의 플랫폼이 어떻게 작동하는지 자세히 알아보세요.''', 
    "28", 
    "public")
response = uploader.upload_video()
print(response)