#!/usr/bin/env python3
"""
🎥 YouTube Video Downloader & Processor
ดาวน์โหลดจาก YouTube และประมวลผลด้วย Viral Video Generator
"""

import os
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlparse

def is_youtube_url(url: str) -> bool:
    """ตรวจสอบว่าเป็น YouTube URL หรือไม่"""
    youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com', 'www.youtube.com']
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in youtube_domains)

def download_from_youtube(youtube_url: str, output_file: str = "downloaded_video.mp4") -> str:
    """ดาวน์โหลดวิดีโอจาก YouTube
    
    Args:
        youtube_url: URL ของ YouTube video
        output_file: ชื่อไฟล์ที่จะบันทึก
        
    Returns:
        str: path ของไฟล์ที่ดาวน์โหลด
    """
    print("\n" + "="*60)
    print("🎥 YOUTUBE VIDEO DOWNLOADER".center(60))
    print("="*60 + "\n")
    
    # ตรวจสอบ URL
    if not is_youtube_url(youtube_url):
        print(f"❌ URL ไม่ใช่ YouTube: {youtube_url}")
        return None
    
    print(f"📥 กำลังดาวน์โหลดจาก YouTube...")
    print(f"   URL: {youtube_url}")
    print(f"   Output: {output_file}\n")
    
    # สั่ง yt-dlp ดาวน์โหลด
    cmd = [
        "yt-dlp",
        "-f", "best[height<=720]/best",  # ไม่ให้เกิน 720p (เร็วขึ้น)
        "-o", output_file,
        youtube_url
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        
        # ตรวจสอบว่ามีไฟล์จริง
        if os.path.exists(output_file):
            file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"\n✅ ดาวน์โหลดสำเร็จ!")
            print(f"   ไฟล์: {output_file}")
            print(f"   ขนาด: {file_size_mb:.1f} MB\n")
            return output_file
        else:
            print(f"❌ ไฟล์ไม่ถูกสร้าง")
            return None
            
    except FileNotFoundError:
        print("❌ ไม่พบ yt-dlp - ติดตั้งด้วย: pip install yt-dlp")
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🎬 VIRAL VIDEO GENERATOR - YOUTUBE MODE".center(60))
    print("="*60 + "\n")
    
    # รับ YouTube URL จากผู้ใช้
    youtube_url = input("📍 ใส่ YouTube URL: ").strip()
    
    if not youtube_url:
        print("❌ URL ว่าง")
        return 1
    
    # ชื่อไฟล์เอาต์พุต
    output_name = input("📝 ชื่อไฟล์เอาต์พุต (default: youtube_video.mp4): ").strip()
    if not output_name:
        output_name = "youtube_video.mp4"
    
    # ดาวน์โหลด
    downloaded_file = download_from_youtube(youtube_url, output_name)
    
    if not downloaded_file:
        print("❌ ดาวน์โหลดไม่สำเร็จ")
        return 1
    
    # ถามว่าต้องการประมวลผลไหม
    process = input("\n🎬 ต้องการประมวลผลด้วย Viral Video Generator ไหม? (y/n): ").strip().lower()
    
    if process == 'y':
        print("\n▶️  เรียก main_integrated.py...\n")
        os.system(f"python main_integrated.py --input {downloaded_file}")
    else:
        print(f"\n✅ ไฟล์ดาวน์โหลดสำเร็จ: {downloaded_file}")
        print("   คุณสามารถประมวลผลด้วย:")
        print(f"   python main_integrated.py --input {downloaded_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
