from fastapi import FastAPI
from dotenv import load_dotenv
import os
import openai
import requests
from newspaper import Article
from google.cloud import texttospeech

load_dotenv()
app = FastAPI()
# Instantiates a client
tts_client = texttospeech.TextToSpeechClient()





@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    await print_env()
    return {"message": "Test"}


@app.get("/print_env")
async def print_env():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    newsInfoUrl = f"https://newsapi.org/v2/top-headlines?country=kr&apiKey={os.getenv('NEWSAPI_KEY')}"
    response = requests.get(newsInfoUrl)
    if not response.status_code == 200:
        print("Error")
        return
    data = response.json()
    articles = data["articles"]
    for article in articles:
        print(article["title"])
        title = article["title"]
        print(article["url"])
        url = article["url"]
        print(article["publishedAt"])
        publishedAt = article["publishedAt"]

        news = Article(url, language="ko")
        news.download()
        news.parse()
        contents = news.text
        print(news.text)
        prompt = f"Here's a news article, and I want to use it as the content of a five-minute podcast, so I'd like you to write a script for the podcast. The podcast should be delivered in natural Korean, like an announcer speaking. The title is {title} and the content is {contents}."
        total_token = 4096
        used_token = len(prompt)
        remaining_token = total_token - used_token
        print(used_token)
        # return
        
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages= [
                {"role": "system","content": "You are a Korean announcer. Please write a script for a five-minute podcast."},
                {"role": "user","content": prompt,}]
        )
        
        print(chat_completion)
        print(chat_completion['choices'][0]['message']['content'])
        return {"message": chat_completion['choices'][0]['message']['content']}

        
        # print(response)
        print("")
        break
    # article = Article(url, language="ko")
    # article.download()
    # article.parse()
    # print(article.title)
    
    


