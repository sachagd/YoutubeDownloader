import sys
import json
import logging
import os
import subprocess
from pytube import YouTube
from bs4 import BeautifulSoup
import requests

# Setup logging
logging.basicConfig(filename='youtube_urls.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def get_complete_video_title(video_url):
    response = requests.get(video_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find("title")
    complete_title = title_tag.text.strip()
    if complete_title.endswith(" - YouTube"):
        complete_title = complete_title[:-10]
    return complete_title

def download_and_convert(video_url, output_path):
    try:
        complete_title = get_complete_video_title(video_url).replace('"',"'").replace("|"," ").replace("/"," ").replace(":", " ").replace("\\", " ")
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        video_filename = f"{complete_title}.mp4"
        audio_stream.download(output_path=output_path, filename=video_filename)
        input_path = os.path.join(output_path, video_filename)
        subprocess.run(f'ffmpeg -i "{input_path}" -map 0:a:0 -acodec libmp3lame "{os.path.join(output_path, f"{complete_title}.mp3")}"', shell=True, stderr=subprocess.DEVNULL)
        os.remove(input_path)
        logging.info(f"Audio of '{complete_title}' downloaded and converted successfully.")
    except Exception as e:
        logging.error(f"Failed to download and convert {complete_title}: {e}")

def read_message():
    try:
        raw_length = sys.stdin.buffer.read(4)
        if not raw_length:
            sys.exit(0)
        message_length = int.from_bytes(raw_length, 'little')
        message = sys.stdin.buffer.read(message_length).decode('utf-8')
        return json.loads(message)
    except Exception as e:
        logging.error(f"Error reading message: {e}")
        return None

def main():
    while True:
        data = read_message()
        if data and 'url' in data:
            logging.info(f"Received YouTube URL: {data['url']}")
            download_and_convert(data['url'], "output")
        else:
            logging.error("No URL received or incorrect data format")

if __name__ == "__main__":
    main()
