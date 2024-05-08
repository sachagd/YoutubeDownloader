// Listen for messages from the background script
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'download') {
        console.log('Received download trigger');
        const videoUrl = window.location.href; // Assuming you want to download the current video
        sendResponse({url: videoUrl});
    }
    if (message.action === 'resolution_error'){
        alert(message.error + '\nAvailable resolutions: ' + message.availableResolutions.join(', '));
    }
});
