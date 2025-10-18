# Pi GameUI - Retro Gaming Launcher

A fullscreen gaming launcher designed for Raspberry Pi with 320×240 display, featuring a retro terminal theme and comprehensive input support.

![Pi GameUI](https://img.shields.io/badge/Platform-Raspberry%20Pi-red) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.5+-green)

## 🎮 Features

- **🎯 Splash Screen** - Animated startup with gamepad logo and fade effects
- **📱 Grid Menu** - 2×3 layout with pixel art icons for games and apps
- **🖥️ Taskbar** - Bottom taskbar with power button, digital clock, and settings
- **⚙️ Settings Menu** - Centered context menu (Shutdown, Reboot, Sleep)
- **🕹️ Multi-Input** - Keyboard, gamepad, and touchscreen support
- **🖥️ Retro Shell** - Themed terminal with full bash access
- **🎨 Visual Polish** - Animations, shadows, gradients, and retro styling

## 🚀 Quick Start

### Prerequisites
- Raspberry Pi (any model)
- 320×240 display (or compatible resolution)
- Python 3.8+ installed
- Git installed

### Installation via GitHub

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/raspbian_ui.git
   cd raspbian_ui
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Test the launcher:**
   ```bash
   python3 main.py
   ```

4. **Enable auto-start (optional):**
   ```bash
   sudo systemctl start gameui
   sudo systemctl enable gameui
   ```

## 📋 Manual Installation

If you prefer to install manually:

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x main.py apps/shell_ui.py
   ```

3. **Install systemd service:**
   ```bash
   sudo cp service/gameui.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable gameui
   ```

## 🎮 Controls

### Keyboard
- **Arrow Keys** - Navigate menu
- **Enter/Space** - Select item
- **F1** - Open settings menu
- **Escape** - Exit/Close menu

### Gamepad
- **D-Pad/Analog Stick** - Navigate menu
- **A Button** - Select item
- **B Button** - Exit/Close menu

### Touchscreen
- **Tap** - Select and launch items
- **Tap Settings** - Open context menu

## ⚙️ Configuration

### Adding Games/Apps

Edit `config.json` to add your games and applications:

```json
[
    {"label": "Retro Games", "command": "retroarch"},
    {"label": "Pac-Man", "command": "mame pacman"},
    {"label": "Tetris", "command": "python3 games/tetris.py"},
    {"label": "Shell", "command": "python3 apps/shell_ui.py"},
    {"label": "Shutdown", "command": "sudo shutdown now"}
]
```

### Customizing Appearance

- **Background Color**: Edit the color values in `main.py` (line 128)
- **Font**: Replace `assets/font.ttf` with your preferred font
- **Icons**: Modify the pixel art icons in the `show_main_menu()` function

## 🖥️ Shell App

The included shell app (`apps/shell_ui.py`) provides a retro-themed terminal:

- **Green-on-black** terminal theme
- **Full bash access** with command execution
- **Interactive features** - cursor navigation, command history
- **Ctrl+C support** for interrupting commands
- **Scrollable output** with status bar

### Shell Controls
- **Arrow Keys** - Navigate command line
- **Home/End** - Jump to beginning/end of line
- **Ctrl+C** - Interrupt current command
- **Escape** - Exit shell

## 🔧 Troubleshooting

### Common Issues

**Launcher won't start:**
```bash
# Check Python and pygame installation
python3 -c "import pygame; print('Pygame version:', pygame.version.ver)"

# Check display permissions
sudo usermod -a -G video pi
```

**Touchscreen not working:**
```bash
# Check touchscreen calibration
sudo apt-get install xinput-calibrator
xinput_calibrator
```

**Service won't start:**
```bash
# Check service status
sudo systemctl status gameui

# View logs
journalctl -u gameui -f
```

**Display issues:**
```bash
# Check display resolution
xrandr

# Force 320x240 resolution
xrandr --output HDMI-1 --mode 320x240
```

### Debug Mode

Run with debug output:
```bash
python3 -c "
import sys
sys.path.append('.')
from main import GameUI
game_ui = GameUI()
game_ui.run()
"
```

## 📁 Project Structure

```
raspbian_ui/
├── main.py                  # Main launcher application
├── apps/
│   └── shell_ui.py         # Retro terminal shell
├── assets/
│   ├── font.ttf            # Custom font file
│   └── bg.png              # Background image
├── service/
│   └── gameui.service      # Systemd service file
├── config.json             # Game/app configuration
├── requirements.txt        # Python dependencies
├── setup.sh               # Installation script
└── README.md              # This file
```

## 🛠️ Development

### Running Tests

```bash
# Test basic functionality
python3 -c "import pygame; print('Pygame OK')"

# Test shell app
python3 apps/shell_ui.py

# Test main launcher
python3 main.py
```

### Adding New Features

1. **New Input Methods**: Add handlers in `handle_events()`
2. **New Menu Items**: Modify `config.json` and icon drawing code
3. **New Apps**: Create in `apps/` directory and add to config
4. **Visual Themes**: Modify colors and styling in drawing functions

## 📝 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with:
   - Raspberry Pi model and OS version
   - Python version (`python3 --version`)
   - Error messages or logs
   - Steps to reproduce the issue

## 🎯 Roadmap

- [ ] Sound effects and music
- [ ] Multiple theme support
- [ ] Game save state management
- [ ] Network game discovery
- [ ] Plugin system for custom apps
- [ ] Web-based configuration interface

---

**Happy Gaming! 🎮✨**

*Built with ❤️ for the Raspberry Pi community*
