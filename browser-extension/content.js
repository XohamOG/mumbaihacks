// Content script for handling user interactions and UI

let analysisPopup = null;
let isAnalyzing = false;

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Content script received message:', message);
  
  switch (message.action) {
    case 'analyzeSelection':
      handleSelectionAnalysis();
      break;
    case 'showScreenshotAnalysis':
      showScreenshotAnalysis(message.screenshot);
      break;
  }
});

// Handle text selection analysis
function handleSelectionAnalysis() {
  const selectedText = window.getSelection().toString().trim();
  
  if (!selectedText) {
    showNotification('No text selected', 'Please select some text to analyze', 'warning');
    return;
  }
  
  if (selectedText.length < 10) {
    showNotification('Text too short', 'Please select at least 10 characters for meaningful analysis', 'warning');
    return;
  }
  
  analyzeSelectedText(selectedText);
}

// Analyze the selected text
async function analyzeSelectedText(text) {
  if (isAnalyzing) {
    return;
  }
  
  isAnalyzing = true;
  showAnalysisPopup('Analyzing...', text);
  
  try {
    const response = await new Promise((resolve, reject) => {
      chrome.runtime.sendMessage({
        action: 'analyzeText',
        text: text
      }, (response) => {
        if (response.success) {
          resolve(response.data);
        } else {
          reject(new Error(response.error));
        }
      });
    });
    
    showAnalysisResults(response, text);
    
  } catch (error) {
    console.error('Analysis failed:', error);
    showAnalysisPopup('Analysis Failed', `Error: ${error.message}`, 'error');
  } finally {
    isAnalyzing = false;
  }
}

// Show analysis popup
function showAnalysisPopup(title, content, type = 'info') {
  removeExistingPopup();
  
  const popup = document.createElement('div');
  popup.id = 'misinformation-detector-popup';
  popup.className = `md-popup md-popup-${type}`;
  
  popup.innerHTML = `
    <div class="md-popup-header">
      <h3 class="md-popup-title">${title}</h3>
      <button class="md-popup-close" onclick="this.parentElement.parentElement.remove()">×</button>
    </div>
    <div class="md-popup-content">
      <p class="md-popup-text">${content}</p>
      ${type === 'info' ? '<div class="md-popup-loading">🔍 Analyzing...</div>' : ''}
    </div>
  `;
  
  document.body.appendChild(popup);
  analysisPopup = popup;
  
  // Auto-remove after 10 seconds for non-result popups
  if (type !== 'result') {
    setTimeout(() => {
      if (popup.parentElement) {
        popup.remove();
      }
    }, 10000);
  }
}

// Show analysis results
function showAnalysisResults(results, originalText) {
  removeExistingPopup();
  
  const popup = document.createElement('div');
  popup.id = 'misinformation-detector-popup';
  popup.className = 'md-popup md-popup-result';
  
  const truncatedText = originalText.length > 100 ? 
    originalText.substring(0, 100) + '...' : originalText;
  
  popup.innerHTML = `
    <div class="md-popup-header">
      <h3 class="md-popup-title">📊 Analysis Results</h3>
      <button class="md-popup-close" onclick="this.parentElement.parentElement.remove()">×</button>
    </div>
    <div class="md-popup-content">
      <div class="md-popup-section">
        <h4>Analyzed Text:</h4>
        <p class="md-analyzed-text">"${truncatedText}"</p>
      </div>
      
      <div class="md-popup-section">
        <h4>Status:</h4>
        <p class="md-status ${results.status}">${results.status.toUpperCase()}</p>
      </div>
      
      <div class="md-popup-section">
        <h4>Analysis Time:</h4>
        <p class="md-timestamp">${new Date(results.timestamp).toLocaleString()}</p>
      </div>
      
      <div class="md-popup-actions">
        <button class="md-btn md-btn-primary" onclick="window.open('http://127.0.0.1:8000', '_blank')">
          View Full Report
        </button>
        <button class="md-btn md-btn-secondary" onclick="this.closest('.md-popup').remove()">
          Close
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(popup);
  analysisPopup = popup;
}

// Show screenshot analysis UI
function showScreenshotAnalysis(screenshot) {
  removeExistingPopup();
  
  const popup = document.createElement('div');
  popup.id = 'misinformation-detector-popup';
  popup.className = 'md-popup md-popup-screenshot';
  
  popup.innerHTML = `
    <div class="md-popup-header">
      <h3 class="md-popup-title">📸 Screenshot Analysis</h3>
      <button class="md-popup-close" onclick="this.parentElement.parentElement.remove()">×</button>
    </div>
    <div class="md-popup-content">
      <div class="md-popup-section">
        <h4>Captured Screenshot:</h4>
        <img src="${screenshot}" alt="Screenshot" class="md-screenshot-preview">
      </div>
      
      <div class="md-popup-section">
        <p>Screenshot captured successfully!</p>
        <p><em>Image analysis feature coming soon...</em></p>
      </div>
      
      <div class="md-popup-actions">
        <button class="md-btn md-btn-primary" onclick="downloadScreenshot('${screenshot}')">
          Download Screenshot
        </button>
        <button class="md-btn md-btn-secondary" onclick="this.closest('.md-popup').remove()">
          Close
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(popup);
  analysisPopup = popup;
}

// Remove existing popup
function removeExistingPopup() {
  if (analysisPopup && analysisPopup.parentElement) {
    analysisPopup.remove();
    analysisPopup = null;
  }
}

// Download screenshot
function downloadScreenshot(dataUrl) {
  const link = document.createElement('a');
  link.download = `misinformation-check-${Date.now()}.png`;
  link.href = dataUrl;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Show notification
function showNotification(title, message, type = 'info') {
  chrome.runtime.sendMessage({
    action: 'showNotification',
    title: title,
    message: message,
    type: type
  });
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Ctrl+Shift+F (or Cmd+Shift+F on Mac)
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'F') {
    e.preventDefault();
    handleSelectionAnalysis();
  }
  
  // Escape to close popup
  if (e.key === 'Escape' && analysisPopup) {
    removeExistingPopup();
  }
});

// Add double-click analysis (optional feature)
document.addEventListener('dblclick', (e) => {
  // Only trigger if Alt key is held during double-click
  if (e.altKey) {
    e.preventDefault();
    setTimeout(() => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText && selectedText.length >= 10) {
        analyzeSelectedText(selectedText);
      }
    }, 10);
  }
});

console.log('🔍 Misinformation Detector extension loaded');
