import sys
import json
import logging
import os
import subprocess
from pytubefix import YouTube, Playlist
from bs4 import BeautifulSoup
from tkinter import Tk, filedialog
import requests
import win32com.client
import threading
import time

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

def download_video(video_url, path, format, resolution, timestamps, filenamePreference, iTunesSync):
    """ Downloads the video and converts it to specified format. """
    try:
        
        logging.info("into the download_video")
        if filenamePreference:
            complete_title = get_complete_video_title(video_url)
            logging.info("got the complete title")
            for c in '<>:"/\\|?*':
                complete_title = complete_title.replace(c, " ")
        else:
            complete_title = f"output_{len(os.listdir(path))}"
        yt = YouTube(video_url)
        if format == 'mp3':
            logging.info("searching the audio")
            stream = yt.streams.get_audio_only()
            logging.info("got the audio")
            logging.info(stream)
            logging.info(yt.streams)
            if iTunesSync and not timestamps:
                '''
                Mp3 files downloaded with pytubefix do not include metadata such as bitrate that iTunes needs to import them.
                '''
                logging.info("downloading the audio")
                t = threading.Thread(target=lambda: stream.download(output_path=path, filename=f"{complete_title}_audio.mp3"))
                t.start()
                t.join(60)  # wait 60s max
                if t.is_alive():
                    raise TimeoutError(f"Download stuck for {complete_title}")
                logging.info("downloaded the audio")
                input_path = os.path.join(path, f"{complete_title}_audio.mp3")
                subprocess.run(["ffmpeg", '-y', '-nostdin', '-i', input_path, '-acodec', 'mp3', os.path.join(path, f"{complete_title}.mp3")], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                downloaded_video.append(f"{complete_title}.mp3")
                os.remove(input_path)
            else:
                logging.info("downloading the audio")
                t = threading.Thread(target=lambda: stream.download(output_path=path, filename=f"{complete_title}.mp3"))
                logging.info("roergoepgreroegerreg")
                t.start()
                logging.info("fsfddfs")
                start = time.time()
                logging.info("fehseifesij")
                while t.is_alive() and time.time() - start < 60:
                    time.sleep(0.5)
                    logging.info(time.time() - start)
                logging.info("uuhfuhsedhu")
                if t.is_alive():
                    logging.warning(f"Download appears stuck for {complete_title}, skipping...")
                    raise TimeoutError(f"Download stuck for {complete_title}")
                logging.info("downloaded the audio")

            if timestamps:
                uncut_path = os.path.join(path, f"{complete_title}.mp3")
                for i, ts in enumerate(timestamps):
                    part_filename = f"{complete_title}_part_{i+1}.mp3"
                    part_path = os.path.join(path, part_filename)
                    ffmpeg_cmd = ["ffmpeg", '-y', '-nostdin']

                    if ts['startTime']:
                        ffmpeg_cmd += ['-ss', ts['startTime']]

                    if ts['endTime']:
                        ffmpeg_cmd += ['-to', ts['endTime']]

                    ffmpeg_cmd += ['-i', uncut_path, '-c:a', 'mp3', part_path]
                    subprocess.run(ffmpeg_cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

                    if iTunesSync:
                        downloaded_video.append(part_filename)

                    logging.info(f"{part_filename} downloaded successfully.")
                os.remove(uncut_path)
            else:
                logging.info(f"{complete_title} downloaded successfully.")
        else:
            '''
            From what i've tested, progressive streams are rarely available at high resolutions.
            Workaround: download separate audio/video and merge.
            '''
            video_stream = yt.streams.filter(res=resolution).first()
            if not video_stream:
                available_resolutions = sorted({s.resolution for s in yt.streams.filter(file_extension='mp4') if s.resolution})
                send_message({
                    'error': f"No streams available at resolution {resolution}",
                    'availableResolutions': available_resolutions
                })
                logging.error(f"No streams available at resolution {resolution}, available: {available_resolutions}")
                return
            if video_stream.is_progressive:
                video_stream.download(output_path=path, filename=f"{complete_title}.mp4")
                if timestamps:
                    uncut_path = os.path.join(path, f"{complete_title}.mp4")
                    for i, ts in enumerate(timestamps):
                        part_filename = f"{complete_title}_part_{i+1}.mp4"
                        part_path = os.path.join(path, part_filename)
                        ffmpeg_cmd = ["ffmpeg", '-y', '-nostdin']

                        if ts['startTime']:
                            ffmpeg_cmd += ['-ss', ts['startTime']]

                        if ts['endTime']:
                            ffmpeg_cmd += ['-to', ts['endTime']]

                        ffmpeg_cmd += ['-i', uncut_path, '-c:a', 'mp3', '-c:v', 'copy', part_path]
                        subprocess.run(ffmpeg_cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

                        if iTunesSync:
                            downloaded_video.append(part_filename)
                        
                        logging.info(f"{part_filename} downloaded successfully.")
                    os.remove(uncut_path)
            else: 
                audio_stream = yt.streams.get_audio_only()
                video_stream.download(output_path=path, filename="video.mp4")
                audio_stream.download(output_path=path, filename="audio.mp3")
                video_path = os.path.join(path, "video.mp4")
                audio_path = os.path.join(path, "audio.mp3")

                if timestamps:
                    for i, ts in enumerate(timestamps):
                        video_part_path = os.path.join(path, f"video_part_{i+1}.mp4")
                        audio_part_path = os.path.join(path, f"audio_part_{i+1}.mp3")
                        output_part_filename = f"{complete_title}_part_{i+1}.mp4"
                        output_part_path = os.path.join(path, output_part_filename)
                        ffmpeg_cmd = ["ffmpeg", '-y', '-nostdin']

                        if ts['startTime']:
                            ffmpeg_cmd += ['-ss', ts['startTime']]

                        if ts['endTime']:
                            ffmpeg_cmd += ['-to', ts['endTime']]

                        video_ffmpeg_cmd = ffmpeg_cmd + ['-i', video_path, '-c:v', 'copy', video_part_path]
                        audio_ffmpeg_cmd = ffmpeg_cmd + ['-i', audio_path, '-c:a', 'mp3', audio_part_path]
                        subprocess.run(video_ffmpeg_cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        subprocess.run(audio_ffmpeg_cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        subprocess.run(["ffmpeg", '-y', '-nostdin', '-i', video_part_path, '-i', audio_part_path, '-c', 'copy', output_part_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        os.remove(video_part_path)
                        os.remove(audio_part_path)
                        if iTunesSync:
                            downloaded_video.append(output_part_filename)
                        logging.info(f"{output_part_filename} downloaded successfully.")
                else:
                    subprocess.run(["ffmpeg", '-y', '-nostdin', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'mp3', os.path.join(path, f'{complete_title}.mp4')], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if iTunesSync:
                        downloaded_video.append(f"{complete_title}.mp4")
                    logging.info(f"{complete_title} downloaded successfully.")
                os.remove(audio_path)
                os.remove(video_path)
        send_message({'action': "files have been downloaded successfully"})
    except Exception as e:
        logging.exception(f"Failed to download and convert {complete_title}: {e}")

def download_playlist(playlist_url, path, format, resolution, timestamps, filenamePreference, iTunesSync):
    playlist = Playlist(playlist_url)
    for video_url in playlist.video_urls:
        logging.info(video_url)
        download_video(video_url, path, format, resolution, timestamps, filenamePreference, iTunesSync)

def iTunesSync(path):
    iTunes = win32com.client.Dispatch("iTunes.Application")
    library = iTunes.LibraryPlaylist
    for filename in downloaded_video:
        library.AddFile(os.path.join(os.path.abspath(path), filename))

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
    global downloaded_video
    while True:
        data = read_message()
        # data = {'action' : 'download', 'url' : 'https://www.youtube.com/playlist?list=PL-Lb9sJYEEo2X_dxb7oaVJalP2flxg529', 'format': 'mp3', 'path': 'output', 'resolution': None, 'type': 'playlist', 'timestamps': None, 'filenamePreference': True, 'iTunesSync': False}
        if data['action'] == 'download':
            if data and 'url' in data and 'format' in data and 'path' in data and 'type' in data and 'resolution' in data and 'timestamps' in data and 'filenamePreference' in data and 'iTunesSync' in data:
                logging.info(f"Received YouTube URL: {data['url']}, format: {data['format']}, path: {data['path']}, resolution: {data['resolution']}, type: {data['type']}, timestamps: {data['timestamps']}, filenamePreference: {data['filenamePreference']} and iTunesSync: {data['iTunesSync']}")
                downloaded_video = []
                if data['type'] == 'video':
                    download_video(data['url'], data['path'], data['format'], data['resolution'], data['timestamps'], data['filenamePreference'], data['iTunesSync'])
                if data['type'] == 'playlist':
                    download_playlist(data['url'], data['path'], data['format'], data['resolution'], data['timestamps'], data['filenamePreference'], data['iTunesSync'])
                if data['iTunesSync']:
                    iTunesSync(data['path'])
            else:
                logging.error("Some data was not received")
            break
        if data['action'] == 'select_folder':
            path = select_folder()
            logging.info(f"Selected folder path: {path}")
            send_message({'path': path})
            break

if __name__ == "__main__":
    main()