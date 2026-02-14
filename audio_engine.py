import os
import subprocess
import glob
from faster_whisper import WhisperModel

class AudioEngine:
    """Component 1: Audio & Speech Engine (Whisper)
    
    ฟังก์ชัน: แปลงวิดีโอ → เสียง → ข้อความ พร้อมตำแหน่งเวลา (Word-level Timestamps)
    """
    
    def __init__(self, model_size="large-v3-turbo", device="cuda", compute_type=None):
        """
        Args:
            model_size: ขนาดโมเดล Whisper (tiny, base, small, medium, large, large-v3-turbo)
            device: "cuda" หรือ "cpu"
            compute_type: "float16" หรือ "int8"
        """
        self.model_size = model_size
        self.device = device
        
        # กำหนด compute_type อัตโนมัติถ้าไม่ระบุ
        if compute_type is None:
            self.compute_type = "float16" if device == "cuda" else "int8"
        else:
            self.compute_type = compute_type
            
        print(f"🔧 กำลังสร้าง AudioEngine...")
        print(f"   - Model: {self.model_size}")
        print(f"   - Device: {self.device}")
        print(f"   - Compute: {self.compute_type}")
        
        try:
            # Use positional argument for model_size_or_path
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
        except Exception as e:
            print(f"   ⚠️  Retrying with minimal parameters: {e}")
            try:
                # Last resort - minimal parameters
                self.model = WhisperModel(self.model_size, device=self.device)
            except Exception as e2:
                print(f"   ❌ Failed: {e2}")
                raise
    
    def convert_to_wav(self, input_media, output_wav="temp_audio.wav"):
        """แปลงวิดีโอ/เสียงให้เป็น WAV 16kHz Mono เพื่อเตรียมสำหรับ Whisper
        
        Args:
            input_media: ไฟล์วิดีโอ
            output_wav: ไฟล์เสียง WAV ที่เอาต์พุต
            
        Returns:
            path ของไฟล์ WAV
        """
        print("🔄 1. กำลังแปลงไฟล์เป็น WAV 16kHz...")
        
        # หา FFmpeg ตามลำดับก่อนหลัง
        ffmpeg_exe = self._find_ffmpeg()
        
        cmd = [
            ffmpeg_exe, "-y", "-i", input_media,
            "-ac", "1", "-ar", "16000", "-vn",
            "-f", "wav", output_wav
        ]
        
        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"   ✅ สำเร็จ: {output_wav}")
            return output_wav
            
        except FileNotFoundError as e:
            print(f"❌ ไม่พบ FFmpeg: {e}")
            raise RuntimeError(
                "FFmpeg ไม่พบ! ติดตั้ง FFmpeg หรือตั้งค่า PATH"
            )
    
    def transcribe(self, audio_path, beam_size=5, word_timestamps=True):
        """แกะเสียงเป็นข้อความพร้อม Timestamps ของแต่ละคำ
        
        Args:
            audio_path: เส้นทางไฟล์เสียง
            beam_size: ขนาด beam search (สูง = แม่นยำแต่ช้า)
            word_timestamps: True = ให้ timestamp ของแต่ละคำ
            
        Returns:
            (segments, info): segments = รายการ segment, info = ข้อมูลทั่วไป
        """
        print(f"🎙️ 2. กำลังแกะเสียงด้วย {self.model_size} (Word-level)...")
        
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=beam_size,
            word_timestamps=word_timestamps,
            condition_on_previous_text=False
        )
        
        # แปลง generator เป็น list เพื่อให้ใช้ซ้ำได้
        segments_list = list(segments)
        
        print(f"   ✅ ตรวจพบภาษา: {info.language}")
        print(f"   ✅ จำนวน segments: {len(segments_list)}")
        
        return segments_list, info
    
    def _find_ffmpeg(self):
        """หา FFmpeg executable
        
        ลำดับการค้นหา:
        1. ตามเส้นทางที่กำหนดไว้ (Windows built-in)
        2. ค้นหาแบบ recursive จากทำเนียบโปรเจกต์
        3. ใช้ชื่อตรงๆจากระบบ (เผื่ออยู่ใน PATH)
        """
        # ลำดับที่ 1: Fast path
        common_paths = [
            r"C:\Webpedpok\ffmpeg-2026-02-09-git-9bfa1635ae-essentials_build\bin\ffmpeg.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # ลำดับที่ 2: Recursive search
        search_pattern = os.path.join(os.getcwd(), "**", "ffmpeg.exe")
        found = glob.glob(search_pattern, recursive=True)
        if found:
            print(f"   🔎 พบ FFmpeg ที่: {found[0]}")
            return found[0]
        
        # ลำดับที่ 3: System PATH
        return "ffmpeg"
