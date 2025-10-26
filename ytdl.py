import sys
import os
import logging

if sys.platform == "darwin":
    import certifi
    import shutil
    os.environ["SSL_CERT_FILE"] = certifi.where()
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        os.environ["PATH"] += os.pathsep + ffmpeg_dir
    else:
        logging.error("FFmpeg not found. Please install it via Homebrew (brew install ffmpeg) or ensure it's in PATH.")

import json
import subprocess
from pytubefix import YouTube, Playlist
from pytubefix.helpers import safe_filename
from tkinter import Tk, filedialog

logging.basicConfig(filename='youtube_urls.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def download_video(video_url, path, format, resolution, timestamps, filename_preference, iTunesSync):
    """ Downloads the video and converts it to specified format. """
    try:
        logging.info("avant Youtube")
        yt = YouTube(video_url)
        logging.info("avant yt.title")
        title = safe_filename(yt.title) if filename_preference else f"output_{len(os.listdir(path))}"
        logging.info("après yt.title")
        if format == 'mp3':
            stream = yt.streams.get_audio_only()
            if iTunesSync and not timestamps:
                '''
                Mp3 files downloaded with pytubefix do not include metadata such as bitrate that iTunes needs to import them.
                '''
                stream.download(output_path=path, filename=f"{title}_audio.mp3")
                input_path = os.path.join(path, f"{title}_audio.mp3")
                runcommand(["ffmpeg", '-y', '-nostdin', '-i', input_path, '-acodec', 'mp3', os.path.join(path, f"{title}.mp3")])
                downloaded_video.append(f"{title}.mp3")
                os.remove(input_path)
            else:
                logging.info("avant stream.download")
                stream.download(output_path=path, filename=f"{title}.mp3")
                logging.info("après stream.download")
                
            if timestamps:
                uncut_path = os.path.join(path, f"{title}.mp3")
                for i, ts in enumerate(timestamps):
                    part_filename = f"{title}_part_{i+1}.mp3"
                    part_path = os.path.join(path, part_filename)
                    ffmpeg_cmd = ["ffmpeg", '-y', '-nostdin']

                    if ts['startTime']:
                        ffmpeg_cmd += ['-ss', ts['startTime']]

                    if ts['endTime']:
                        ffmpeg_cmd += ['-to', ts['endTime']]

                    ffmpeg_cmd += ['-i', uncut_path, '-c:a', 'mp3', part_path]
                    runcommand(ffmpeg_cmd)

                    if iTunesSync:
                        downloaded_video.append(part_filename)

                    logging.info(f"{part_filename} downloaded successfully.")
                os.remove(uncut_path)
            else:
                logging.info(f"{title} downloaded successfully.")
        else:
            '''
            From what i've tested, progressive streams are rarely available at high resolutions.
            Workaround: download separate audio/video and merge.
            '''
            video_stream = yt.streams.filter(res=resolution).first()
            if not video_stream:
                available_resolutions = sorted(
                    {s.resolution for s in yt.streams.filter(file_extension='mp4') if s.resolution},
                    key=lambda r: int(r.replace('p', ''))
                )
                send_message({
                    'error': f"No streams available at resolution {resolution}",
                    'availableResolutions': available_resolutions
                })
                logging.error(f"No streams available at resolution {resolution}, available: {available_resolutions}")
                return
            if video_stream.is_progressive:
                video_stream.download(output_path=path, filename=f"{title}.mp4")
                if timestamps:
                    uncut_path = os.path.join(path, f"{title}.mp4")
                    for i, ts in enumerate(timestamps):
                        part_filename = f"{title}_part_{i+1}.mp4"
                        part_path = os.path.join(path, part_filename)
                        ffmpeg_cmd = ["ffmpeg", '-y', '-nostdin']

                        if ts['startTime']:
                            ffmpeg_cmd += ['-ss', ts['startTime']]

                        if ts['endTime']:
                            ffmpeg_cmd += ['-to', ts['endTime']]

                        ffmpeg_cmd += ['-i', uncut_path, '-c:a', 'mp3', '-c:v', 'copy', part_path]
                        runcommand(ffmpeg_cmd)

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
                        output_part_filename = f"{title}_part_{i+1}.mp4"
                        output_part_path = os.path.join(path, output_part_filename)
                        ffmpeg_cmd = ["ffmpeg", '-y', '-nostdin']

                        if ts['startTime']:
                            ffmpeg_cmd += ['-ss', ts['startTime']]

                        if ts['endTime']:
                            ffmpeg_cmd += ['-to', ts['endTime']]

                        video_ffmpeg_cmd = ffmpeg_cmd + ['-i', video_path, '-c:v', 'copy', video_part_path]
                        audio_ffmpeg_cmd = ffmpeg_cmd + ['-i', audio_path, '-c:a', 'mp3', audio_part_path]
                        runcommand(video_ffmpeg_cmd)
                        runcommand(audio_ffmpeg_cmd)
                        runcommand(["ffmpeg", '-y', '-nostdin', '-i', video_part_path, '-i', audio_part_path, '-c', 'copy', output_part_path])
                        os.remove(video_part_path)
                        os.remove(audio_part_path)
                        if iTunesSync:
                            downloaded_video.append(output_part_filename)
                        logging.info(f"{output_part_filename} downloaded successfully.")
                else:
                    runcommand(["ffmpeg", '-y', '-nostdin', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'mp3', os.path.join(path, f'{title}.mp4')])
                    if iTunesSync:
                        downloaded_video.append(f"{title}.mp4")
                    logging.info(f"{title} downloaded successfully.")
                os.remove(audio_path)
                os.remove(video_path)
    except Exception as e:
        logging.exception(f"Failed to download and convert {video_url}: {e}")

def runcommand(command):
    if sys.platform == "win32":
        subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def download_playlist(playlist_url, path, format, resolution, timestamps, filename_preference, iTunesSync):
    playlist = Playlist(playlist_url)
    for video_url in playlist.video_urls:
        download_video(video_url, path, format, resolution, timestamps, filename_preference, iTunesSync)

def iTunesSyncWin(path):
    import win32com.client
    iTunes = win32com.client.Dispatch("iTunes.Application")
    library = iTunes.LibraryPlaylist
    for filename in downloaded_video:
        library.AddFile(os.path.join(os.path.abspath(path), filename))

def iTunesSyncMacos(path):
    for filename in downloaded_video:
        file_path = os.path.join(os.path.abspath(path), filename)
        subprocess.run([
            "osascript", "-e",
            f'tell application "Music" to add POSIX file "{file_path}" to library playlist 1'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
        if data['action'] == 'download':
            if data and 'url' in data and 'format' in data and 'path' in data and 'type' in data and 'resolution' in data and 'timestamps' in data and 'filenamePreference' in data and 'iTunesSync' in data:
                logging.info(f"Received YouTube URL: {data['url']}, format: {data['format']}, path: {data['path']}, resolution: {data['resolution']}, type: {data['type']}, timestamps: {data['timestamps']}, filenamePreference: {data['filenamePreference']} and iTunesSync: {data['iTunesSync']}")
                downloaded_video = []
                if data['type'] == 'video':
                    download_video(data['url'], data['path'], data['format'], data['resolution'], data['timestamps'], data['filenamePreference'], data['iTunesSync'])
                if data['type'] == 'playlist':
                    download_playlist(data['url'], data['path'], data['format'], data['resolution'], data['timestamps'], data['filenamePreference'], data['iTunesSync'])
                if data['iTunesSync']:
                    if sys.platform == "win32":
                        iTunesSyncWin(data['path'])
                    elif sys.platform == "darwin":
                        iTunesSyncMacos(data['path'])
                    elif sys.platform.startswith("linux"):
                        logging.warning("iTunesSync is not available on linux")
            else:
                logging.error("Some data was not received")
            send_message({'action': "execution ended"})
            break
        if data['action'] == 'select_folder':
            path = select_folder()
            logging.info(f"Selected folder path: {path}")
            send_message({'path': path})
            break

if __name__ == "__main__":
    main()