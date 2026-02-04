# ⚡ QUICKSTART - E-Paper Designer Pro

## 🎯 Get Running in 3 Minutes!

### 1️⃣ Extract (10 seconds)
```bash
tar -xzf epaper-designer-pro-v1.0-COMPLETE.tar.gz
cd epaper-designer-pro
```

### 2️⃣ Check Setup (20 seconds)
```bash
python3 check_setup.py
```

If you see "✅ ALL CHECKS PASSED!" → You're ready!

If not, install missing dependencies:
```bash
# Linux
sudo apt-get install python3-tk python3-pil

# macOS  
brew install python-tk && pip3 install Pillow

# Windows
pip install Pillow
```

### 3️⃣ Launch! (5 seconds)
```bash
python3 epaper_designer_pro.py
```

**Done!** 🎉

---

## 🎨 Your First Design (2 minutes)

### Design a Status Bar:

1. **Add WiFi icon**
   - Click "📶 WiFi" button
   - Drag it to top-right corner

2. **Add Battery icon**
   - Click "🔋 Battery Full"
   - Drag next to WiFi

3. **Add Text**
   - Click "📝 Text"
   - Type "12:34 PM"
   - Drag to top-left

4. **Export**
   - Menu: File → Export Python Code
   - Save as `status_bar.py`

5. **Deploy to Pi**
   ```bash
   scp status_bar.py pi@raspberrypi:~
   ssh pi@raspberrypi
   python3 status_bar.py
   ```

**Your design is now on the e-paper display!** ✨

---

## 💡 Pro Tips

### Keyboard Shortcuts:
- `Ctrl+Z` - Undo
- `Ctrl+S` - Save project
- `Del` - Delete selected
- `Arrow keys` - Nudge 1px

### Mouse:
- `Left click` - Select/Drag
- `Right click` - Delete

### Alignment:
- Use alignment buttons for perfect positioning
- Enable "Grid Snap" for 5px precision

---

## 🆘 Troubleshooting

### Can't see QR code in Support dialog?
Make sure `qrcode.png` is in the same folder as the .py file!

### "No module named tkinter"?
```bash
sudo apt-get install python3-tk
```

### "No module named PIL"?
```bash
pip3 install Pillow
```

---

## 📚 Learn More

- **Full docs:** `README_EPAPER_DESIGNER.md`
- **Detailed install:** `INSTALL.md`
- **Help in app:** Help → Keyboard Shortcuts

---

## ☕ Love It? Support It!

**Help → Support Development** in the app

Scan the QR code or use PayPal to buy me a coffee! ❤️

---

**That's it! Start designing!** 🚀

Questions? Check the README or open an issue on GitHub!
