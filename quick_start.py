#!/usr/bin/env python3
"""
🚀 QUICK START - YouTube to Viral Video (Auto-Device)
ใช้ได้แบบสั้นๆ ปล่อยให้ระบบเลือก CPU/GPU อัตโนมัติ
"""

import sys
import os

def detect_best_device():
    """เลือก device ที่ดีที่สุดอัตโนมัติ"""
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU พบ: {gpu_name}")
            print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
            return "cuda"
        else:
            print("⚠️  GPU ไม่พบ - ใช้ CPU")
            return "cpu"
    except:
        print("💻 ใช้ CPU")
        return "cpu"

def main():
    print("\n" + "="*60)
    print("🎬 QUICK START - Viral Video Generator".center(60))
    print("="*60 + "\n")
    
    # รับ YouTube URL
    url = input("📍 ใส่ YouTube URL (หรือ path ของไฟล์วิดีโอ): ").strip()
    if not url:
        print("❌ URL ว่าง")
        return 1
    
    # เลือก device
    print("\n🔍 กำลังตรวจสอบระบบ...\n")
    device = detect_best_device()
    
    # กำหนด model ตามการตรวจสอบ
    if device == "cuda":
        model = "small"  # GPU ค่อนข้างไว
        preset = "medium"
        print(f"\n⚙️  ตั้งค่า: Model={model}, Preset={preset}, Device={device}")
    else:
        model = "tiny"   # CPU ต้องใช้ model เล็ก
        preset = "ultrafast"
        print(f"\n⚙️  ตั้งค่า: Model={model}, Preset={preset}, Device={device}")
        print("   ⏳ CPU ช้า - ใช้เวลา 15-30 นาที")
    
    # ถามว่า render ไหม
    print("\n🎬 ตัวเลือก rendering:")
    print("  1. เต็ม (ข้อความเต็ม frame) - ช้าที่สุด")
    print("  2. เฉพาะวิเคราะห์ (ไม่เรนเดอร์) - เร็วที่สุด")
    choice = input("  เลือก (1-2, default=2): ").strip() or "2"
    
    no_render = choice == "2"
    
    # สร้าง command
    cmd = f'python main_integrated.py --input "{url}" --model {model} --preset {preset} --device {device} --no-vision'
    
    if no_render:
        cmd += " --no-render"
    
    print(f"\n▶️  รันคำสั่ง:\n   {cmd}\n")
    print("="*60)
    print("⏳ กำลังประมวลผล... (รอสักครู่)\n")
    
    # รัน
    os.system(cmd)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
