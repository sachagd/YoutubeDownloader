document.querySelectorAll('input[name="format"]').forEach(radio => {
    radio.addEventListener('change', () => {
        const format = radio.value;
        const resolution = document.getElementById('resolution');
        const settings = {format};
        if (format === 'mp4') {
            resolution.disabled = false;
            settings.resolution = resolution.value;
            document.getElementById('itunes-sync').checked = false;
            settings.iTunesSync = false
        } else {
            resolution.disabled = true;
            settings.resolution = null;
        }
        browser.storage.local.set(settings);
    });
});

document.getElementById('resolution').addEventListener('change', () => {
    const resolution = document.getElementById('resolution').value;
    browser.storage.local.set({resolution});
});

document.getElementById('timestamps').addEventListener('input', () => {
    const input = document.getElementById('timestamps').value.trim();
    const lines = input.split('\n').filter(Boolean);
    const timestamps = lines.map(line => {
        const [startTime, endTime] = line.split('-').map(str => str.trim());
        return { startTime, endTime };
    });
    browser.storage.local.set({timestamps});
});

document.querySelectorAll('input[name="filename-preference"]').forEach(radio => {
    radio.addEventListener('change', () => {
        if(radio.value === 'title'){
            browser.storage.local.set({filenamePreference: true}); 
        }
        else{
            browser.storage.local.set({filenamePreference: false});
        }
    });
});

document.getElementById('standard-path-button').addEventListener('click', () => {
    browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', {action: 'select_folder'}, response => {
        if (browser.runtime.lastError) {
            alert('Failed to connect to the native application. Please ensure it is installed and configured correctly.');
        } else {
            if (response.path !== ""){
                document.getElementById('standard-path-text').textContent = 'Selected folder: ' + response.path;
                browser.storage.local.set({standardPath: response.path});
            }
        }
    });
});

document.getElementById('itunes-sync').addEventListener('change', () => {
    const isChecked = document.getElementById('itunes-sync').checked;
    const settings = {iTunesSync: isChecked}
    if (isChecked) {
        document.getElementById('format-mp3').checked = true;
        settings.format = 'mp3'
        document.getElementById('resolution').disabled = true;
    }
    browser.storage.local.set(settings);
}); 

document.getElementById('itunes-path-button').addEventListener('click', () => {
    browser.runtime.sendNativeMessage('com.sacha.youtubedownloader', {action: 'select_folder'}, response => {
        if (browser.runtime.lastError) {
            alert('Failed to connect to the native application. Please ensure it is installed and configured correctly.');
        } else {
            if (response.path !== ""){
            document.getElementById('itunes-path-text').textContent = 'Selected folder: ' + response.path;
            browser.storage.local.set({iTunesPath: response.path});
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', async () => {
    const settings = await browser.storage.local.get();

    if (settings.format) {
        document.getElementById(`format-${settings.format}`).checked = true;
        const resolution = document.getElementById('resolution');
        resolution.disabled = settings.format !== 'mp4';
    }

    if (settings.resolution) {
        document.getElementById('resolution').value = settings.resolution;
    }

    if (Array.isArray(settings.timestamps)) {
        const text = settings.timestamps.map(t => `${t.startTime} - ${t.endTime}`).join('\n');
        document.getElementById('timestamps').value = text;
    }

    if (settings.filenamePreference === false) {
        document.getElementById('filename-output').checked = true;
    } else {
        document.getElementById('filename-title').checked = true;
    }

    if (settings.standardPath) {
        document.getElementById('standard-path-text').textContent = 'Selected folder: ' + settings.standardPath;
    }

    if (settings.iTunesSync) {
        document.getElementById('itunes-sync').checked = true;
        document.getElementById('format-mp3').checked = true;
        document.getElementById('resolution').disabled = true;
    }

    if (settings.iTunesPath) {
        document.getElementById('itunes-path-text').textContent = 'Selected folder: ' + settings.iTunesPath;
    }
});
