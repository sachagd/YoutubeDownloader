// Listens for a click on the browser action (extension icon)
browser.browserAction.onClicked.addListener((tab) => {
    // Retrieve both the preferred format and the download path
    browser.storage.local.get(['downloadFormat', 'downloadPath', 'downloadResolution', 'startTime', 'endTime']).then(settings => {
        const downloadFormat = settings.downloadFormat || 'mp3';
        const downloadPath = settings.downloadPath || 'output';  
        const downloadResolution = settings.downloadResolution || null;
        const startTime = settings.startTime || null;
        const endTime = settings.endTime || null;
        // Send a message to the content script with the format and path included
        browser.tabs.sendMessage(tab.id, {action: 'download'}).then(response => {
            if (response.url.includes("youtube.com/watch")) {
                sendMessageToNativeApp(response.url, downloadFormat, downloadPath, downloadResolution, "video", startTime, endTime);
            }
            if (response.url.includes("youtube.com/playlist")){
                sendMessageToNativeApp(response.url, downloadFormat, downloadPath, downloadResolution, "playlist", startTime, endTime);
            }
        }).catch(error => console.error(`Error sending message to content script: ${error}`));
    });
});

// Updated function to send messages to the native application including the path
function sendMessageToNativeApp(url, format, path, resolution, type, startTime, endTime) {
    var message = {action: 'download', url: url, format: format, path: path, resolution: resolution, type: type, startTime: startTime, endTime: endTime};
    browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', message, response => {
        if (browser.runtime.lastError) {
            console.error('Error sending message to native application:', browser.runtime.lastError.message);
            alert('Failed to communicate with the native application. Please ensure it is installed and configured correctly.');
        } else {
            console.log('Response from native application:', response);
            // Check the response for error or success
            if (response.error) {
                alert(response.error + '\nAvailable resolutions: ' + response.availableResolutions.join(', '));
            }
        }
    });
}

