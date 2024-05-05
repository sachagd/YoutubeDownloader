// background.js - Handles the browser action click and communicates with the content script and native application.

// Listen for a click on the browser action (extension icon)
browser.browserAction.onClicked.addListener((tab) => {
  // Send a message to the content script
  browser.tabs.sendMessage(tab.id, {action: 'download_audio'}).then(response => {
      // Check if the URL is a YouTube video URL
      if (response.url.includes("youtube.com/watch")) {
          sendMessageToNativeApp(response.url);
      }
  }).catch(error => console.error(`Error sending message to content script: ${error}`));
});

function sendMessageToNativeApp(videoUrl) {
  var message = { url: videoUrl };
  browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', message, response => {
      if (browser.runtime.lastError) {
          console.error('Error sending message to native application:', browser.runtime.lastError.message);
      } else {
          console.log('Response from native application:', response);
      }
  });
}
