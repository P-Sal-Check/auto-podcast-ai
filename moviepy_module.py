from moviepy import editor
import requests
from PIL import Image
from io import BytesIO

class MoviepyModule:
    def __init__(self) -> None:
        pass

    def create_video(self, mp3_file, image_url, output_file):
        # Download the image
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.save('thumbnail.jpg')
        
        # Load audio and image to moviepy
        audio = editor.AudioFileClip(mp3_file)
        image = editor.ImageClip('thumbnail.jpg', duration=audio.duration)
        
        # Set audio to image clip
        videoclip = image.set_audio(audio)
        
        # Write the result to a file
        videoclip.write_videofile(output_file, codec='libx264', fps=24)

