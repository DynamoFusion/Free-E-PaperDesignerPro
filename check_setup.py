#!/usr/bin/env python3
"""
E-Paper Designer Pro - Setup Check
Verifies everything is ready to run
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.7+)")
        return False

def check_tkinter():
    """Check if tkinter is available"""
    print("🖼️  Checking tkinter...")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide window
        root.destroy()
        print("   ✅ tkinter available")
        return True
    except ImportError:
        print("   ❌ tkinter not found")
        print("      Install: sudo apt-get install python3-tk")
        return False
    except Exception as e:
        print(f"   ⚠️  tkinter error: {e}")
        return False

def check_pillow():
    """Check if Pillow (PIL) is available"""
    print("🖼️  Checking Pillow (PIL)...")
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageTk
        print("   ✅ Pillow available")
        return True
    except ImportError:
        print("   ❌ Pillow not found")
        print("      Install: pip3 install Pillow")
        return False

def check_files():
    """Check if required files exist"""
    print("📁 Checking files...")
    
    files_status = []
    
    # Main script
    if os.path.exists('epaper_designer_pro.py'):
        print("   ✅ epaper_designer_pro.py")
        files_status.append(True)
    else:
        print("   ❌ epaper_designer_pro.py (REQUIRED)")
        files_status.append(False)
    
    # QR code (optional but nice to have)
    if os.path.exists('qrcode.png'):
        print("   ✅ qrcode.png (PayPal QR code)")
        files_status.append(True)
    else:
        print("   ⚠️  qrcode.png (optional - for donation QR)")
        files_status.append(True)  # Not critical
    
    # README (optional)
    if os.path.exists('README_EPAPER_DESIGNER.md'):
        print("   ✅ README_EPAPER_DESIGNER.md")
    else:
        print("   ⚠️  README_EPAPER_DESIGNER.md (optional)")
    
    return all(files_status)

def check_paypal_link():
    """Check if PayPal link is configured"""
    print("💰 Checking PayPal configuration...")
    
    try:
        with open('epaper_designer_pro.py', 'r') as f:
            content = f.read()
            
        if 'paypal.me/yourname' in content:
            print("   ⚠️  PayPal link not configured (still 'yourname')")
            print("      Update 'paypal.me/yourname' to your actual link")
            return False
        elif 'paypal.me/' in content:
            print("   ✅ PayPal link configured")
            return True
        else:
            print("   ⚠️  PayPal link not found")
            return False
    except:
        print("   ⚠️  Could not check PayPal link")
        return True

def main():
    """Run all checks"""
    print("=" * 50)
    print("🎨 E-Paper Designer Pro - Setup Check")
    print("=" * 50)
    print()
    
    checks = []
    
    # Required checks
    checks.append(("Python Version", check_python_version()))
    checks.append(("tkinter", check_tkinter()))
    checks.append(("Pillow", check_pillow()))
    checks.append(("Files", check_files()))
    
    # Optional checks
    paypal_ok = check_paypal_link()
    
    print()
    print("=" * 50)
    print("📊 Results")
    print("=" * 50)
    
    all_passed = all(result for name, result in checks)
    
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("🚀 You're ready to run E-Paper Designer Pro!")
        print()
        print("   python3 epaper_designer_pro.py")
        print()
        
        if not paypal_ok:
            print("💡 TIP: Update your PayPal link before sharing!")
            print("   Find 'paypal.me/yourname' in the code")
            print("   Replace with your actual PayPal.me username")
            print()
    else:
        print("❌ SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before running.")
        print()
        
        # Show what failed
        for name, result in checks:
            if not result:
                print(f"   ❌ {name}")
        
        print()
        print("See INSTALL.md for detailed instructions.")
    
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
