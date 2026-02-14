#!/usr/bin/env python3
"""
=========================================
🎬 VIRAL VIDEO AUTO-GENERATOR SYSTEM 🎬
=========================================

4-Component Architecture:
1. AudioEngine      - แกะเสียงเป็นข้อความ (Whisper)
2. ContentIntelligence - วิเคราะห์หา viral moments (GPT)
3. VisionEngine     - auto-reframe ใบหน้า (MediaPipe)
4. VideoRenderer    - เรนเดอร์วิดีโอออกมา (MoviePy)

Workflow: Test.mp4 → Audio Extract → Transcribe → Analyze → Vision → Render → viral_output.mp4

BONUS: Support YouTube URLs - Auto-download & process!
"""

import os
import time
import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

# Import components
from audio_engine import AudioEngine
from content_intelligence import ContentIntelligence
from vision_engine import VisionEngine
from video_renderer import VideoRenderer

# ==========================================
# 🎥 YOUTUBE HELPER FUNCTIONS
# ==========================================
def is_youtube_url(url: str) -> bool:
    """ตรวจสอบว่าเป็น YouTube URL หรือไม่"""
    youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com', 'www.youtube.com']
    try:
        parsed_url = urlparse(url)
        return any(domain in parsed_url.netloc for domain in youtube_domains)
    except:
        return False

def download_youtube_video(youtube_url: str, output_file: str = "youtube_download.mp4") -> str:
    """ดาวน์โหลดจาก YouTube
    
    Args:
        youtube_url: YouTube URL
        output_file: ชื่อไฟล์เอาต์พุต
        
    Returns:
        str: path ของไฟล์ที่ดาวน์โหลด หรือ None
    """
    print("\n📥 กำลังดาวน์โหลดจาก YouTube...")
    print(f"   URL: {youtube_url}")
    print("   ⏳ อาจใช้เวลาสักครู่...\n")
    
    try:
        # ใช้ python -m yt_dlp กับ devnull เพื่อเร็ว
        cmd = [
            sys.executable,
            "-m", "yt_dlp",
            "-f", "best[height<=720]/best",
            "-o", output_file,
            "--quiet",  # ลดการแสดง log
            youtube_url
        ]
        
        result = subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        
        if os.path.exists(output_file):
            file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            file_duration_info = ""
            try:
                import mediainfo
                file_duration_info = " (ตรวจสอบระยะเวลา)"
            except:
                pass
            
            print(f"   ✅ ดาวน์โหลดสำเร็จ ({file_size_mb:.1f} MB){file_duration_info}")
            return output_file
        else:
            print(f"   ❌ ไฟล์ไม่ถูกสร้าง")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"   ⏱️  หมดเวลา (>5 นาที) - วิดีโออาจยาวเกินไป")
        print("   💡 ลองใช้: --model tiny หรือ --preset ultrafast")
        return None
    except Exception as e:
        print(f"   ❌ yt-dlp error: {str(e)[:100]}")
        print("   💡 ตรวจสอบ:")
        print("      - URL ถูกต้องไหม")
        print("      - Internet connection OK?")
        print("      - ลอง: pip install --upgrade yt-dlp")
        return None

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
class Config:
    # Input/Output
    INPUT_VIDEO = "test.mp4"
    OUTPUT_VIDEO = "output_viral.mp4"
    OUTPUT_VIDEO_9_16 = "output_viral_9_16.mp4"
    OUTPUT_REPORT = "analysis_report.json"
    TEMP_AUDIO = "temp_audio.wav"
    
    # Audio Engine
    WHISPER_MODEL = "large-v3-turbo"
    DEVICE = "cuda"  # หรือ "cpu"
    
    # Content Intelligence
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
    CONTENT_ANALYSIS_NUM = 3  # จำนวน moments ที่มองหา
    
    # Vision Engine
    FACE_CONFIDENCE = 0.5
    
    # Video Rendering
    OUTPUT_FPS = 30
    VIDEO_CODEC = "libx264"
    PRESET = "medium"  # ultrafast, fast, medium, slow
    
    # Features
    ENABLE_VISION = True
    ENABLE_9_16_FORMAT = True
    RENDER_OUTPUT = True


