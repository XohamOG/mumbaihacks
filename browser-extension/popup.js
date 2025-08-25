// popup.js - Extension popup functionality
document.addEventListener('DOMContentLoaded', async () => {
  await initializePopup();
});

async function initializePopup() {
  try {
    // Update status indicators
    await updateServiceStatus();
    await loadSettings();
    
    // Set up event listeners
    setupEventListeners();
    
    // Update version info
    const manifest = chrome.runtime.getManifest();
    const versionElement = document.querySelector('.version');
    if (versionElement) {
      versionElement.textContent = `v${manifest.version}`;
    }
    
  } catch (error) {
    console.error('Error initializing popup:', error);
  }
}

function setupEventListeners() {
  // Quick Actions
  document.getElementById('analyze-text')?.addEventListener('click', () => {
    analyzeCurrentTab('text');
  });
  
  document.getElementById('analyze-screenshot')?.addEventListener('click', () => {
    analyzeCurrentTab('screenshot');
  });
  
  document.getElementById('open-dashboard')?.addEventListener('click', () => {
    chrome.tabs.create({ url: 'http://localhost:8000' });
    window.close();
  });
  
  // Settings toggles
  document.getElementById('auto-analyze')?.addEventListener('change', (e) => {
    saveSettings({ autoAnalyze: e.target.checked });
  });
  
  document.getElementById('show-confidence')?.addEventListener('change', (e) => {
    saveSettings({ showConfidence: e.target.checked });
  });
  
  document.getElementById('enable-shortcuts')?.addEventListener('change', (e) => {
    saveSettings({ enableShortcuts: e.target.checked });
  });
  
  // Footer buttons
  document.getElementById('help-btn')?.addEventListener('click', () => {
    chrome.tabs.create({ url: 'https://github.com/yourusername/misinformation-detector/wiki' });
    window.close();
  });
  
  document.getElementById('feedback-btn')?.addEventListener('click', () => {
    chrome.tabs.create({ url: 'mailto:support@misinformation-detector.com' });
    window.close();
  });
  
  // Refresh status button (if exists)
  document.querySelector('.refresh-status')?.addEventListener('click', updateServiceStatus);
}

async function analyzeCurrentTab(type) {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (type === 'text') {
      // Inject content script to get selected text
      const results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: getSelectedText
      });
      
      const selectedText = results[0]?.result;
      if (!selectedText) {
        showMessage('Please select some text on the page first');
        return;
      }
      
      // Send to background script for analysis
      chrome.runtime.sendMessage({
        action: 'analyzeText',
        text: selectedText,
        source: 'popup'
      });
      
      showMessage('Analyzing selected text...', 'info');
      
    } else if (type === 'screenshot') {
      // Send screenshot request to background script
      chrome.runtime.sendMessage({
        action: 'takeScreenshot',
        source: 'popup'
      });
      
      showMessage('Taking screenshot for analysis...', 'info');
    }
    
    // Close popup after action
    setTimeout(() => window.close(), 1000);
    
  } catch (error) {
    console.error('Error analyzing tab:', error);
    showMessage('Error: Could not analyze content', 'error');
  }
}

function getSelectedText() {
  const selection = window.getSelection();
  return selection.toString().trim();
}

async function updateServiceStatus() {
  const statusElements = {
    service: document.getElementById('service-status'),
    lastCheck: document.getElementById('last-check'),
    apiCalls: document.getElementById('api-calls')
  };
  
  try {
    // Check if ADK service is running
    const response = await fetch('http://localhost:8000/health', {
      method: 'GET',
      timeout: 3000
    });
    
    if (response.ok) {
      statusElements.service.textContent = 'Online';
      statusElements.service.className = 'status-value online';
    } else {
      throw new Error('Service unavailable');
    }
    
  } catch (error) {
    statusElements.service.textContent = 'Offline';
    statusElements.service.className = 'status-value offline';
  }
  
  // Update last check time
  statusElements.lastCheck.textContent = new Date().toLocaleTimeString();
  
  // Get API call count from storage
  try {
    const result = await chrome.storage.local.get(['apiCalls']);
    statusElements.apiCalls.textContent = result.apiCalls || '0';
  } catch (error) {
    statusElements.apiCalls.textContent = '0';
  }
}

async function loadSettings() {
  try {
    const settings = await chrome.storage.sync.get([
      'autoAnalyze',
      'showConfidence', 
      'enableShortcuts'
    ]);
    
    // Update checkbox states
    document.getElementById('auto-analyze').checked = settings.autoAnalyze !== false;
    document.getElementById('show-confidence').checked = settings.showConfidence !== false;
    document.getElementById('enable-shortcuts').checked = settings.enableShortcuts !== false;
    
  } catch (error) {
    console.error('Error loading settings:', error);
  }
}

async function saveSettings(updates) {
  try {
    await chrome.storage.sync.set(updates);
    showMessage('Settings saved', 'success');
    
    // Notify background script of setting changes
    chrome.runtime.sendMessage({
      action: 'settingsUpdated',
      settings: updates
    });
    
  } catch (error) {
    console.error('Error saving settings:', error);
    showMessage('Error saving settings', 'error');
  }
}

function showMessage(text, type = 'info') {
  // Create or update message element
  let messageEl = document.querySelector('.popup-message');
  if (!messageEl) {
    messageEl = document.createElement('div');
    messageEl.className = 'popup-message';
    document.querySelector('.popup-container').appendChild(messageEl);
  }
  
  messageEl.textContent = text;
  messageEl.className = `popup-message ${type}`;
  messageEl.style.cssText = `
    position: fixed;
    top: 10px;
    left: 10px;
    right: 10px;
    padding: 12px;
    border-radius: 6px;
    font-size: 13px;
    z-index: 1000;
    text-align: center;
    ${type === 'error' ? 'background: #ffebee; color: #c62828; border: 1px solid #ef5350;' :
      type === 'success' ? 'background: #e8f5e8; color: #2e7d32; border: 1px solid #4caf50;' :
      'background: #e3f2fd; color: #1565c0; border: 1px solid #2196f3;'}
  `;
  
  // Auto-hide message after 3 seconds
  setTimeout(() => {
    if (messageEl) {
      messageEl.remove();
    }
  }, 3000);
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'analysisComplete') {
    showMessage('Analysis complete! Check the results on the page.', 'success');
  } else if (message.action === 'analysisError') {
    showMessage(`Analysis failed: ${message.error}`, 'error');
  }
});

// Keyboard shortcuts in popup
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    window.close();
  } else if (e.key === 'Enter' && e.ctrlKey) {
    analyzeCurrentTab('text');
  }
});

// Auto-refresh status every 30 seconds
setInterval(updateServiceStatus, 30000);
