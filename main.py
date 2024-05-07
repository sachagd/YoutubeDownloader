import sys
import json
import logging
import os
import subprocess
from pytube import YouTube, Playlist
from bs4 import BeautifulSoup
from tkinter import Tk, filedialog
import requests

# Setup logging
logging.basicConfig(filename='youtube_urls.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def get_complete_video_title(video_url):
    """ Extracts and returns the complete title of the YouTube video. """
    response = requests.get(video_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find("title")
    complete_title = title_tag.text.strip()
    if complete_title.endswith(" - YouTube"):
        complete_title = complete_title[:-10]
    return complete_title

def download_video(video_url, output_path, format, resolution, startTime, endTime):
    """ Downloads the video and converts it to specified format. """
    try:
        complete_title = get_complete_video_title(video_url).replace('"',"'").replace("|"," ").replace("/"," ").replace(":", " ").replace("\\\\", " ")
        yt = YouTube(video_url)
        if format == 'mp3':
            stream = yt.streams.filter(only_audio=True,file_extension='mp4').first()
        else:
            stream = yt.streams.filter(res=resolution,file_extension='mp4').first()
            if not stream:
                available_resolutions = {stream.resolution for stream in yt.streams.filter(file_extension='mp4') if stream.resolution}
                send_message({
                    'error': f"No streams available at resolution {resolution}",
                    'availableResolutions': list(available_resolutions)
                })
        
        filename = f"{complete_title}.mp4"
        stream.download(output_path=output_path, filename=filename)
        
        if format == 'mp3':
            input_path = os.path.join(output_path, filename)
            subprocess.run(f'ffmpeg -i "{input_path}" -map 0:a:0 -acodec libmp3lame "{os.path.join(output_path, f"{complete_title}.mp3")}"', shell=True)
            os.remove(input_path)
        
        if not startTime and not endTime:
            uncut_file_path = os.path.join(output_path, f"{complete_title}.{format}")
            temp_file_path = os.path.join(output_path, f"{complete_title}_temp.{format}")
            ffmpeg_cmd = ['ffmpeg', '-i', uncut_file_path]

            if startTime is not None:
                ffmpeg_cmd += ['-ss', startTime]

            if endTime is not None:
                ffmpeg_cmd += ['-to', endTime]
                
            ffmpeg_cmd += ['-c', 'copy', temp_file_path]
            subprocess.run(ffmpeg_cmd, check=True)
            os.remove(uncut_file_path)
            os.rename(temp_file_path,uncut_file_path)

        logging.info(f"File '{filename}' downloaded successfully.")
    except Exception as e:
        logging.error(f"Failed to download and convert {complete_title}: {e}")

def download_playlist(playlist_url, output_path, format, resolution, startTime, endTime):
    playlist = Playlist(playlist_url)
    for video_url in playlist.video_urls:
        download_video(video_url, output_path, format, resolution, startTime, endTime)

def select_folder():
    """Open a folder selection dialog and return the selected path."""
    root = Tk()
    root.withdraw()  
    folder_path = filedialog.askdirectory()
    return folder_path

def read_message():
    """ Reads a message from the stdin buffer and returns it. """
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
    
def send_message(response):
    """Send a message to stdout."""
    encoded_content = json.dumps(response).encode('utf-8')
    encoded_length = len(encoded_content).to_bytes(4, byteorder='little')
    sys.stdout.buffer.write(encoded_length)
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.flush()

def main():
    """ Main loop to process incoming messages continuously. """
    while True:
        data = read_message()
        if data['action'] == 'download': 
            if data and 'url' in data and 'format' in data and 'path' in data and 'type' in data and 'resolution' in data:
                logging.info(f"Received YouTube URL: {data['url']}, format: {data['format']}, path: {data['path']}, resolution: {data['resolution']} and type: {data['type']}")
                if data['type'] == 'video':
                    download_video(data['url'], data['path'], data['format'], data['resolution'], data['startTime'], data['endTime'])
                if data['type'] == 'playlist':
                    download_playlist(data['url'], data['path'], data['format'], data['resolution'], data['startTime'], data['endTime'])
            else:
                logging.error("No URL, path, format, resolution or type (video or playlist) received, or incorrect data format")
        if data['action'] == 'select_folder':
            path = select_folder()
            logging.info(f"Selected folder path: {path}")
            send_message({'path': path})

if __name__ == "__main__":
    main()
