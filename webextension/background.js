browser.browserAction.onClicked.addListener((tab) => {
    browser.storage.local.get(['format', 'standardPath', 'resolution', 'timestamps', 'filenamePreference', 'iTunesSync', 'iTunesPath']).then(settings => {
        const iTunesSync = settings.iTunesSync || false;
        const path = iTunesSync ? (settings.iTunesPath || 'output') : (settings.standardPath || 'output');
        const format = settings.format || 'mp3';
        const resolution = settings.resolution || null;
        const timestamps = settings.timestamps || null;
        const filenamePreference = settings.filenamePreference !== undefined ? settings.filenamePreference : true;
        browser.tabs.sendMessage(tab.id, {action: 'download'}).then(response => {
            if (response.url.includes("youtube.com/watch")) {
                sendMessageToNativeApp(tab, response.url, format, path, resolution, "video", timestamps, filenamePreference, iTunesSync);
            }
            if (response.url.includes("youtube.com/playlist")){
                sendMessageToNativeApp(tab, response.url, format, path, resolution, "playlist", timestamps, filenamePreference, iTunesSync);
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
    }) ;
}

