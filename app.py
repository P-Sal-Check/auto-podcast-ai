import os
import news_scrap
import openai_mod
import datetime
import gcp_tts
import moviepy_module
import youtube_module

class APP:
    def __init__(self) -> None:
        self.newsscrap = news_scrap.NEWSSCRAP()
        self.openai_client = openai_mod.OPENAI()
        self.gcp_client = gcp_tts.GCPTTS()
        self.moviepy_client = moviepy_module.MoviepyModule()
        self.youtube_client = youtube_module.YouTubeUploader()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"


    def run(self):
        # 뉴스 긁어오기
        newses = self.newsscrap.getNewses()
        # 뉴스를 하나씩 읽어서 openai에 요청
        for news in newses[:1]:
            title = news.title
            url = news.url
            contents = self.newsscrap.getContents(url)
            urlToImage = news.urlToImage
            print(f"제목: {title}, openai 요청 시작")
            chat_completion_contents = self.openai_client.chatCompletion(title, contents)['message']
            # gcp tts의 응답을 mp3 파일로 저장
            print(f"제목: {title}, gcp tts 요청 시작")
            audio_file_name = self.gcp_client.get_tts(title, chat_completion_contents)
            # mp3 파일에 썸네일 이미지만 붙여서 mp4로 변환
            print(f"제목: {title}, mp4 변환 시작")
            self.moviepy_client.create_video(audio_file_name, urlToImage, f"videos/{title}.mp4")
            # youtube에 업로드
            print(f"제목: {title}, youtube 업로드 시작")
            self.youtube_client.upload_video(f"videos/{title}.mp4", title, '''
            이 뉴스는 테스트 중인 뉴스입니다. 뉴스는 인공지능이 작성했습니다.
            ''', "25", "public")
            print(f"제목: {title}, 업로드 완료")
            

    def getNewses(self):
        return self.newsscrap.getNewses()
    
    def startSample(self):
        print("샘플 시작")
        newses = self.newsscrap.getNewses()
        sample_news = newses[0]
        title = sample_news['title']
        url = sample_news['url']
        contents = self.newsscrap.getContents(url)
        chat_completion = self.openai_client.chatCompletion(title, contents)
        message = chat_completion['message']
        print(message)
        today = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"{title}_{today}.txt"
        # txt로 저장
        with open(f"today/{filename}", "w", encoding="utf-8") as f:
            f.write(message)
        print(f"파일 저장 완료 {filename}")
    
    def makeSampleTts(self):
        # 20230528 폴더에서 txt 파일 목록 읽어옴
        dir = "20230528"
        files = os.listdir(dir)
        for file in files:
            with open(f"{dir}/{file}", "r", encoding="utf-8") as f:
                title = file.split(".")[0]
                contents = f.read()
                print(f"제목: {title}")
                print(f"내용: {contents}")
                filename = self.gcp_client.get_tts(title, contents)
                




app = APP()
app.run()