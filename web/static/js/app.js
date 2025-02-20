// DOM Elements
const urlInput = document.getElementById('urlInput');
const pasteButton = document.getElementById('pasteButton');
const clearButton = document.getElementById('clearButton');
const downloadButton = document.getElementById('downloadButton');
const downloadsList = document.getElementById('downloadsList');
const themeSelect = document.getElementById('themeSelect');
const statusToast = document.getElementById('statusToast');
const statusMessage = document.getElementById('statusMessage');

// State
let activeDownloads = new Set();
let isDownloading = false;

// Theme Management
function setTheme(theme) {
    if (theme === 'system') {
        const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
    } else {
        document.body.setAttribute('data-theme', theme);
    }
    localStorage.setItem('theme', theme);
}

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'system';
themeSelect.value = savedTheme;
setTheme(savedTheme);

// Toast Management
function showToast(message, duration = 3000) {
    statusMessage.textContent = message;
    statusToast.classList.remove('hidden');
    setTimeout(() => {
        statusToast.classList.add('hidden');
    }, duration);
}

// Download Item Template
function createDownloadItem(download) {
    const item = document.createElement('div');
    item.className = 'download-item';
    item.id = `download-${download.id}`;
    
    const statusClass = {
        'completed': 'completed',
        'failed': 'failed',
        'downloading': 'downloading',
        'starting': 'downloading'
    }[download.status];

    item.innerHTML = `
        <div class="download-info">
            <div class="download-url">${download.url}</div>
            ${download.error ? `<div class="error-message">${download.error}</div>` : ''}
        </div>
        <div class="status ${statusClass}">${download.status}</div>
        ${download.status === 'downloading' ? `
            <div class="progress-bar">
                <div class="fill" style="width: ${download.progress}%"></div>
            </div>
        ` : ''}
    `;
    
    return item;
}

// API Calls
async function startDownload(urls) {
    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ urls })
        });
        
        const data = await response.json();
        if (response.ok) {
            data.download_ids.forEach(id => activeDownloads.add(id));
            showToast('✓ Downloads started');
            return data.download_ids;
        } else {
            throw new Error(data.error || 'Failed to start download');
        }
    } catch (error) {
        showToast(`❌ ${error.message}`);
        return [];
    }
}

async function checkDownloadStatus(downloadId) {
    try {
        const response = await fetch(`/api/status/${downloadId}`);
        const data = await response.json();
        
        if (response.ok) {
            const downloadItem = document.getElementById(`download-${downloadId}`);
            if (downloadItem) {
                const newItem = createDownloadItem(data);
                downloadItem.replaceWith(newItem);
            } else {
                downloadsList.prepend(createDownloadItem(data));
            }
            
            if (data.status === 'completed' || data.status === 'failed') {
                activeDownloads.delete(downloadId);
            }
        } else {
            activeDownloads.delete(downloadId);
        }
    } catch (error) {
        console.error('Error checking download status:', error);
    }
}

async function updateDownloads() {
    if (activeDownloads.size > 0) {
        for (const downloadId of activeDownloads) {
            await checkDownloadStatus(downloadId);
        }
        setTimeout(updateDownloads, 1000);
    } else {
        isDownloading = false;
        downloadButton.textContent = 'Start Download';
    }
}

// Event Listeners
pasteButton.addEventListener('click', async () => {
    try {
        const text = await navigator.clipboard.readText();
        if (text) {
            const currentText = urlInput.value;
            urlInput.value = currentText ? `${currentText}\n${text}` : text;
            showToast('✓ URLs pasted from clipboard');
        }
    } catch (error) {
        showToast('❌ Failed to read clipboard');
    }
});

clearButton.addEventListener('click', () => {
    urlInput.value = '';
    showToast('✓ URLs cleared');
});

downloadButton.addEventListener('click', async () => {
    if (isDownloading) {
        isDownloading = false;
        downloadButton.textContent = 'Start Download';
        showToast('⏹ Downloads cancelled');
        return;
    }

    const urls = urlInput.value
        .split('\n')
        .map(url => url.trim())
        .filter(url => url && !url.startsWith('#'));

    if (urls.length === 0) {
        showToast('⚠ No URLs to download');
        return;
    }

    isDownloading = true;
    downloadButton.textContent = 'Stop Download';
    const downloadIds = await startDownload(urls);
    
    if (downloadIds.length > 0) {
        updateDownloads();
    }
});

themeSelect.addEventListener('change', (e) => {
    setTheme(e.target.value);
});

// Watch for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (themeSelect.value === 'system') {
        setTheme('system');
    }
}); 