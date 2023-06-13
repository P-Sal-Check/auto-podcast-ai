from dotenv import load_dotenv
import os
import openai


class OPENAI:
    def __init__(self) -> None:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        

    def chatCompletion(self, title:str, contents:str):
        print(f"chat completion 요청, 제목 {title}")
        prompt = f"The title is {title} and the content is {contents}."
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages= [
                {"role": "system","content": "Given the title and body of a news story from South Korea, write a 10-minute news podcast script based on this story. The script should only include important information from the story and should be delivered in natural Korean language, written as a Korean announcer would speak. Do not include names of news organizations or reporters, such as 'Yonhap News TV' or 'Reporter Kim Jun-hee'. The script should not include phrases such as 'This is reporter Kim Jun-hee.' The script should contain only informative content. Please provide the title and content of the news story."},
                {"role": "user","content": prompt,}]
        )

        return {
            "message": chat_completion['choices'][0]['message']['content']
            }