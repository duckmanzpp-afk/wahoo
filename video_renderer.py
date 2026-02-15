<<<<<<< HEAD
=======
<<<<<<< HEAD
# -*- coding: utf-8 -*-
import os
from typing import List, Dict, Tuple, Optional

# Set FFmpeg path
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
if os.path.exists(FFMPEG_PATH):
    os.environ['FFMPEG_BINARY'] = FFMPEG_PATH

# Suppress imageio ffmpeg download
import imageio
imageio.plugins.ffmpeg.FFMPEG_BINARY = FFMPEG_PATH

try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, vfx
except (ImportError, RuntimeError):
    # Fallback for moviepy 2.x
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.VideoClip import TextClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    import moviepy.video.fx as vfx

try:
    from moviepy.config import change_settings
    if os.path.exists(FFMPEG_PATH):
        change_settings({"FFMPEG_BINARY": FFMPEG_PATH})
except ImportError:
    def change_settings(d): pass  # Dummy function
=======
>>>>>>> SIJN
import os
from typing import List, Dict, Tuple, Optional
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, vfx
from moviepy.config import change_settings
<<<<<<< HEAD
=======
>>>>>>> aa72dfb (Initial project setup: WebPedPok YouTube video analysis and content intelligence system)
>>>>>>> SIJN

