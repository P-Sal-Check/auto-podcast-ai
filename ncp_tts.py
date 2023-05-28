import os
import sys
import urllib.request
import requests
from dotenv import load_dotenv

class NcpTts:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("NCP_ACCESS_KEY_ID")
        self.client_secret = os.getenv("NCP_SECRET_KEY")
        
        self.url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

        
        self.response = None
        self.rescode = None
        self.response_body = None
        self.filename = None

    def get_tts(self, text):
        encText = urllib.parse.quote(text)
        data = "speaker=nara&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
        print("encoding text: " + encText, type(encText))
        print("data: " + data, type(data))
        print("data.encode('utf-8')", data.encode('utf-8'), type(data.encode('utf-8')))
        # request = urllib.request.Request(self.url)
        # request.add_header("X-NCP-APIGW-API-KEY-ID",self.client_id)
        # request.add_header("X-NCP-APIGW-API-KEY",self.client_secret)
        # self.response = urllib.request.urlopen(request, data=(data.encode('utf-8')))
        headers = {
            "X-NCP-APIGW-API-KEY-ID":self.client_id,
            "X-NCP-APIGW-API-KEY":self.client_secret,
            "Content-Type":"application/x-www-form-urlencoded"
        }
        self.response = requests.post(
            self.url, 
            data=(data.encode('utf-8')), 
            headers=headers
            )
        print("response: " + str(self.response), type(self.response))
        print("content: " + str(self.response.content), type(self.response.content))

        # self.rescode = self.response.getcode()
        self.rescode = (self.response.status_code)
        
        if(self.rescode==200):
            print("TTS mp3 저장")
            # self.response_body = self.response.read()
            self.response_body = self.response.content
            self.filename = "1111.mp3"
            with open(self.filename, 'wb') as f:
                f.write(self.response_body)
        else:
            print("Error Code:" + str(self.rescode), self.response_body)
        return self.filename
    

if __name__ == "__main__":
    ncp_tts = NcpTts()
    filename = ncp_tts.get_tts("안녕하세요. 저는 김보석입니다. 반갑습니다.")
    print(filename)