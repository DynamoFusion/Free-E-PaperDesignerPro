# 🚀 E-Paper Designer Pro - Installation Guide

## ⚡ Quick Install (60 seconds)

### Step 1: Download
Download the release package and extract it:
```bash
tar -xzf epaper-designer-pro-v1.0-RELEASE.tar.gz
cd epaper-designer-pro
```

Or from GitHub:
```bash
git clone https://github.com/yourname/epaper-designer.git
cd epaper-designer
```

### Step 2: Install Requirements

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-tk python3-pil python3-pil.imagetk
```

**macOS:**
```bash
brew install python-tk
pip3 install Pillow
```

**Windows:**
```bash
# tkinter comes with Python
pip install Pillow
```

### Step 3: Run!
```bash
python3 epaper_designer_pro.py
```

**That's it!** 🎉

---

## 📁 File Structure

After extraction, you should have:
```
epaper-designer-pro/
├── epaper_designer_pro.py    ← Main application
├── qrcode.png                 ← PayPal QR code (for donations)
└── README_EPAPER_DESIGNER.md  ← Full documentation
```

**IMPORTANT:** Keep `qrcode.png` in the same folder as the .py file!

---

## 🖥️ System Requirements

### Minimum:
- **OS:** Windows 7+, macOS 10.12+, Linux (any modern distro)
- **Python:** 3.7 or higher
- **RAM:** 256MB
- **Display:** 800×600 or higher

### Recommended:
- **Python:** 3.9+
- **RAM:** 512MB+
- **Display:** 1920×1080

---

## 🔧 Troubleshooting

### "No module named 'tkinter'"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Reinstall Python and check "tcl/tk and IDLE" during installation.

### "No module named 'PIL'"

```bash
pip3 install Pillow
```

Or:
```bash
python3 -m pip install Pillow
```

### QR Code Not Showing

Make sure `qrcode.png` is in the same folder as `epaper_designer_pro.py`:
```bash
ls -la
# Should show both files
```

### Permission Denied

**Linux/macOS:**
```bash
chmod +x epaper_designer_pro.py
python3 epaper_designer_pro.py
```

---

## 🎯 First Run

When you first launch:

1. **Window opens** with canvas and tools
2. **Try adding a shape** - Click "📐 Rectangle"
3. **Drag it around** - Click and drag!
4. **Add an icon** - Click "📶 WiFi"
5. **Export code** - File → Export Python Code
6. **You're ready!** 🎉

---

## 📚 Learning Resources

### Built-in Help:
- **Help → Keyboard Shortcuts** - All shortcuts
- **Help → About** - Version info
- **Help → Support Development** - If you like it! ☕

### Documentation:
- **README_EPAPER_DESIGNER.md** - Complete guide
- **Examples** - Coming soon!
- **Video tutorials** - Coming soon!

---

## 🚀 Next Steps

### Design Your First Screen:
1. Open the app
2. Add a WiFi icon (top-right)
3. Add text "Connected" 
4. Add a battery icon
5. Export Python code
6. Copy to your Raspberry Pi
7. Run it!

### Join the Community:
- ⭐ Star on GitHub
- 🐛 Report bugs
- 💡 Request features
- 📢 Share your designs

---

## 💖 Support Development

If this tool saves you time, consider buying me a coffee! ☕

**Help → Support Development** in the app  
or scan the QR code in `qrcode.png`

Every contribution helps keep this free and improving!

---

## 🆘 Getting Help

**Found a bug?**
- Open an issue on GitHub
- Include: OS, Python version, error message

**Have a question?**
- Check the README first
- Search existing issues
- Ask the community

**Want a feature?**
- Open a feature request
- Describe your use case
- Community will vote!

---

## ✅ Installation Complete!

You're ready to start designing e-paper displays visually!

```bash
python3 epaper_designer_pro.py
```

**Happy designing!** 🎨✨

---

<p align="center">
  <b>Made with ❤️ for the maker community</b>
  <br>
  <i>No subscriptions. No trials. No limits.</i>
</p>
