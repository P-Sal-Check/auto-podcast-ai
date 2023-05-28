import os
import news_scrap
import openai_mod
import datetime
import gcp_tts

class APP:
    def __init__(self) -> None:
        self.newsscrap = news_scrap.NEWSSCRAP()
        self.openai_client = openai_mod.OPENAI()
        self.gcp_client = gcp_tts.GCPTTS()
    
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
                




    
    


if __name__ == "__main__":
    print("app 실행")
    instance = APP()
    instance.makeSampleTts()