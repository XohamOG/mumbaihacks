// Background script for handling hotkeys and API communication

const API_BASE_URL = 'http://127.0.0.1:8000';

// Handle keyboard shortcuts
chrome.commands.onCommand.addListener((command, tab) => {
  console.log('Command received:', command);
  
  if (command === 'analyze-selection') {
    // Trigger text analysis
    chrome.tabs.sendMessage(tab.id, {
      action: 'analyzeSelection'
    });
  } else if (command === 'capture-and-analyze') {
    // Trigger screenshot analysis
    captureAndAnalyze(tab);
  }
});

// Handle context menu clicks
chrome.runtime.onInstalled.addListener(() => {
  // Create context menu items
  chrome.contextMenus.create({
    id: 'analyze-text',
    title: 'Analyze for misinformation',
    contexts: ['selection']
  });
  
  chrome.contextMenus.create({
    id: 'analyze-link',
    title: 'Analyze link content',
    contexts: ['link']
  });
  
  chrome.contextMenus.create({
    id: 'analyze-image',
    title: 'Analyze image',
    contexts: ['image']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  switch (info.menuItemId) {
    case 'analyze-text':
      analyzeText(info.selectionText, tab);
      break;
    case 'analyze-link':
      analyzeUrl(info.linkUrl, tab);
      break;
    case 'analyze-image':
      analyzeImage(info.srcUrl, tab);
      break;
  }
});

// Handle messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Message received:', message);
  
  switch (message.action) {
    case 'analyzeText':
      analyzeText(message.text, sender.tab)
        .then(result => sendResponse({success: true, data: result}))
        .catch(error => sendResponse({success: false, error: error.message}));
      return true; // Keep message channel open for async response
      
    case 'analyzeImage':
      analyzeImage(message.imageUrl, sender.tab)
        .then(result => sendResponse({success: true, data: result}))
        .catch(error => sendResponse({success: false, error: error.message}));
      return true;
      
    case 'showNotification':
      showNotification(message.title, message.message, message.type);
      break;
  }
});

// Analyze text content
async function analyzeText(text, tab) {
  if (!text || text.trim().length === 0) {
    throw new Error('No text selected');
  }
  
  try {
    console.log('Analyzing text:', text.substring(0, 100) + '...');
    
    const response = await fetch(`${API_BASE_URL}/apps/root_orchestrator/users/user/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    });
    
    if (!response.ok) {
      throw new Error('Failed to create session');
    }
    
    const sessionData = await response.json();
    const sessionId = sessionData.session_id;
    
    // Send analysis request
    const analysisResponse = await fetch(`${API_BASE_URL}/run_sse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        app_name: 'root_orchestrator',
        session_id: sessionId,
        message: `Please analyze this content for misinformation: "${text}"`
      })
    });
    
    if (!analysisResponse.ok) {
      throw new Error('Analysis request failed');
    }
    
    // For now, return a simplified response
    // In production, you'd parse the SSE stream
    return {
      text: text.substring(0, 200) + (text.length > 200 ? '...' : ''),
      status: 'analyzed',
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    console.error('Error analyzing text:', error);
    throw error;
  }
}

// Analyze image
async function analyzeImage(imageUrl, tab) {
  try {
    console.log('Analyzing image:', imageUrl);
    
    // For now, return a placeholder response
    // In production, you'd send the image to your AI system
    return {
      imageUrl: imageUrl,
      status: 'analyzed',
      message: 'Image analysis not yet implemented',
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    console.error('Error analyzing image:', error);
    throw error;
  }
}

// Analyze URL content
async function analyzeUrl(url, tab) {
  try {
    console.log('Analyzing URL:', url);
    
    // For now, return a placeholder response
    return {
      url: url,
      status: 'analyzed', 
      message: 'URL analysis not yet implemented',
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    console.error('Error analyzing URL:', error);
    throw error;
  }
}

// Capture screenshot and analyze
async function captureAndAnalyze(tab) {
  try {
    const screenshot = await chrome.tabs.captureVisibleTab(tab.windowId, {
      format: 'png',
      quality: 80
    });
    
    // Send to content script to show analysis UI
    chrome.tabs.sendMessage(tab.id, {
      action: 'showScreenshotAnalysis',
      screenshot: screenshot
    });
    
  } catch (error) {
    console.error('Error capturing screenshot:', error);
    showNotification('Error', 'Failed to capture screenshot', 'error');
  }
}

// Show browser notification
function showNotification(title, message, type = 'info') {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon48.png',
    title: title,
    message: message
  });
}
