#!/usr/bin/env python3
"""
Git Installer Helper for Windows
Downloads and guides installation of Git for Windows
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

def download_git():
    """Download Git installer from GitHub"""
    url = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    temp_dir = Path(os.environ.get('TEMP', 'C:\\Temp'))
    installer = temp_dir / "GitInstaller.exe"
    
    print("📥 Downloading Git for Windows...")
    print(f"   URL: {url}")
    print(f"   To: {installer}")
    
    try:
        urllib.request.urlretrieve(url, installer)
        print(f"✅ Download successful: {installer}")
        return installer
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def check_git():
    """Check if Git is available"""
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Git not found")
    return False

def main():
    print("\n" + "="*60)
    print("🔧 Git Installation Helper")
    print("="*60 + "\n")
    
    # Check if already installed
    if check_git():
        print("\n✨ You're all set! Run: python github_upload.py")
        return 0
    
    # Download installer
    installer = download_git()
    if not installer:
        print("\n❌ Could not download Git installer")
        print("   Manual download: https://git-scm.com/download/win")
        return 1
    
    print("\n" + "="*60)
    print("📋 NEXT STEPS:")
    print("="*60)
    print(f"\n1️⃣  Double-click: {installer}")
    print("\n2️⃣  Follow installer prompts (accept defaults is fine):\n")
    print("   - License: Click Next")
    print("   - Installation location: C:\\Program Files\\Git")
    print("   - Components: Keep defaults")
    print("   - Default editor: Use Vim (or your preference)")
    print("   - Default branch: main")
    print("   - PATH environment: 'Git from the command line...'")
    print("   - HTTPS transport: Use OpenSSL")
    print("   - Line ending: 'Checkout Windows-style...'")
    print("   - Terminal: MinTTY")
    print("   - Pull strategy: Default (fast-forward)")
    print("\n3️⃣  Wait for installation to complete\n")
    print("4️⃣  Open NEW PowerShell window and run:")
    print("   git --version")
    print("\n5️⃣  Then run:")
    print("   python github_upload.py\n")
    
    print("="*60)
    print("⏳ Waiting for installer... (This window will stay open)")
    print("="*60)
    
    # Try to execute installer
    try:
        subprocess.Popen(str(installer))
        print(f"\n✅ Installer launched: {installer}")
        print("\n⚠️  IMPORTANT:")
        print("   - Installation usually takes 1-2 minutes")
        print("   - When done, CLOSE this window")
        print("   - Open a NEW PowerShell window")
        print("   - Run: python github_upload.py")
        
        input("\n⏸️  Press ENTER when installation is complete...")
        
    except Exception as e:
        print(f"\n❌ Could not launch installer: {e}")
        print(f"\n💡 Try manually running: {installer}")
        return 1
    
    # Verify installation
    print("\n🔍 Checking if Git is installed...")
    if check_git():
        print("\n✨ Perfect! Now run: python github_upload.py")
        return 0
    else:
        print("\n⚠️  Git still not found. Possible reasons:")
        print("   1. Installation not complete yet")
        print("   2. Need to open a NEW PowerShell window")
        print("   3. Need to restart computer")
        print("\n💡 Try opening NEW PowerShell and run: git --version")
        return 1

if __name__ == "__main__":
    sys.exit(main())
