from google.cloud import texttospeech
import datetime


class GCPTTS:
    def __init__(self) -> None:
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Wavenet-A",
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
    
    def get_tts(self, title, text):
        today = datetime.datetime.now().strftime("%Y%m%d")
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input, 
            voice=self.voice, 
            audio_config=self.audio_config
            )
        # filename 은 title + 오늘 날짜 + .mp3
        filename = 'audios/' + title + '_' + today + '_' + ".mp3"
        
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            
        
        return filename



    
        