# ==========================================
# 🚀 MAIN ORCHESTRATOR
# ==========================================
class ViralVideoGenerator:
    """Main orchestrator ที่ประสานทำงาน 4 components"""
    
    def __init__(self, config=Config):
        self.config = config
        self.audio_engine = None
        self.content_intelligence = None
        self.vision_engine = None
        self.video_renderer = None
        self.segments = None
        self.info = None
        self.moments = None
        self.vision_data = None
        
        print("\n" + "="*60)
        print("🎬 VIRAL VIDEO AUTO-GENERATOR SYSTEM 🎬".center(60))
        print("="*60 + "\n")
    
    def initialize_components(self):
        """สร้าง instances ของทั้ง 4 components"""
        print("📦 INITIALIZATION PHASE\n")
        print("-" * 60)
        
        try:
            # 1. AudioEngine
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.audio_engine = AudioEngine(
                model_size=self.config.WHISPER_MODEL,
                device=device
            )
            print()
            
            # 2. ContentIntelligence
            self.content_intelligence = ContentIntelligence(
                api_key=self.config.OPENAI_API_KEY
            )
            print()
            
            # 3. VisionEngine (optional)
            if self.config.ENABLE_VISION:
                try:
                    self.vision_engine = VisionEngine(
                        confidence=self.config.FACE_CONFIDENCE
                    )
                    print()
                except ImportError:
                    print("⚠️  Vision disabled (MediaPipe not installed)\n")
                    self.config.ENABLE_VISION = False
            
            # 4. VideoRenderer
            imagemagick_path = None
            if os.name != 'nt':  # Non-Windows
                imagemagick_path = "/usr/bin/convert"  # Linux standard path
            
            self.video_renderer = VideoRenderer(
                imagemagick_path=imagemagick_path,
                font="Arial-Bold",
                fontsize=80,
                color="yellow"
            )
            print()
            
            print("✅ All components initialized!\n")
            return True
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    def run_pipeline(self):
        """เรียกใช้ pipeline แยกตามลำดับ"""
        print("="*60)
        print("PIPELINE EXECUTION\n")
        print("-" * 60)
        
        # Step 1: Extract & Transcribe
        if not self._step_1_audio_processing():
            return False
        
        # Step 2: Content Analysis
        if not self._step_2_content_analysis():
            return False
        
        # Step 3: Vision Processing
        if self.config.ENABLE_VISION and not self._step_3_vision_processing():
            print("⚠️  Vision processing skipped\n")
        
        # Step 4: Render Output
        if self.config.RENDER_OUTPUT and not self._step_4_rendering():
            return False
        
        return True
    
    def _step_1_audio_processing(self):
        """Step 1: Audio Extraction & Transcription"""
        print("\n📋 STEP 1: AUDIO PROCESSING")
        print("-" * 60)
        
        try:
            # ตรวจสอบไฟล์อินพุต
            if not os.path.exists(self.config.INPUT_VIDEO):
                print(f"❌ ไฟล์ไม่พบ: {self.config.INPUT_VIDEO}")
                return False
            
            # แปลงเป็น WAV
            audio_path = self.audio_engine.convert_to_wav(
                self.config.INPUT_VIDEO,
                self.config.TEMP_AUDIO
            )
            
            # แกะเสียง
            start_time = time.time()
            self.segments, self.info = self.audio_engine.transcribe(
                audio_path,
                word_timestamps=True
            )
            elapsed = time.time() - start_time
            
            print(f"\n📊 Transcription Summary:")
            print(f"   Language: {self.info.language}")
            print(f"   Duration: {elapsed:.2f}s")
            print(f"   Segments: {len(self.segments)}")
            
            # แสดง preview (first 3 segments)
            print(f"\n📝 Preview (first 3 segments):")
            for i, seg in enumerate(self.segments[:3]):
                print(f"   [{seg.start:.2f}s - {seg.end:.2f}s] {seg.text[:50]}...")
            
            # สะอาดไฟล์ชั่วคราว
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Error in audio processing: {e}")
            return False
    
    def _step_2_content_analysis(self):
        """Step 2: Content Intelligence Analysis"""
        print("\n📋 STEP 2: CONTENT ANALYSIS")
        print("-" * 60)
        
        try:
            if not self.segments:
                print("❌ No transcript data from Step 1")
                return False
            
            # รวม transcript
            full_transcript = " ".join([seg.text for seg in self.segments])
            
            # วิเคราะห์
            self.moments = self.content_intelligence.find_best_moments(
                transcript_text=full_transcript,
                num_moments=self.config.CONTENT_ANALYSIS_NUM
            )
            
            print(f"\n📊 Analysis Results:")
            print(f"   Found {len(self.moments)} viral moments\n")
            
            for i, moment in enumerate(self.moments, 1):
                print(f"   Moment {i}:")
                print(f"      Time: {moment.get('start'):.2f}s - {moment.get('end'):.2f}s")
                print(f"      Headline: {moment.get('headline', 'N/A')}")
                print(f"      Viral Score: {moment.get('viral_score', 0)}/100")
                if 'reason' in moment:
                    print(f"      Reason: {moment.get('reason')[:60]}...")
                print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error in content analysis: {e}")
            return False
    
    def _step_3_vision_processing(self):
        """Step 3: Vision Engine Processing"""
        print("\n📋 STEP 3: VISION PROCESSING")
        print("-" * 60)
        
        try:
            if not self.vision_engine:
                print("⚠️  Vision Engine not available")
                return False
            
            self.vision_data = self.vision_engine.process_video_samples(
                self.config.INPUT_VIDEO,
                sample_frames=5
            )
            
            print(f"\n📊 Vision Analysis Results:")
            print(f"   Face detected in: {self.vision_data['detected_count']} / {len(self.vision_data['face_positions'])} frames")
            print(f"   Detection rate: {100 * self.vision_data['detected_count'] / max(1, len(self.vision_data['face_positions'])):.1f}%")
            
            return True
            
        except Exception as e:
            print(f"⚠️  Vision processing error: {e}")
            return False
    
    def _step_4_rendering(self):
        """Step 4: Video Rendering"""
        print("\n📋 STEP 4: VIDEO RENDERING")
        print("-" * 60)
        
        try:
            # เตรียม subtitles จาก segments
            word_subtitles = []
            for segment in self.segments:
                if hasattr(segment, 'words'):
                    for word in segment.words:
                        word_subtitles.append({
                            "word": word.word.strip(),
                            "start": word.start,
                            "end": word.end
                        })
            
            # Render main output
            print(f"\n🎬 Rendering main output. It may take a while...")
            self.video_renderer.render_viral_clip(
                input_video=self.config.INPUT_VIDEO,
                output_name=self.config.OUTPUT_VIDEO,
                moment_segments=self.moments or [],
                word_subtitles=word_subtitles if word_subtitles else None,
                fps=self.config.OUTPUT_FPS,
                codec=self.config.VIDEO_CODEC,
                preset=self.config.PRESET
            )
            
            # Render 9:16 format (optional)
            if self.config.ENABLE_9_16_FORMAT:
                print(f"\n🎬 Rendering 9:16 format...")
                self.video_renderer.render_9_16_format(
                    input_video=self.config.INPUT_VIDEO,
                    output_name=self.config.OUTPUT_VIDEO_9_16,
                    face_tracking_data=self.vision_data,
                    word_subtitles=word_subtitles if word_subtitles else None,
                    fps=self.config.OUTPUT_FPS
                )
            
            return True
            
        except Exception as e:
            print(f"❌ Rendering error: {e}")
            return False
    
    def save_report(self):
        """บันทึกรายงานวิเคราะห์เป็น JSON"""
        report = {
            "input_video": self.config.INPUT_VIDEO,
            "transcription": {
                "language": self.info.language if self.info else "unknown",
                "segments_count": len(self.segments) if self.segments else 0,
            },
            "moments": self.moments or [],
            "vision": self.vision_data or {},
            "outputs": {
                "main_video": self.config.OUTPUT_VIDEO,
                "vertical_video": self.config.OUTPUT_VIDEO_9_16 if self.config.ENABLE_9_16_FORMAT else None,
            }
        }
        
        with open(self.config.OUTPUT_REPORT, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Report saved: {self.config.OUTPUT_REPORT}")
    
    def run(self):
        """เรียกใช้ pipeline ทั้งหมด"""
        start_time = time.time()
        
        # Initialize
        if not self.initialize_components():
            print("\n❌ Failed to initialize components")
            return False
        
        # Run pipeline
        if not self.run_pipeline():
            print("\n❌ Pipeline failed")
            return False
        
        # Save report
        self.save_report()
        
        # Summary
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETE!".center(60))
        print("="*60)
        print(f"\nTotal time: {elapsed:.1f}s")
        print(f"\n📁 Outputs:")
        print(f"   - {self.config.OUTPUT_VIDEO}")
        if self.config.ENABLE_9_16_FORMAT:
            print(f"   - {self.config.OUTPUT_VIDEO_9_16}")
        print(f"   - {self.config.OUTPUT_REPORT}")
        print()
        
        return True


# ==========================================
# 🎯 MAIN ENTRY POINT
# ==========================================
def main():
    parser = argparse.ArgumentParser(
        description="🎬 Viral Video Auto-Generator (รองรับ YouTube!)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_integrated.py --input myvideo.mp4 --output result.mp4
  python main_integrated.py --input "https://www.youtube.com/watch?v=..." --output result.mp4
  python main_integrated.py --input test.mp4 --no-vision
  python main_integrated.py --preset fast --device cpu
        """
    )
    
    parser.add_argument("--input", default="test.mp4", help="Input video file หรือ YouTube URL")
    parser.add_argument("--output", default="output_viral.mp4", help="Output video file")
    parser.add_argument("--model", default="large-v3-turbo", help="Whisper model size")
    parser.add_argument("--device", default="cuda", help="Device: cuda or cpu")
    parser.add_argument("--preset", default="medium", help="Render preset: ultrafast, fast, medium, slow")
    parser.add_argument("--no-vision", action="store_true", help="Disable Vision component")
    parser.add_argument("--no-9-16", action="store_true", help="Disable 9:16 format")
    parser.add_argument("--no-render", action="store_true", help="Skip rendering (analysis only)")
    
    args = parser.parse_args()
    
    # ตรวจสอบและดาวน์โหลด YouTube video ถ้าต้อง
    input_file = args.input
    
    if is_youtube_url(args.input):
        print("\n🎥 ตรวจพบ YouTube URL - กำลังดาวน์โหลด...")
        downloaded_file = download_youtube_video(args.input, "youtube_download.mp4")
        
        if downloaded_file:
            input_file = downloaded_file
            print(f"✅ ใช้ไฟล์ที่ดาวน์โหลด: {input_file}\n")
        else:
            print("❌ ดาวน์โหลด YouTube ล้มเหลว")
            return 1
    
    # Apply arguments to config
    config = Config()
    config.INPUT_VIDEO = input_file
    config.OUTPUT_VIDEO = args.output
    config.WHISPER_MODEL = args.model
    config.DEVICE = args.device
    config.PRESET = args.preset
    config.ENABLE_VISION = not args.no_vision
    config.ENABLE_9_16_FORMAT = not args.no_9_16
    config.RENDER_OUTPUT = not args.no_render
    
    # Run generator
    generator = ViralVideoGenerator(config)
    success = generator.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
