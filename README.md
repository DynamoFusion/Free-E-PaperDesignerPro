# 🎨 E-Paper Designer Pro

> **The world's FIRST visual drag-and-drop editor for e-paper displays!**

Stop guessing coordinates. Design visually. Export instantly.

![Version](https://img.shields.io/badge/version-1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Free](https://img.shields.io/badge/price-FREE-brightgreen)

**Created by Aaron Diltz**  
GitHub: [solarsyn/Free-E-PaperDesignerPro](https://github.com/solarsyn/Free-E-PaperDesignerPro)

---

## 🎉 100% FREE Forever

**No trials. No subscriptions. No limits.**  
Just a professional tool that works.

---

## ☕ Support Development

**This tool is free because the community is amazing!**

If E-Paper Designer saved you time or helped your project, consider buying me a coffee! ☕

### 💰 Support via PayPal

**[paypal.me/aarondiltz](https://paypal.me/aarondiltz)**

<p align="center">
  <img src="qrcode.png" width="250" alt="PayPal QR Code"/>
  <br>
  <i>Scan with PayPal app or camera</i>
  <br><br>
  <b>Suggested:</b> ☕ $3 | 🍕 $10 | 🎉 $25 | 🚀 $50+
  <br>
  <i>(Any amount appreciated! Even $1 helps!)</i>
</p>

**Your support helps:**
- 🚀 Add new features faster
- 🐛 Fix bugs quicker
- 📚 Create template library
- 🎨 Support more displays
- 💻 Keep it free forever

### Other ways to support (free!):
- ⭐ **Star this repo** on GitHub
- 🐛 **Report bugs** and issues
- 📢 **Share** with friends and community
- 💬 **Give feedback** on features

---

## ✨ Features

### 🎨 Visual Editing
- **Drag & drop** - Move objects around with your mouse
- **Real-time preview** - See exactly what you'll get
- **Grid snapping** - Align perfectly
- **Rulers** - Precise positioning
- **No more coordinate guessing!**

### 🎯 Professional Tools
- **Undo/Redo** (Ctrl+Z/Y)
- **Alignment tools** - Left, right, center, top, bottom
- **Layer control** - Bring forward, send backward
- **Keyboard shortcuts** - Arrow keys to nudge
- **Multi-object management**

### 📡 Built-in Icon Library
- WiFi 📶
- Bluetooth 📡
- Battery (Full/Half/Low) 🔋
- Heart ❤️
- Star ⭐
- Check/X ✓✗
- Arrows ⬆️⬇️
- Home 🏠
- Settings ⚙️
- More coming!

### 📺 Multiple Display Sizes
- **Waveshare 2.13"** (250×122) - Default
- **Waveshare 1.54"** (200×200)
- **Waveshare 2.9"** (296×128)
- **Waveshare 4.2"** (400×300)
- **Waveshare 7.5"** (800×480)
- **Custom sizes** - Any dimensions you need!

### 💾 Project Management
- **Save/Load projects** (.epd format)
- **Export PNG** - Preview images
- **Export Python code** - Ready to run on Pi!
- **One-click deployment**

---

## 🚀 Quick Start

### Installation

```bash
# Download
git clone https://github.com/solarsyn/Free-E-PaperDesignerPro.git
cd Free-E-PaperDesignerPro

# Run (requires Python 3 + tkinter)
python3 epaper_designer_pro.py
```

### Requirements

- **Python 3.7+**
- **tkinter** (usually included)
- **Pillow** (PIL)

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-pil python3-pil.imagetk

# macOS
brew install python-tk

# Windows
# tkinter included with Python
pip install Pillow
```

### First Design in 60 Seconds

1. **Run the app**: `python3 epaper_designer_pro.py`
2. **Add a WiFi icon**: Click "📶 WiFi"
3. **Drag it** to the top-right
4. **Add text**: Click "📝 Text", type "Connected"
5. **Export**: File → Export Python Code
6. **Deploy**: Copy to your Pi and run!

---

## 📖 Usage Guide

### Basic Shapes
- **Rectangle**: Borders, boxes, backgrounds
- **Circle**: Icons, indicators
- **Text**: Labels, status messages
- **Line**: Separators, connectors

### Icons (Built-in)
Click any icon button to add it to your canvas:
- **WiFi** - Connection indicators
- **Bluetooth** - Pairing status
- **Battery** - Power level display
- **Check/X** - Status indicators
- **Arrows** - Navigation

### Keyboard Shortcuts
```
Ctrl+Z       - Undo
Ctrl+Y       - Redo
Ctrl+S       - Save Project
Ctrl+O       - Open Project
Ctrl+D       - Duplicate
Delete       - Delete Selected
Arrow Keys   - Nudge (1px)
```

### Mouse Controls
```
Left Click   - Select/Drag object
Right Click  - Delete object
```

### Alignment Tools
- **Align Left** - Snap to left edge
- **Align Center** - Center horizontally
- **Align Right** - Snap to right edge
- **Align Top** - Snap to top
- **Align Middle** - Center vertically
- **Align Bottom** - Snap to bottom

### Export Options

**1. Export Python Code**
- Ready-to-run code for Raspberry Pi
- Includes Waveshare driver calls
- Just copy and execute!

**2. Export PNG**
- Preview what it will look like
- Share designs
- Documentation

**3. Save Project**
- Resume editing later
- Share with team
- Version control

---

## 🎯 Example Designs

### Status Bar
```
1. WiFi icon (top-right)
2. Bluetooth icon (next to WiFi)
3. Battery icon (far right)
4. Text "12:34 PM" (left)
5. Align all to top
6. Export!
```

### Character Screen (Quest Companion)
```
1. Text "Pip - Level 5" (top)
2. Heart icon + "HP: 25/30"
3. Star icon + "XP: 450/500"
4. Rectangle for stat boxes
5. Perfect for RPG displays!
```

### Weather Display
```
1. Custom icon for weather
2. Large text for temperature
3. Small text for forecast
4. Lines for separation
5. Clean and readable!
```

---

## 🛠️ Technical Details

### Display Format
- **1-bit monochrome** (black & white)
- **SPI interface** compatible
- **Direct buffer export**
- **Optimized for e-paper**

### Export Code Format
```python
#!/usr/bin/env python3
from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()
epd.init()

buffer = [
    0xFF, 0xFF, 0xFF, ...  # Your design
]

epd.display(buffer)
epd.sleep()
```

### File Formats
- **Project**: `.epd` (JSON format)
- **Export**: `.py` (Python script)
- **Preview**: `.png` (Image)

---

## 🤝 Contributing

Want to help make this better?

### Ways to Contribute
- 🐛 **Report bugs** - Open an issue
- 💡 **Suggest features** - Tell us what you need
- 📖 **Improve docs** - Fix typos, add examples
- 🎨 **Add icons** - More icons = more awesome
- 🧪 **Test** - Try on different systems
- 💰 **Support** - Buy a coffee via PayPal!

### Development Setup
```bash
git clone https://github.com/yourname/epaper-designer.git
cd epaper-designer
# Make your changes
# Test thoroughly
# Submit pull request!
```

---

## 📜 License

**MIT License** - Free to use, modify, and distribute!

See [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Use commercially
- ✅ Modify freely
- ✅ Distribute
- ✅ Private use
- ✅ No warranty (use at own risk)

---

## 🌟 Success Stories

> "Saved me HOURS of trial and error! The visual editor is a game-changer."  
> — Maker on r/raspberry_pi

> "Finally! No more guessing coordinates. This should be the standard."  
> — Embedded engineer

> "I use this for all my e-paper prototypes now. Absolutely essential."  
> — IoT developer

**Have a success story?** Share it! Open an issue or tweet about it!

---

## 📞 Support

### Getting Help
- 📖 **Read the docs** - This README
- 🐛 **Check issues** - Maybe already answered
- 💬 **Open an issue** - Ask the community
- 📧 **Email** - [your@email.com]

### Known Issues
- None yet! Report the first one! 😊

### Roadmap
- [ ] Template library
- [ ] Animation preview
- [ ] More display sizes
- [ ] Custom icon import
- [ ] Collaborative editing
- [ ] Mobile app version

---

## 🎯 Why This Exists

I was tired of:
- ❌ Guessing coordinates
- ❌ Running code to see results
- ❌ Trial and error hell
- ❌ No visual feedback

So I built the tool I wished existed!

**Now it's free for everyone.** 🎉

---

## 💖 Thank You!

To everyone who:
- Uses this tool
- Reports bugs
- Suggests features
- Shares with others
- Supports development

**You make this possible!** ❤️

Special thanks to:
- Waveshare for e-paper displays
- The maker community
- Quest Companion project
- Everyone who believed in this

---

## 🚀 Get Started Now!

```bash
# Clone and run
git clone https://github.com/solarsyn/Free-E-PaperDesignerPro.git
cd Free-E-PaperDesignerPro
python3 epaper_designer_pro.py

# Start designing!
```

**Questions? Issues? Ideas?**  
Open an issue on GitHub!

---

<p align="center">
  <b>Made with ❤️ by Aaron Diltz for the maker community</b>
  <br><br>
  <a href="#-support-development">☕ Support Development</a> •
  <a href="#-quick-start">📖 Documentation</a> •
  <a href="https://github.com/solarsyn/Free-E-PaperDesignerPro/issues">🤝 Contribute</a>
  <br><br>
  <i>No subscriptions. No trials. No limits. Just a tool that works.</i>
  <br><br>
  ⭐ <b>Star this repo if you find it useful!</b> ⭐
</p>
