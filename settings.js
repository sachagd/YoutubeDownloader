document.getElementById('selectFolderButton').addEventListener('click', () => {
    browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', {action: 'select_folder'}, response => {
        if (browser.runtime.lastError) {
            console.error('Error sending message to native application:', browser.runtime.lastError.message);
            alert('Failed to connect to the native application. Please ensure it is installed and configured correctly.');
        } else {
            console.log('Selected folder path:', response.path);
            document.getElementById('selectedFolderPath').textContent = 'Selected folder: ' + response.path;
            browser.storage.local.set({downloadPath: response.path});
        }
    });
});

document.getElementById('start-time').addEventListener('input', () => {
    let startTime = document.getElementById('start-time').value;
    console.log('start time saved:', startTime)
    browser.storage.local.set({startTime: startTime});
});

document.getElementById('end-time').addEventListener('input', () => {
    let endTime = document.getElementById('end-time').value;
    console.log('end time saved:', endTime)
    browser.storage.local.set({endTime: endTime});
});

document.querySelectorAll('input[name="format"]').forEach(radio => {
    radio.addEventListener('change', () => {
        const selectedFormat = radio.value;
        const resolutionSelect = document.getElementById('resolution-select');
        let settingsToSave = {downloadFormat: selectedFormat};

        if (selectedFormat === 'mp4') {
            resolutionSelect.disabled = false;
            // Save the resolution setting as well
            settingsToSave.downloadResolution = resolutionSelect.value;
        } else {
            resolutionSelect.disabled = true;
            // Ensure no resolution is saved or it's cleared when MP3 is selected
            settingsToSave.downloadResolution = null;
        }

        browser.storage.local.set(settingsToSave, () => {
            console.log('Settings saved:', settingsToSave);
        });
    });
});

document.querySelectorAll('input[name="filenamePreference"]').forEach(radio => {
    radio.addEventListener('change', () => {
        if(radio.value === 'title'){
            browser.storage.local.set({filenamePreference: true}); 
        }
        else{
            browser.storage.local.set({filenamePreference: false});
        }
        console.log('Filename preference saved:', radio.value);
    });
});

// Additionally, save resolution when it is changed, assuming MP4 is already selected
document.getElementById('resolution-select').addEventListener('change', () => {
    if (!document.getElementById('resolution-select').disabled) {
        const selectedResolution = document.getElementById('resolution-select').value;
        browser.storage.local.set({downloadResolution: selectedResolution}, () => {
            console.log('Resolution saved:', selectedResolution);
        });
    }
});
