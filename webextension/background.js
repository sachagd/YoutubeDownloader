browser.browserAction.onClicked.addListener((tab) => {
    browser.storage.local.get(['downloadFormat', 'downloadPathStandard', 'downloadResolution', 'timestamps', 'filenamePreference', 'iTunesSync', 'downloadPathiTunesSync']).then(settings => {
        const iTunesSync = settings.iTunesSync || false;
        const downloadPath = iTunesSync ? (settings.downloadPathiTunesSync || 'output') : (settings.downloadPathStandard || 'output');
        const downloadFormat = settings.downloadFormat || 'mp3';
        const downloadResolution = settings.downloadResolution || null;
        const timestamps = settings.timestamps || null;
        const filenamePreference = settings.filenamePreference !== undefined ? settings.filenamePreference : true;
        browser.tabs.sendMessage(tab.id, {action: 'download'}).then(response => {
            if (response.url.includes("youtube.com/watch")) {
                sendMessageToNativeApp(tab, response.url, downloadFormat, downloadPath, downloadResolution, "video", timestamps, filenamePreference, iTunesSync);
            }
            if (response.url.includes("youtube.com/playlist")){
                sendMessageToNativeApp(tab, response.url, downloadFormat, downloadPath, downloadResolution, "playlist", timestamps, filenamePreference, iTunesSync);
            }
        }).catch(error => console.error(`Error sending message to content script: ${error}`));
    });
});

function sendMessageToNativeApp(tab, url, format, path, resolution, type, timestamps, filenamePreference, iTunesSync) {
    var message = {action: 'download', url: url, format: format, path: path, resolution: resolution, type: type, timestamps: timestamps, filenamePreference : filenamePreference, iTunesSync : iTunesSync};
    browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', message, response => {
        if (browser.runtime.lastError) {
            console.error('Error sending message to native application:', browser.runtime.lastError.message);
        } else {
            console.log('Response from native application:', response);
            if (response.error) {
                browser.tabs.sendMessage(tab.id, {action: 'resolution_error', availableResolutions : response.availableResolutions, error : response.error});
            }
        }
    })  ;
}

