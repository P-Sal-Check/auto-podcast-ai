
from datetime import datetime
import os
import feedparser
import json
from newspaper import Article
import openai
from dotenv import load_dotenv
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def rss_to_json(url):
    
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Create an empty list to store the feed items
    feed_items = []

    

    for entry in feed.entries:
        # For each entry, create a dictionary of data
        
        feed_item = {
            "title": entry.title,
            "link": entry.link,
            "pubDate": entry.published,
            "description": entry.description,
            "traffic": entry.ht_approx_traffic,
            "picture": '',
            "picture_source": '',
        }

        if hasattr(entry, 'ht_picture'):
            feed_item['picture'] = entry.ht_picture
            feed_item['picture_source'] = entry.ht_picture_source
        print(entry)

        # If the RSS feed has 'ht:news_item', parse that as well
        # if hasattr(entry, 'ht:news_item'):
            
        news_items = []

        news_url = entry['ht_news_item_url']
        
        news_item = {
            "title": entry['ht_news_item_title'],
            "snippet": entry['ht_news_item_snippet'],
            "url": news_url,
            "source": entry['ht_news_item_source']
        }
        news_items.append(news_item)
        feed_item['news_item'] = news_items

        feed_items.append(feed_item)

        news_contents = news_url_to_text(news_url)
        # openai에 news contents와 키워드(title)을 주고 title이 실시간으로 핫한 이유, 썸머리, 어떤 점이 쟁점이 되고 있는지 분석하는 글을 요청한다.
        prompt = f"Here are the most popular search terms and news content in Korea in real time, and I want you to write a post based on the news content that explains why the keywords are hot right now, summarizes, analyzes, etc. Please write in natural Korean. keywords: {entry.title} news content: {news_contents} Please write in the following format. Keyword : \nReason:\nSummary and analysis: \n\n "

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages= [
                
                {"role": "user","content": prompt,}]
        )
        print(chat_completion)
        print(chat_completion['choices'][0]['message']['content'])
        feed_item['content'] = chat_completion['choices'][0]['message']['content']
        return



    

    json_content = json.dumps(feed_items, ensure_ascii=False)
    # 파일로 저장
    today = datetime.today().strftime("%Y%m%d")
    with open(f'trend/{today}.json', 'w', encoding='utf-8') as f:
        f.write(json_content)
    return json_content

def news_url_to_text(url):
    print('news_url_to_text', url)
    news = Article(url, language="ko")
    news.download()
    news.parse()
    contents = news.text
    return contents




url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"
print(rss_to_json(url))

