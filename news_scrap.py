import json
from dotenv import load_dotenv
import os
import requests
from newspaper import Article
import datetime

class NEWSSCRAP:
    def __init__(self) -> None:
        load_dotenv()
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.newurl = f"https://newsapi.org/v2/top-headlines?country=kr&apiKey={self.newsapi_key}"
        self.newses = self.initNewses()

    def initNewses(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"news_{today}.json"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                # json으로 변환
                self.newses = json.load(f)
            return self.newses

        response = requests.get(self.newurl)
        if not response.status_code == 200:
            print("newsapi.org 에러")
            return None
        data = response.json()
        # json 으로 저장
        self.newses = data["articles"]

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.newses, f, indent=4, ensure_ascii=False)

        return self.newses
    
    def getNewses(self):
        return self.newses
    
    def getContents(self, url):
        news = Article(url, language="ko")
        news.download()
        news.parse()
        contents = news.text
        return contents


        

