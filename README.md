# YouTubeDownloader

**YouTubeDownloader** is a Firefox extension that allows you to download YouTube videos and playlists in MP3 and MP4 formats. You can also select specific parts of a video and choose the resolution for MP4 files.

This repository represents the local component of the extension. It will not work unless you install the corresponding [Firefox add-on](https://addons.mozilla.org/fr/firefox/addon/youtubedownloader/).

## Installation

###  Windows
> **Warning:** The executable provided in the releases is flagged as a Trojan by Windows Defender because it's unsigned. As a result, init.bat runs a command to exclude it from Defender scans. Proceed means that you completely trust me; otherwise, download the source code to use it directly (may involve more steps to setup).
1. **Install FFmpeg (may take a bit):**
   ```bash
   winget install ffmpeg
   ```
2. **Download [ytdl-win.zip](https://github.com/sachagd/YoutubeDownloader/releases/download/v1.3/ytdl-win.zip)** and unzip it.  
   _Do not execute `main.exe` directly._
3. **Run `init.bat` as Administrator.**

---

### MacOS
1. **Install FFmpeg (may take a bit):**
   ```bash
   brew install ffmpeg
   ```
2. **Check your architecture:**
   ```bash
   uname -m
   ```
   - If it prints `arm64`, download [ytdl-macos-arm64.zip](https://github.com/sachagd/YoutubeDownloader/releases/download/v1.3/ytdl-macos-arm64.zip).  
   - If it prints `x86_64`, download [ytdl-macos-x86_64.zip](https://github.com/sachagd/YoutubeDownloader/releases/download/v1.3/ytdl-macos-x86_64.zip).
3. **Unzip and run the setup script:**
   ```bash
   chmod +x init.sh
   ./init.sh
   ```

---

### Ubuntu
1. **Install FFmpeg (may take a bit):**
   ```bash
   sudo apt install ffmpeg
   ```
2. **Download [ytdl-ubuntu.zip](https://github.com/sachagd/YoutubeDownloader/releases/download/v1.3/ytdl-ubuntu.zip)** and unzip it.
3. **Run the setup script:**
   ```bash
   chmod +x init.sh
   ./init.sh
   ```
---

## Accessing Extension Settings

1. Open a new tab and search `about:addons`.  
2. Find **YouTubeDownloader** in the list.  
3. Click **Options** (or **Preferences**) to change the settings.

Settings are persistent between download so you don't need to set them each time

## How to Use the Extension

1. Navigate to the YouTube video or playlist you want to download.  
2. Click the extension icon in the Firefox toolbar to start the download.  

## Additional Information
- By default, files are saved in the extension directory, in a folder named output.
- The **Timestamps** box is empty by default, meaning the entire YouTube video will be downloaded.
- The format for the timestamps is HH:MM:SS.MS (ffmpeg format). For instance, formats like 1:15 or 10 are understood as 1 minute 15 seconds and 10 seconds respectively.
- iTunesSync allows you to automatically add songs to your itunes library. This options will only work on Windows and MacOS. Open Itunes before using it.