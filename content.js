// content.js - This script reacts to messages from the background script.

// Listen for messages from the background script
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'download_audio') {
        console.log('Received download trigger');
        const videoUrl = window.location.href; // Assuming you want to download the current video
        sendResponse({url: videoUrl});
    }
});
