# GitHub Setup Guide

This guide will help you set up a GitHub repository for your Pi GameUI project and deploy it to your Raspberry Pi.

## 🚀 Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in to your account
2. **Click "New repository"** (green button)
3. **Repository settings:**
   - **Name**: `raspbian_ui` (or your preferred name)
   - **Description**: `Retro Gaming Launcher for Raspberry Pi`
   - **Visibility**: Public (recommended) or Private
   - **Initialize**: ✅ Add a README file
   - **Add .gitignore**: ✅ Python
   - **Choose a license**: MIT (recommended)

4. **Click "Create repository"**

## 📤 Step 2: Upload Your Code

### Option A: Using GitHub Desktop (Easiest)
1. Download and install [GitHub Desktop](https://desktop.github.com/)
2. Clone your new repository
3. Copy all files from your local `raspbian_ui` folder to the cloned repository folder
4. Commit and push your changes

### Option B: Using Command Line
```bash
# Navigate to your project directory
cd /path/to/your/raspbian_ui

# Initialize git repository
git init

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/raspbian_ui.git

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: Pi GameUI launcher"

# Push to GitHub
git push -u origin main
```

### Option C: Using GitHub Web Interface
1. Go to your repository on GitHub
2. Click "uploading an existing file"
3. Drag and drop all your files
4. Add commit message: "Initial commit: Pi GameUI launcher"
5. Click "Commit changes"

## 🔧 Step 3: Update Repository URLs

After creating your repository, update these files with your actual GitHub URL:

### Update `deploy.sh`
```bash
# Change this line in deploy.sh:
REPO_URL="https://github.com/YOUR_USERNAME/raspbian_ui.git"
```

### Update `README.md`
```bash
# Change this line in README.md:
git clone https://github.com/YOUR_USERNAME/raspbian_ui.git
```

## 🍓 Step 4: Deploy to Raspberry Pi

### Method 1: Using the Deploy Script (Recommended)
```bash
# On your Raspberry Pi, run:
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/raspbian_ui/main/deploy.sh | bash
```

### Method 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/raspbian_ui.git
cd raspbian_ui

# Run setup
chmod +x setup.sh
./setup.sh

# Test the launcher
python3 main.py
```

### Method 3: Using SSH (if you have SSH access)
```bash
# From your local machine, copy files to Pi
scp -r /path/to/raspbian_ui pi@YOUR_PI_IP:/home/pi/

# SSH into your Pi
ssh pi@YOUR_PI_IP

# Run setup on Pi
cd /home/pi/raspbian_ui
chmod +x setup.sh
./setup.sh
```

## 🔄 Step 5: Keep Your Pi Updated

To update your Pi with the latest changes:

```bash
# On your Raspberry Pi
cd /home/pi/raspbian_ui
git pull origin main

# Restart the service if it's running
sudo systemctl restart gameui
```

## 📝 Step 6: Customize for Your Setup

1. **Edit `config.json`** to add your games and apps
2. **Modify `main.py`** to change colors, layout, or features
3. **Add custom assets** to the `assets/` folder
4. **Commit and push** your changes to GitHub

## 🐛 Step 7: Troubleshooting

### Common Issues

**Git not installed on Pi:**
```bash
sudo apt-get update
sudo apt-get install git
```

**Permission denied:**
```bash
chmod +x *.sh
chmod +x *.py
```

**Service won't start:**
```bash
sudo systemctl status gameui
journalctl -u gameui -f
```

**Display issues:**
```bash
# Check if X11 is running
echo $DISPLAY

# Start X11 if needed
startx
```

## 📚 Additional Resources

- [GitHub Documentation](https://docs.github.com/)
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Pygame Documentation](https://www.pygame.org/docs/)

## 🎯 Next Steps

1. **Test thoroughly** on your Raspberry Pi
2. **Customize** the launcher for your needs
3. **Share** your setup with the community
4. **Contribute** improvements back to the project

---

**Happy coding! 🚀**
