from dotenv import load_dotenv
import os
import openai


class OPENAI:
    def __init__(self) -> None:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        

    def chatCompletion(self, title:str, contents:str):
        print(f"chat completion 요청, 제목 {title}")
        prompt = f"Here's a news article, and I want to use it as the content of a five-minute podcast, so I'd like you to write a script for the podcast. The podcast should be delivered in natural Korean, like an announcer speaking. The title is {title} and the content is {contents}."
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages= [
                {"role": "system","content": "You are a Korean announcer. Please write a script for a five-minute podcast."},
                {"role": "user","content": prompt,}]
        )

        return {
            "message": chat_completion['choices'][0]['message']['content']
            }