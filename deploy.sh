#!/bin/bash

# Pi GameUI Deployment Script
# This script downloads and sets up Pi GameUI on a Raspberry Pi

set -e

echo "🎮 Pi GameUI Deployment Script"
echo "=============================="

# Configuration
REPO_URL="https://github.com/YOUR_USERNAME/raspbian_ui.git"
INSTALL_DIR="/home/pi/gameui"
SERVICE_USER="pi"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please do not run this script as root. Run as pi user instead."
    exit 1
fi

# Check if we're on a Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    print_warning "This doesn't appear to be a Raspberry Pi system."
    print_warning "The setup will continue, but some features may not work correctly."
fi

# Update system packages
print_status "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
print_status "Installing system dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv git
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
sudo apt-get install -y xvfb  # For headless testing

# Install Python dependencies
print_status "Installing Python dependencies..."
pip3 install --user pygame Pillow numpy

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    print_status "Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    print_status "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Make scripts executable
print_status "Setting up permissions..."
chmod +x main.py apps/shell_ui.py setup.sh

# Run the setup script
print_status "Running setup script..."
./setup.sh

# Configure display (if needed)
print_status "Configuring display..."
if ! grep -q "DISPLAY=:0" ~/.bashrc; then
    echo "export DISPLAY=:0" >> ~/.bashrc
fi

# Set up autostart (optional)
read -p "Enable auto-start on boot? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Enabling auto-start..."
    sudo systemctl enable gameui
    print_success "Auto-start enabled. The launcher will start automatically on boot."
else
    print_warning "Auto-start not enabled. You can enable it later with: sudo systemctl enable gameui"
fi

# Test the installation
print_status "Testing installation..."
if python3 -c "import pygame; print('Pygame OK')" 2>/dev/null; then
    print_success "Pygame installation verified"
else
    print_error "Pygame installation failed"
    exit 1
fi

# Create desktop shortcut
print_status "Creating desktop shortcut..."
cat > ~/Desktop/Pi\ GameUI.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Pi GameUI
Comment=Retro Gaming Launcher
Exec=python3 $INSTALL_DIR/main.py
Icon=applications-games
Terminal=false
Categories=Game;
EOF
chmod +x ~/Desktop/Pi\ GameUI.desktop

# Final instructions
print_success "Installation completed successfully!"
echo
echo "🎮 Next steps:"
echo "1. Test the launcher: python3 $INSTALL_DIR/main.py"
echo "2. Start the service: sudo systemctl start gameui"
echo "3. Check service status: sudo systemctl status gameui"
echo "4. View logs: journalctl -u gameui -f"
echo
echo "📁 Installation directory: $INSTALL_DIR"
echo "🖥️ Desktop shortcut created"
echo "⚙️ Configuration file: $INSTALL_DIR/config.json"
echo
echo "🎯 To customize games and apps, edit: $INSTALL_DIR/config.json"
echo
print_success "Happy gaming! 🎮✨"
