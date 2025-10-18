#!/bin/bash

# Pi GameUI Setup Script
# This script helps set up the GameUI launcher on a Raspberry Pi

set -e

echo "🎮 Pi GameUI Setup Script"
echo "========================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please do not run this script as root. Run as pi user instead."
    exit 1
fi

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="gameui.service"
SERVICE_FILE="$SCRIPT_DIR/service/$SERVICE_NAME"

echo "📁 Working directory: $SCRIPT_DIR"

# Check if we're on a Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi system."
    echo "   The setup will continue, but some features may not work correctly."
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make main script executable
echo "🔧 Making scripts executable..."
chmod +x "$SCRIPT_DIR/main.py"

# Install systemd service
echo "⚙️  Installing systemd service..."
if [ -f "$SERVICE_FILE" ]; then
    sudo cp "$SERVICE_FILE" /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    echo "✅ Service installed and enabled"
else
    echo "❌ Service file not found: $SERVICE_FILE"
    exit 1
fi

# Create desktop entry for easy testing
echo "🖥️  Creating desktop entry..."
DESKTOP_FILE="/home/pi/Desktop/Pi GameUI.desktop"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Pi GameUI
Comment=Retro Gaming Launcher
Exec=python3 $SCRIPT_DIR/main.py
Icon=applications-games
Terminal=false
Categories=Game;
EOF
chmod +x "$DESKTOP_FILE"

# Set up permissions
echo "🔐 Setting up permissions..."
chmod 755 "$SCRIPT_DIR"
chmod 644 "$SCRIPT_DIR"/*.py
chmod 644 "$SCRIPT_DIR"/*.json
chmod 644 "$SCRIPT_DIR"/*.txt

# Create a simple test script
echo "🧪 Creating test script..."
cat > "$SCRIPT_DIR/test_launcher.py" << 'EOF'
#!/usr/bin/env python3
"""
Test script for Pi GameUI
This script can be used to test the launcher without the full systemd service
"""

import subprocess
import sys
import os

def main():
    print("🎮 Testing Pi GameUI Launcher...")
    
    # Check if pygame is available
    try:
        import pygame
        print("✅ Pygame is available")
    except ImportError:
        print("❌ Pygame not found. Please install requirements:")
        print("   pip3 install -r requirements.txt")
        return 1
    
    # Check if assets exist
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    if os.path.exists(assets_dir):
        print("✅ Assets directory found")
    else:
        print("⚠️  Assets directory not found. Creating placeholder...")
        os.makedirs(assets_dir, exist_ok=True)
    
    # Check if config exists
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_file):
        print("✅ Config file found")
    else:
        print("❌ Config file not found. Please create config.json")
        return 1
    
    # Try to run the launcher
    print("🚀 Starting launcher...")
    try:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'main.py')])
    except KeyboardInterrupt:
        print("\n⏹️  Launcher stopped by user")
    except Exception as e:
        print(f"❌ Error running launcher: {e}")
        return 1
    
    print("✅ Test completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x "$SCRIPT_DIR/test_launcher.py"

# Create README
echo "📝 Creating README..."
cat > "$SCRIPT_DIR/README.md" << 'EOF'
# Pi GameUI - Retro Gaming Launcher

A fullscreen gaming launcher designed for Raspberry Pi with 320×240 display.

## Features

- 🎮 **Splash Screen**: Animated startup with gamepad logo
- 🎯 **Grid Menu**: 2×4 grid layout for games and apps
- 🕹️ **Multi-Input Support**: Keyboard, gamepad, and touchscreen
- 🎨 **Pixel Art Style**: Retro-themed icons and animations
- ⚡ **Smooth Animations**: Pulsing selections and visual effects
- 🔄 **Auto-Return**: Returns to launcher after app closes

## Controls

### Keyboard
- **Arrow Keys**: Navigate menu
- **Enter/Space**: Launch selected app
- **Escape**: Exit launcher

### Gamepad
- **D-Pad/Analog Stick**: Navigate menu
- **A Button**: Launch selected app
- **B Button**: Exit launcher

### Touchscreen
- **Tap**: Select and launch app

## Installation

1. Run the setup script:
   ```bash
   ./setup.sh
   ```

2. Test the launcher:
   ```bash
   python3 test_launcher.py
   ```

3. Start the service:
   ```bash
   sudo systemctl start gameui
   ```

4. Enable auto-start on boot:
   ```bash
   sudo systemctl enable gameui
   ```

## Configuration

Edit `config.json` to add your games and apps:

```json
[
    {"label": "Game Name", "command": "command_to_launch_game"},
    {"label": "Another Game", "command": "another_command"},
    {"label": "Shutdown", "command": "sudo shutdown now"}
]
```

## Assets

Place your custom assets in the `assets/` directory:
- `bg.png`: Background image (320×240)
- `font.ttf`: Custom font file

## Troubleshooting

- Check service status: `sudo systemctl status gameui`
- View logs: `journalctl -u gameui -f`
- Test manually: `python3 test_launcher.py`

## Development

The launcher is built with Python and Pygame, designed for embedded systems and retro gaming setups.
EOF

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Test the launcher: python3 test_launcher.py"
echo "   2. Start the service: sudo systemctl start gameui"
echo "   3. Enable auto-start: sudo systemctl enable gameui"
echo ""
echo "📖 For more information, see README.md"
echo ""
echo "🎮 Happy gaming!"
