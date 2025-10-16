# YouTubeDownloader

**YouTubeDownloader** is a Firefox extension that allows you to download YouTube videos and playlists in MP3 and MP4 formats. You can also select specific parts of a video and choose the resolution for MP4 files.

This repository represents the local component of the extension. It will not work unless you install the corresponding [Firefox add-on](https://addons.mozilla.org/fr/firefox/addon/youtubedownloader/).

## Installation

1. **Download the** [local component](https://github.com/sachagd/YoutubeDownloader/releases/download/v1.2) **and unzip it. Do not execute `main.exe`.**

   **Warning:** `main.exe` is flagged as a Trojan by Windows Defender because from its perspective it is a random exe that downloads content from the internet. As a result, `init.bat` runs a command to exclude its folder from Defender scans. Proceed means that you completely trust me; otherwise, download the source code to use it directly or build the project yourself.

2. **Run `init.bat` as Administrator**  
   - Excludes the folder from Defender  
   - Adds the native messaging registry key  

   Linux and macOS users must use the source code.

## How to Use the Extension

1. Navigate to the YouTube video or playlist you want to download.  
2. Click the extension icon in the Firefox toolbar.  
3. Select your options and start the download.

## Accessing Extension Settings

1. Open a new tab and go to `about:addons`.  
2. Find **YouTubeDownloader** in the list.  
3. Click **Options** to adjust settings.

## Additional Information
- By default, files are saved in the extension directory, in a folder named output.
- The **Timestamps** box is empty by default, meaning the entire YouTube video will be downloaded.
- The format for the timestamps is HH:MM:SS.MS (ffmpeg format). For instance, formats like 1:15 or 10 are understood as 1 minute 15 seconds and 10 seconds respectively.
- iTunesSync allows you to automatically add songs to your itunes library. This options will only work on Windows and MacOS. Open Itunes before using it.