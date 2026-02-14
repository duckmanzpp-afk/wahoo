# 🎬 VIRAL VIDEO AUTO-GENERATOR

**ระบบอัตโนมัติสำหรับสร้างวิดีโอไวรัลด้วย AI**

## 🎯 ความสามารถหลัก

✅ **แกะเสียง** - แปลงวิดีโอเป็นข้อความ (Word-level Timestamps)  
✅ **วิเคราะห์ AI** - หาช่วง "Viral Moments" ที่น่าสนใจ  
✅ **ตรวจจับใบหน้า** - Auto-reframe วิดีโอเป็นแนวตั้ง (9:16)  
✅ **เรนเดอร์ขั้นสูง** - ใส่ซับไตเติลเด้งๆ พร้อม animations  

---

## 🏗️ สถาปัตยกรรม 4 Components

```
INPUT VIDEO (test.mp4)
        ↓
┌───────────────────────────────────────┐
│ 1️⃣ AUDIO ENGINE (Whisper)            │
│    - แกะเสียง → ข้อความ              │
│    - Word-level timestamps           │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│ 2️⃣ CONTENT INTELLIGENCE (GPT)        │
│    - วิเคราะห์ transcript            │
│    - หา viral moments                │
│    - ให้ viral scores                │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│ 3️⃣ VISION ENGINE (MediaPipe)         │
│    - ตรวจจับใบหน้า                   │
│    - คำนวณ crop window 9:16          │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│ 4️⃣ VIDEO RENDERER (MoviePy)          │
│    - ตัด/resize วิดีโอ               │
│    - เพิ่มซับไตเติล                  │
│    - Render output files             │
└───────────────────────────────────────┘
        ↓
OUTPUT: viral_output.mp4 + viral_9_16.mp4
```

---

## 📋 ไฟล์ระหว่างการทำงาน

| ไฟล์ | ฟังก์ชัน | คำอธิบาย |
|-----|--------|--------|
| `main_integrated.py` | Orchestrator | เรียกใช้ทั้ง 4 components |
| `audio_engine.py` | Component 1 | FFmpeg + Whisper |
| `content_intelligence.py` | Component 2 | OpenAI GPT API |
| `vision_engine.py` | Component 3 | MediaPipe face detection |
| `video_renderer.py` | Component 4 | MoviePy rendering |

---

## ⚡ Quick Start

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. ใส่ไฟล์วิดีโอ
```bash
# Copy ไฟล์ของคุณเข้า workspace
cp /path/to/your/video.mp4 c:\Webpedpok\test.mp4
```

### 3. ตั้งค่า API Key (optional)
```bash
# Windows PowerShell:
$env:OPENAI_API_KEY = "your-api-key-here"

# Linux/macOS:
export OPENAI_API_KEY="your-api-key-here"
```

### 4. เรียกใช้งาน
```bash
# แบบง่าย (ใช้ default settings)
python main_integrated.py

# แบบกำหนดเอง
python main_integrated.py --input myvideo.mp4 --preset fast --device cuda
```

### 5. รอจนเสร็จ
```
OUTPUT:
  ✅ output_viral.mp4 (กับซับไตเติล)
  ✅ output_viral_9_16.mp4 (แนวตั้ง)
  ✅ analysis_report.json (รายงาน)
```

---

## 🎛️ Command-Line Options

```bash
python main_integrated.py [OPTIONS]

Options:
  --input FILE              Input video file (default: test.mp4)
  --output FILE             Output video file (default: output_viral.mp4)
  --model {tiny,base,small,medium,large,large-v3-turbo}
                           Whisper model size (default: large-v3-turbo)
  --device {cuda,cpu}      Processing device (default: cuda)
  --preset {ultrafast,fast,medium,slow}
                           Render quality (default: medium)
  --no-vision              Disable Vision component
  --no-9-16                Disable 9:16 format output
  --no-render              Analysis only (skip rendering)

Examples:
  python main_integrated.py --input myvideo.mp4 --preset fast
  python main_integrated.py --model small --device cpu
  python main_integrated.py --no-vision --no-9-16
```

---

## 📊 Output Files

### 1. `output_viral.mp4`
- วิดีโอเต็มความสูงต้นฉบับ
- มี subtitles ตามข้อความ
- Format: 16:9 (landscape)

### 2. `output_viral_9_16.mp4`
- วิดีโอแนวตั้ง (TikTok-style)
- Crop ตามตำแหน่งใบหน้า
- Format: 9:16 (portrait)

### 3. `analysis_report.json`
```json
{
  "input_video": "test.mp4",
  "transcription": {
    "language": "th",
    "segments_count": 42
  },
  "moments": [
    {
      "start": 15.5,
      "end": 45.0,
      "headline": "ช่วงที่ตลกที่สุด",
      "viral_score": 92,
      "reason": "ตลกสนุก relatable"
    },
    ...
  ],
  "outputs": {
    "main_video": "output_viral.mp4",
    "vertical_video": "output_viral_9_16.mp4"
  }
}
```

---

## 🔧 Configuration

### ปรับแต่งในไฟล์ `main_integrated.py` (Class: Config)

