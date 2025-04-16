# YouTubeDownloader

**YouTubeDownloader** is a Firefox extension that allows you to download YouTube videos and playlist in mp3 and mp4 format. It also allows you to select specific parts of a video and choose a resolution for mp4 files.

This repository represent the local part of the extension. It will not work if you don't install the corresponding [extension](https://addons.mozilla.org/fr/firefox/addon/youtubedownloader/) in Firefox.

## Prerequisites
Before using the extension, you must download a few dependencies, you can do the steps manually if you want or if you use linux:

**Execute `init.bat` in Administrator mode:**
   - Installs `pip` if it's not already installed.
   - Installs Python libraries: `Tkinter`, `BeautifulSoup`, `requests`, and `pytubefix`.
   - Installs `ffmpeg` if it's not already installed and adds the file path to the `PATH` environment variable.
   - Adds a registry key.

## How to Use the Extension
Once the extension is properly installed:
1. Navigate to the YouTube video or playlist you want to download.
2. Click on the extension button in the top right corner of Firefox.
3. Click on the YouTubeDownloader extension to start the download process.

## Accessing Extension Settings
To modify the settings of the extension:

1. Open a new Firefox tab and enter `about:addons`.
2. Click on the extension.
3. Click on **Options**.

## Additional Information
- By default, files are saved in the extension directory, in a folder named `output`.
- The **Timestamps** box is empty by default, meaning the entire YouTube video will be downloaded.
- The format for the timestamps is `HH:MM:SS`. Formats like `1:15` or `10` are understood as 1 minute 15 seconds and 10 seconds respectively.
- iTunesSync allows you to automatically add songs to your itunes library.
