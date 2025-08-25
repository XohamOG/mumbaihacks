# Extension Icons

Since we cannot create actual image files through this interface, here are the instructions to create the required icons:

## Required Icon Sizes:
- 16x16px (toolbar icon)
- 48x48px (extension management page)  
- 128x128px (Chrome Web Store)

## Icon Design Guidelines:
1. **Theme**: Shield with checkmark or magnifying glass
2. **Colors**: Blue (#2196F3) and white/gray
3. **Style**: Modern, minimal, recognizable at small sizes

## Quick Icon Creation Options:

### Option 1: Use Online Icon Generator
1. Go to https://favicon.io/favicon-generator/
2. Use text "MD" (Misinformation Detector)
3. Background: #2196F3 (blue)
4. Text Color: white
5. Download and rename to icon-16.png, icon-48.png, icon-128.png

### Option 2: Create Simple Icons
Create solid blue squares with white text "MD" in the center for each size.

### Option 3: Use Built-in Browser Icons (Temporary)
For development, you can temporarily remove the "icons" section from manifest.json and Chrome will use default icons.

## File Locations:
- browser-extension/icons/icon-16.png
- browser-extension/icons/icon-48.png  
- browser-extension/icons/icon-128.png
