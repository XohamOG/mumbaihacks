# 🛡️ Misinformation Detector Browser Extension

A Chrome browser extension that provides quick access to AI-powered misinformation detection through keyboard shortcuts and context menus.

## ✨ Features

- **Hotkey Analysis**: Quickly analyze selected text with `Ctrl+Shift+F`
- **Screenshot Analysis**: Capture and analyze images with `Ctrl+Shift+S`
- **Context Menu Integration**: Right-click to analyze selected content
- **Real-time Status**: Monitor AI service status and usage statistics
- **Customizable Settings**: Configure auto-analysis and display preferences

## 🚀 Installation

### Prerequisites
1. Your AI Detection Service must be running on `http://localhost:8000`
2. Chrome browser (latest version recommended)

### Install Extension

#### Developer Mode (Recommended for Development)
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked"
4. Select the `browser-extension` folder from your project

#### Manual Installation
1. Zip the `browser-extension` folder
2. Rename to `misinformation-detector.zip`
3. Go to `chrome://extensions/`
4. Enable "Developer mode"
5. Click "Load unpacked" and select the unzipped folder

## 📋 Usage

### Keyboard Shortcuts
- `Ctrl+Shift+F` - Analyze selected text on current page
- `Ctrl+Shift+S` - Take screenshot and analyze visible content
- `Alt+Double-click` - Quick analyze word/phrase under cursor

### Context Menu
1. Select any text on a webpage
2. Right-click and choose "Analyze with Misinformation Detector"
3. Results appear in a popup overlay

### Extension Popup
- Click the extension icon in toolbar
- Access quick actions, settings, and service status
- View usage statistics and analysis history

## ⚙️ Settings

Available in the extension popup:

- **Auto-analyze**: Automatically analyze selected text
- **Show Confidence**: Display confidence scores in results
- **Enable Shortcuts**: Enable/disable keyboard shortcuts

## 🔧 Configuration

### API Endpoint
Default: `http://localhost:8000`

To change the API endpoint:
1. Edit `background.js`
2. Update the `API_BASE_URL` constant
3. Reload the extension

### Permissions
The extension requires:
- `activeTab` - Access current tab content
- `contextMenus` - Add context menu items  
- `storage` - Save settings and usage data
- `host permissions` - Communicate with your AI service

## 🐛 Troubleshooting

### Extension Not Working
1. Check if AI service is running on `localhost:8000`
2. Verify extension is enabled in `chrome://extensions/`
3. Check browser console for error messages

### Shortcuts Not Working
1. Go to `chrome://extensions/shortcuts`
2. Verify shortcuts are assigned and not conflicting
3. Toggle "Enable Shortcuts" in extension settings

### Analysis Popup Not Showing
1. Check if text is properly selected
2. Ensure popup blockers aren't interfering
3. Try refreshing the page and analyzing again

## 📊 Service Status

The extension monitors your AI service health:
- **Online**: Service is running and responsive
- **Offline**: Service unavailable or not responding
- **API Calls**: Number of analyses performed today

## 🔒 Privacy & Security

- No data is stored remotely
- All analysis happens through your local AI service
- Settings stored locally in browser storage
- No tracking or analytics

## 🛠️ Development

### File Structure
```
browser-extension/
├── manifest.json          # Extension configuration
├── background.js          # Service worker (background tasks)
├── content.js            # Content script (page interaction)
├── content.css          # Content script styles
├── popup.html           # Extension popup interface
├── popup.js             # Popup functionality
├── popup.css            # Popup styles
└── icons/               # Extension icons (16px, 48px, 128px)
```

### API Integration
The extension communicates with your AI service via REST API:

```javascript
// Analyze text
POST /analyze
{
  "content": "text to analyze",
  "type": "text",
  "source": "browser-extension"
}

// Health check
GET /health
```

### Adding New Features
1. Update `manifest.json` for new permissions
2. Add functionality to `background.js` or `content.js`
3. Update popup UI in `popup.html` and `popup.js`
4. Test and reload extension

## 📈 Version History

### v1.0.0
- Initial release
- Text and screenshot analysis
- Keyboard shortcuts
- Context menu integration
- Settings management
- Service status monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Create an issue in the project repository
- Contact support team

---

**Note**: This extension requires your AI Detection Service to be running locally. Make sure the service is started before using the extension.
