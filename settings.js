document.querySelectorAll('input[name="format"]').forEach(radio => {
    radio.addEventListener('change', () => {
        const selectedFormat = radio.value;
        const resolutionSelect = document.getElementById('resolution-select');
        const settingsToSave = {downloadFormat: selectedFormat};

        if (selectedFormat === 'mp4') {
            resolutionSelect.disabled = false;
            document.getElementById('iTunesSync').checked = false;
            settingsToSave.downloadResolution = resolutionSelect.value;
        } else {
            resolutionSelect.disabled = true;
            settingsToSave.downloadResolution = null;
        }

        browser.storage.local.set(settingsToSave);
    });
});

document.getElementById('resolution-select').addEventListener('change', () => {
    const selectedResolution = document.getElementById('resolution-select').value;
    browser.storage.local.set({downloadResolution: selectedResolution});
});

document.getElementById('start-time').addEventListener('input', () => {
    const startTime = document.getElementById('start-time').value;
    browser.storage.local.set({startTime: startTime});
});

document.getElementById('end-time').addEventListener('input', () => {
    const endTime = document.getElementById('end-time').value;
    browser.storage.local.set({endTime: endTime});
});

document.querySelectorAll('input[name="filenamePreference"]').forEach(radio => {
    radio.addEventListener('change', () => {
        if(radio.value === 'title'){
            browser.storage.local.set({filenamePreference: true}); 
        }
        else{
            browser.storage.local.set({filenamePreference: false});
        }
    });
});

document.getElementById('selectFolderButtonStandard').addEventListener('click', () => {
    browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', {action: 'select_folder'}, response => {
        if (browser.runtime.lastError) {
            alert('Failed to connect to the native application. Please ensure it is installed and configured correctly.');
        } else {
            document.getElementById('selectedFolderPathStandard').textContent = 'Selected folder: ' + response.path;
            browser.storage.local.set({downloadPathStandard: response.path});
        }
    });
});

document.getElementById('iTunesSync').addEventListener('change', () => {
    const isChecked = document.getElementById('iTunesSync').checked;
    browser.storage.local.set({ iTunesSync: isChecked });
    if (isChecked) {
        document.getElementById('format-mp3').checked = true;
        document.getElementById('resolution-select').disabled = true;
    }
});

document.getElementById('selectFolderButtoniTunesSync').addEventListener('click', () => {
    browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', {action: 'select_folder'}, response => {
        if (browser.runtime.lastError) {
            alert('Failed to connect to the native application. Please ensure it is installed and configured correctly.');
        } else {
            document.getElementById('selectedFolderPathiTunesSync').textContent = 'Selected folder: ' + response.path;
            browser.storage.local.set({downloadPathiTunesSync: response.path});
        }
    });
});