class VideoRenderer:
    """Component 4: Video Rendering Engine (MoviePy)
    
    ฟังก์ชัน: เรนเดอร์วิดีโอขั้นสุดท้าย โดยใส่:
    - ซับไตเติลเด้งๆ (Bouncy subtitles)
    - ตัด segment ที่ AI เลือก
    - Auto-reframe เป็น 9:16 ถ้ามีข้อมูล
    """
    
    def __init__(
        self,
        imagemagick_path: Optional[str] = None,
        font: str = "Arial-Bold",
        fontsize: int = 80,
        color: str = "yellow",
        stroke_color: str = "black",
        stroke_width: int = 2
    ):
        """
        Args:
            imagemagick_path: เส้นทาง ImageMagick (สำหรับ rendering text บน macOS)
            font: Font ที่ใช้ (เช่น Arial-Bold, Courier)
            fontsize: ขนาดฟอนต์
            color: สีข้อความ (yellow, white, etc.)
            stroke_color: สีขอบข้อความ
            stroke_width: ความหนาของขอบ
        """
        # ตั้งค่า ImageMagick ถ้าระบุ (สำหรับ macOS/Linux)
        if imagemagick_path and os.path.exists(imagemagick_path):
            change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
            print(f"🖼️  ImageMagick: {imagemagick_path}")
        
        self.font = font
        self.fontsize = fontsize
        self.color = color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        
        print(f"🔧 กำลังสร้าง VideoRenderer...")
        print(f"   - Font: {self.font}")
        print(f"   - Size: {self.fontsize}px")
        print(f"   - Color: {self.color}")
        print(f"   ✅ MoviePy Ready")
    
    def create_subtitle_clip(
        self,
        text: str,
        start_time: float,
        duration: float,
        position: Tuple[str, str] = ('center', 'bottom'),
        with_animation: bool = True
    ) -> TextClip:
        """สร้าง subtitle clip เดี่ยว พร้อม animation
        
        Args:
            text: ข้อความที่แสดง
            start_time: เวลาเริ่ม (วินาที)
            duration: ระยะเวลา (วินาที)
            position: ตำแหน่ง ('center', 'bottom') หรือ ('left', 'top') ฯลฯ
            with_animation: ใช้ animation หรือไม่
            
        Returns:
            TextClip: subtitle clip ที่พร้อมใช้
        """
        # สร้าง TextClip
        txt_clip = TextClip(
            text,
            fontsize=self.fontsize,
            color=self.color,
            font=self.font,
            stroke_color=self.stroke_color,
            stroke_width=self.stroke_width,
            method='label'
        )
        
        # ตั้งเวลา
        txt_clip = txt_clip.set_start(start_time).set_duration(max(0.1, duration))
        
        # ตั้งตำแหน่ง
        txt_clip = txt_clip.set_position(position)
        
        # เพิ่ม animation ถ้ากำหนด
        if with_animation:
            # ตัวอย่าง: Scale up แล้ว down (bounce effect)
            txt_clip = txt_clip.fx(vfx.grow, duration=duration * 0.1)
        
        return txt_clip
    
    def render_viral_clip(
        self,
        input_video: str,
        output_name: str,
        moment_segments: List[Dict],
        word_subtitles: Optional[List[Dict]] = None,
        fps: int = 30,
        codec: str = "libx264",
        preset: str = "medium"
    ) -> str:
        """เรนเดอร์วิดีโอ viral clip สุดท้าย
        
        Args:
            input_video: ไฟล์วิดีโออินพุต
            output_name: ชื่อไฟล์เอาต์พุต
            moment_segments: รายการ moment segments (start, end, headline, etc.)
            word_subtitles: subtitle ทีละคำ (optional) - format: 
                            [{"word": "...", "start": 10.5, "end": 11.0}, ...]
            fps: Frames per second
            codec: video codec (libx264, libx265, etc.)
            preset: quality preset (ultrafast, fast, medium, slow)
            
        Returns:
            str: เส้นทางไฟล์เอาต์พุต
        """
        print(f"🎬 5. กำลังเรนเดอร์วิดีโอออกมา...")
        print(f"   Input: {input_video}")
        print(f"   Output: {output_name}")
        
        # โหลดวิดีโอ
        video = VideoFileClip(input_video)
        original_fps = video.fps
        original_duration = video.duration
        
        print(f"   - Duration: {original_duration:.1f}s")
        print(f"   - FPS: {original_fps:.1f}")
        print(f"   - Codec: {codec}")
        
        # เก็บ list ของ text clips
        text_clips = []
        
        # ถ้าต้องการตัดตามช่วง moment ที่ AI เลือก
        # ตอนนี้จะข้าม (ใช้วิดีโอทั้งหมด)
        
        # เพิ่ม word subtitles
        if word_subtitles:
            print(f"   📝 เพิ่ม {len(word_subtitles)} subtitle...")
            for subtitle_data in word_subtitles:
                word = subtitle_data.get("word", "")
                start = subtitle_data.get("start", 0)
                end = subtitle_data.get("end", 0)
                duration = max(0.1, end - start)
                
                try:
                    txt_clip = self.create_subtitle_clip(
                        text=word.upper(),
                        start_time=start,
                        duration=duration,
                        position=('center', 'center'),
                        with_animation=True
                    )
                    text_clips.append(txt_clip)
                except Exception as e:
                    print(f"     ⚠️  Skip word '{word}': {e}")
                    continue
        else:
            # ถ้าไม่มี word subtitles ให้แสดง moment headlines
            print(f"   📝 เพิ่ม {len(moment_segments)} moment headlines...")
            for moment in moment_segments:
                headline = moment.get("headline", "Moment")
                viral_score = moment.get("viral_score", 0)
                
                # ใช้ moment time ถ้ามี, ถ้าไม่มีให้ประมาณ
                start = moment.get("start", 10.0)
                end = moment.get("end", start + 10.0)
                duration = max(0.5, end - start)
                
                # จำกัดให้อยู่ในช่วงวิดีโอ
                if start < original_duration:
                    try:
                        txt_clip = self.create_subtitle_clip(
                            text=f"{headline}\n(Score: {viral_score}/100)",
                            start_time=start,
                            duration=min(duration, original_duration - start),
                            position=('center', 'bottom'),
                            with_animation=True
                        )
                        text_clips.append(txt_clip)
                    except Exception as e:
                        print(f"     ⚠️  Skip moment: {e}")
                        continue
        
        # ประกอบ final video
        if text_clips:
            final_video = CompositeVideoClip([video] + text_clips)
        else:
            final_video = video
        
        # เรนเดอร์
        print(f"   ⏳ Rendering... (อาจใช้เวลา)")
        try:
            final_video.write_videofile(
<<<<<<< HEAD
=======
<<<<<<< HEAD
    output_name,
    fps=fps,
    codec=codec,
    audio_codec="aac",
    preset=preset
)


