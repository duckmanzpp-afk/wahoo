<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
>>>>>>> aa72dfb (Initial project setup: WebPedPok YouTube video analysis and content intelligence system)
import os
import time
import torch
import subprocess
from faster_whisper import WhisperModel

# ==========================================
# 1. CONFIGURATION (ตั้งค่าที่นี่)
# ==========================================
INPUT_FILE = "test.mp4"        # ไฟล์ที่คุณต้องการวิเคราะห์
OUTPUT_REPORT = "analysis_report.txt"
MODEL_SIZE = "large-v3-turbo"  # ตัวท็อป แม่นยำที่สุด

# ตรวจสอบอุปกรณ์ (GPU หรือ CPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "float16" if DEVICE == "cuda" else "int8"

# ==========================================
# 2. ฟังก์ชันแปลงเสียง (FFmpeg)
# ==========================================
def extract_audio(input_media):
    temp_wav = "temp_audio_for_analysis.wav"
    print("🔄 1. กำลังสกัดเสียงจากวิดีโอ...")
    
    # 1. ลองใช้ Path ที่คุณระบุไว้
    ffmpeg_exe = r"C:\Webpedpok\ffmpeg-2026-02-09-git-9bfa1635ae-essentials_build\bin\ffmpeg.exe"
    
    # 2. ถ้าหาไม่เจอ ให้ลองหาในโฟลเดอร์โปรเจกต์ (C:\Webpedpok) แบบอัตโนมัติ
    if not os.path.exists(ffmpeg_exe):
        import glob
        search_path = os.path.join(os.getcwd(), "**", "ffmpeg.exe")
        found = glob.glob(search_path, recursive=True)
        if found:
            ffmpeg_exe = found[0]
            print(f"🔎 พบ FFmpeg อัตโนมัติที่: {ffmpeg_exe}")
        else:
            # 3. ไม้ตายสุดท้าย ลองเรียกสั้นๆ (เผื่ออยู่ใน System Path)
            ffmpeg_exe = "ffmpeg"

    cmd = [
        ffmpeg_exe, "-y", "-i", input_media,
        "-ac", "1", "-ar", "16000", "-vn", "-f", "wav", temp_wav
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"❌ Error: ไม่สามารถเรียกใช้ FFmpeg ได้! (สาเหตุ: {e})")
        print("💡 วิธีแก้: ตรวจสอบว่ามีไฟล์ ffmpeg.exe อยู่ในเครื่องจริงๆ หรือไม่")
        raise
        
    return temp_wav

# ==========================================
# 3. ระบบวิเคราะห์เนื้อหาหลัก
# ==========================================
def analyze_content():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ไม่พบไฟล์ {INPUT_FILE}")
        return

    # เตรียมไฟล์เสียง
    audio_path = extract_audio(INPUT_FILE)

    # โหลด AI
    print(f"🚀 2. กำลังโหลด AI Model ({MODEL_SIZE})...")
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

    print("🎙️ 3. AI กำลังวิเคราะห์เนื้อหา (กรุณารอสักครู่)...")
    start_time = time.time()
    
    # เริ่มการแกะเสียงและวิเคราะห์
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    all_text = []
    print("\n" + "="*50)
    print("📝 ผลการวิเคราะห์เนื้อหา (Live Preview):")
    print("="*50)

    for segment in segments:
        print(f"[{segment.start:6.2f}s -> {segment.end:6.2f}s] {segment.text}")
        all_text.append(segment.text.strip())

    elapsed_time = time.time() - start_time
    full_script = " ".join(all_text)
    
    # บันทึกรายงาน
    print("\n" + "="*50)
    print("📊 สรุปรายงาน:")
    print("="*50)
    print(f"ภาษา: {info.language}")
    print(f"เวลาการวิเคราะห์: {elapsed_time:.2f} วินาที")
    
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(f"Analysis Report\n")
        f.write(f"Language: {info.language}\n")
        f.write(f"Duration: {elapsed_time:.2f} seconds\n\n")
        f.write(f"Full Transcript:\n{full_script}")
    
    print(f"\n✅ บันทึกรายงานแล้ว: {OUTPUT_REPORT}")
    
    # ทำความสะอาดไฟล์ชั่วคราว
    if os.path.exists(audio_path):
        os.remove(audio_path)

if __name__ == "__main__":
    analyze_content()