```python
class Config:
    # Input/Output
    INPUT_VIDEO = "test.mp4"
    OUTPUT_VIDEO = "output_viral.mp4"
    
    # Model Settings
    WHISPER_MODEL = "large-v3-turbo"  # ใหญ่แม่นยำ (ช้า)
                                       # หรือ "base" (เร็ว)
    DEVICE = "cuda"                   # cuda หรือ cpu
    
    # Components
    ENABLE_VISION = True              # auto-reframe
    ENABLE_9_16_FORMAT = True         # สร้างแนวตั้ง
    RENDER_OUTPUT = True              # render output
    
    # Render Quality
    OUTPUT_FPS = 30
    PRESET = "medium"  # ultrafast < fast < medium < slow
```

---

## ⚠️ Troubleshooting

### 1. "FFmpeg not found"
```bash
# Windows:
choco install ffmpeg

# macOS:
brew install ffmpeg

# Linux:
sudo apt-get install ffmpeg
```

### 2. "CUDA not available" (wants GPU acceleration)
```bash
# Check CUDA:
python -c "import torch; print(torch.cuda.is_available())"

# If False, install PyTorch with CUDA:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. "OpenAI API error"
- ตรวจสอบ API key: `echo $OPENAI_API_KEY`
- หรือ run without API (ใช้ Mock analysis): ปล่อยไว้ว่าง

### 4. "Out of memory"
- ลดขนาด model: `--model small`
- ใช้ CPU: `--device cpu`
- ลดความจริง/ความยาววิดีโอ

### 5. Rendering takes too long
- ใช้ fast preset: `--preset fast`
- ลดความหลากหลายของข้อมูล
- ปิด Vision: `--no-vision`

---

## 🎓 Understanding the Components

### 1️⃣ AudioEngine
```python
from audio_engine import AudioEngine

engine = AudioEngine(model_size="large-v3-turbo", device="cuda")
audio_path = engine.convert_to_wav("video.mp4")
segments, info = engine.transcribe(audio_path, word_timestamps=True)

# segments = [
#   {id: 0, seek: 0, start: 0.5, end: 5.2, text: "สวัสดี...", 
#    words: [{word: "สวัสดี", start: 0.5, end: 1.2}, ...]},
#   ...
# ]
```

### 2️⃣ ContentIntelligence
```python
from content_intelligence import ContentIntelligence

ci = ContentIntelligence(api_key="sk-...")
moments = ci.find_best_moments(full_transcript, num_moments=3)

# moments = [
#   {start: 15.5, end: 45.0, headline: "...", viral_score: 92, reason: "..."},
#   ...
# ]
```

### 3️⃣ VisionEngine
```python
from vision_engine import VisionEngine

vision = VisionEngine()
x_center, y_center, detected = vision.get_face_center(frame)

# Auto-crop 9:16 format
cropped_frame = vision.crop_frame_9_16(frame, x_center, y_center)

# Analyze whole video
analysis = vision.process_video_samples("video.mp4", sample_frames=5)
```

### 4️⃣ VideoRenderer
```python
from video_renderer import VideoRenderer

renderer = VideoRenderer(fontsize=80, color="yellow")

# Render with subtitles
renderer.render_viral_clip(
    input_video="video.mp4",
    output_name="output.mp4",
    moment_segments=moments,
    word_subtitles=word_list
)

# Render 9:16 format
renderer.render_9_16_format(
    input_video="video.mp4",
    output_name="output_9_16.mp4",
    face_tracking_data=vision_analysis
)
```

---

## 📈 Performance

| Model Size | Speed | Accuracy | VRAM | Best For |
|-----------|-------|----------|------|----------|
| tiny | ⚡⚡⚡⚡ | 60% | 1GB | Quick test |
| base | ⚡⚡⚡ | 75% | 2GB | Fast preview |
| small | ⚡⚡ | 85% | 3GB | Balanced |
| medium | ⚡ | 92% | 5GB | Good quality |
| large | 🐢 | 97% | 10GB | Best quality |
| large-v3-turbo | ⚡ | 95% | 8GB | **Recommended** |

---

## 🚀 Advanced Usage

### Process Multiple Videos
```bash
# Batch processing
for video in *.mp4; do
  python main_integrated.py --input "$video" --output "viral_${video}"
  echo "✅ Processed $video"
done
```

### Analysis Only (No Rendering)
```bash
python main_integrated.py --no-render
# Output: analysis_report.json only
```

### Custom Components
```python
from main_integrated import ViralVideoGenerator, Config

config = Config()
config.INPUT_VIDEO = "custom.mp4"
config.WHISPER_MODEL = "small"
config.PRESET = "ultrafast"

generator = ViralVideoGenerator(config)
generator.run()
```

---

## 📝 License & Attribution

- **Whisper**: OpenAI
- **MoviePy**: Zulko
- **MediaPipe**: Google
- **OpenAI API**: OpenAI

---

## 🤝 Support & Issues

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting-) section
2. Verify all dependencies: `pip list`
3. Check logs in console output
4. Try with `--device cpu` and `--preset fast`

---

## 📚 Next Steps

1. **Fine-tune prompts** in `content_intelligence.py` for better moment detection
2. **Customize subtitles** style (color, font, position) in `video_renderer.py`
3. **Add effects** using MoviePy's fx library
4. **Integrate other LLMs** (Llama, Claude, etc.)
5. **Deploy as API** using FastAPI/Flask

Happy rendering! 🎬✨