=======
>>>>>>> SIJN
                output_name,
                fps=fps,
                codec=codec,
                audio_codec="aac",
                preset=preset,
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
                verbose=False,
                logger=None  # ซ่อน logging ของ MoviePy
            )
<<<<<<< HEAD
=======
>>>>>>> aa72dfb (Initial project setup: WebPedPok YouTube video analysis and content intelligence system)
>>>>>>> SIJN
            
            print(f"   ✅ Render Complete!")
            return output_name
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
        finally:
            video.close()
            if hasattr(final_video, 'close'):
                final_video.close()
    
    def render_9_16_format(
        self,
        input_video: str,
        output_name: str,
        face_tracking_data: Optional[Dict] = None,
        word_subtitles: Optional[List[Dict]] = None,
        fps: int = 30
    ) -> str:
        """เรนเดอร์วิดีโอเป็นฟอร์แมต 9:16 (Vertical TikTok-style)
        
        Args:
            input_video: ไฟล์วิดีโออินพุต
            output_name: ชื่อไฟล์เอาต์พุต
            face_tracking_data: ข้อมูล face tracking จาก VisionEngine
            word_subtitles: subtitle details
            fps: Frames per second
            
        Returns:
            str: เส้นทางไฟล์เอาต์พุต
        """
        print(f"🎬 5. กำลังเรนเดอร์วิดีโอ 9:16 format...")
        print(f"   Output: {output_name}")
        
        # โหลดวิดีโอ
        video = VideoFileClip(input_video)
        orig_w, orig_h = video.size
        
        # คำนวณขนาด 9:16 frame
        # ถ้าใช้ height ต้นฉบับ
        target_width = int(orig_h * 9 / 16)
        target_height = orig_h
        
        if target_width > orig_w:
            # ถ้าเกิน ใช้ width ต้นฉบับ
            target_width = orig_w
            target_height = int(orig_w * 16 / 9)
        
        print(f"   - Source: {orig_w}x{orig_h}")
        print(f"   - Target: {target_width}x{target_height}")
        
        # ถ้ามีข้อมูล face tracking ให้ crop ตามตำแหน่งใบหน้า
        # ตอนนี้จะข้าม - ใช้การ crop แบบอย่างง่าย (center crop)
        
        # Center crop
        crop_x = (orig_w - target_width) // 2
        crop_y = 0  # Top aligned
        
        cropped = video.crop(
            x1=crop_x,
            y1=crop_y,
            x2=crop_x + target_width,
            y2=crop_y + target_height
        )
        
        # เพิ่ม subtitle ถ้ามี
        text_clips = []
        if word_subtitles:
            print(f"   📝 เพิ่ม {len(word_subtitles)} subtitle...")
            for subtitle_data in word_subtitles[:100]:  # จำกัด 100 subtitle
                word = subtitle_data.get("word", "")
                start = subtitle_data.get("start", 0)
                end = subtitle_data.get("end", 0)
                duration = max(0.1, end - start)
                
                try:
                    txt_clip = self.create_subtitle_clip(
                        text=word.upper(),
                        start_time=start,
                        duration=duration,
                        position=('center', 'center')
                    )
                    text_clips.append(txt_clip)
                except:
                    continue
        
        # ประกอบ
        if text_clips:
            final_video = CompositeVideoClip([cropped] + text_clips)
        else:
            final_video = cropped
        
        # เรนเดอร์
        print(f"   ⏳ Rendering...")
        try:
            final_video.write_videofile(
                output_name,
                fps=fps,
                codec="libx264",
                audio_codec="aac",
                preset="fast",
                temp_audiofile="temp-audio-vertical.m4a",
                remove_temp=True,
<<<<<<< HEAD
                verbose=False,
                logger=None
=======
<<<<<<< HEAD
                verbose=False
=======
                verbose=False,
                logger=None
>>>>>>> aa72dfb (Initial project setup: WebPedPok YouTube video analysis and content intelligence system)
>>>>>>> SIJN
            )
            
            print(f"   ✅ 9:16 Render Complete!")
            return output_name
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
        finally:
            video.close()
            if hasattr(final_video, 'close'):
                final_video.close()
