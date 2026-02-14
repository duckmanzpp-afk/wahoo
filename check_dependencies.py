#!/usr/bin/env python3
"""
🔍 Dependency Verification Script
ตรวจสอบว่า dependencies ติดตั้งถูกต้องหรือไม่
"""

import sys
from pathlib import Path

def check_import(module_name, package_name=None, required=True):
    """Check if a module can be imported"""
    display_name = package_name or module_name
    
    try:
        __import__(module_name)
        status = "✅"
        print(f"{status} {display_name:<30} INSTALLED")
        return True
    except ImportError as e:
        if required:
            status = "❌"
            print(f"{status} {display_name:<30} MISSING - pip install {package_name or module_name}")
        else:
            status = "⚠️ "
            print(f"{status} {display_name:<30} OPTIONAL")
        return False

def check_cuda():
    """Check CUDA availability"""
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            device_count = torch.cuda.device_count()
            print(f"✅ CUDA Support                ENABLED ({device_count} GPU)")
            print(f"   - Device: {device_name}")
            return True
        else:
            print(f"⚠️  CUDA Support                DISABLED (using CPU)")
            return False
    except:
        return False

def main():
    print("\n" + "="*60)
    print("🔍 VIRAL VIDEO SYSTEM - DEPENDENCY CHECK".center(60))
    print("="*60 + "\n")
    
    required_ok = True
    optional_ok = True
    
    # Required dependencies
    print("📦 REQUIRED DEPENDENCIES")
    print("-" * 60)
    
    required_modules = [
        ("faster_whisper", "faster-whisper"),
        ("torch", "torch"),
        ("torchaudio", "torchaudio"),
        ("openai", "openai"),
        ("cv2", "opencv-python"),
        ("numpy", "numpy"),
        ("moviepy", "moviepy"),
        ("imageio", "imageio"),
    ]
    
    for module, package in required_modules:
        if not check_import(module, package, required=True):
            required_ok = False
    
    print()
    
    # Optional dependencies
    print("📦 OPTIONAL DEPENDENCIES")
    print("-" * 60)
    
    optional_modules = [
        ("mediapipe", "mediapipe"),
        ("dotenv", "python-dotenv"),
    ]
    
    for module, package in optional_modules:
        if not check_import(module, package, required=False):
            optional_ok = False
    
    print()
    
    # Check CUDA
    print("⚙️ HARDWARE ACCELERATION")
    print("-" * 60)
    check_cuda()
    
    print("\n" + "="*60)
    
    if not required_ok:
        print("\n❌ MISSING REQUIRED DEPENDENCIES!")
        print("   Run: pip install -r requirements.txt")
        return 1
    
    if not optional_ok:
        print("\n⚠️ Some optional dependencies are missing.")
        print("   Those components will be disabled during runtime.")
    
    print("\n✅ ALL CHECKS PASSED!")
    print("   Ready to run: python main_integrated.py\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
