// Listen for messages from the background script
browser.runtime.onMessage.addListener((message, sendResponse) => {
    if (message.action === 'download') {
        console.log('Received download trigger');
        const videoUrl = window.location.href; // Assuming you want to download the current video
        // Include the format in the response
        sendResponse({url: videoUrl});
    }
});
