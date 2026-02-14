# 🎬 SETUP & INSTALLATION GUIDE

## 📋 Quick Summary

You now have a **4-Component Viral Video Auto-Generator** system installed. Here's what was created:

```
c:\Webpedpok\
├── 🎵 audio_engine.py              [Component 1] Speech-to-text (Whisper)
├── 🧠 content_intelligence.py      [Component 2] AI analysis (GPT)  
├── 👁️  vision_engine.py            [Component 3] Face detection (MediaPipe)
├── 🎬 video_renderer.py            [Component 4] Video rendering (MoviePy)
├── 📍 main_integrated.py           [Orchestrator] Runs all 4 components
├── 🧪 examples.py                  [Examples] Sample usage patterns
├── ✅ check_dependencies.py        [Checker] Verify installation
├── 📖 README.md                    [Documentation] Full guide
├── 📦 requirements.txt             [Dependencies] Python packages
├── ⚙️  .env.example                [Config template] API keys
└── ❌ main.py                      [Old version - can delete]
```

---

## ⚡ STEP 1: Install Python Dependencies

```bash
# Navigate to workspace
cd c:\Webpedpok

# Install all required packages
pip install -r requirements.txt
```

### ✅ Verify Installation
```bash
# Check all dependencies
python check_dependencies.py

# Expected output:
# ✅ faster_whisper              INSTALLED
# ✅ torch                       INSTALLED
# ✅ openai                      INSTALLED
# ✅ opencv-python              INSTALLED
# ✅ moviepy                     INSTALLED
# ... etc
```

---

## ⚙️ STEP 2: Configure API Keys (Optional but Recommended)

### Get OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key

### Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

**Windows (Permanent - .env file):**
```bash
# Copy example:
copy .env.example .env

# Edit .env:
OPENAI_API_KEY=sk-your-api-key-here
```

**Linux/macOS:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

---

## 🚀 STEP 3: Prepare Your Video

```bash
# Place your video in workspace
# Renaming to test.mp4 (or change in config)
cp /path/to/your/video.mp4 c:\Webpedpok\test.mp4
```

---

## ▶️ STEP 4: Run the System

### Option A: Quick Start (Simplest)
```bash
python main_integrated.py
```

This will:
- Accept default settings
- Use GPU if available, CPU otherwise
- Process test.mp4
- Output viral_output.mp4 + viral_9_16.mp4

### Option B: With Custom Settings
```bash
# Custom input/output files
python main_integrated.py --input myvideo.mp4 --output result.mp4

# Faster processing (small model + fast preset)
python main_integrated.py --model small --preset fast

# CPU-only mode (no GPU needed)
python main_integrated.py --device cpu

# Analysis only (skip rendering)
python main_integrated.py --no-render
```

### Option C: Interactive Examples
```bash
python examples.py

# Choose from:
# 1. Basic usage
# 2. Custom settings
# 3. Analysis only
# 4. Fast mode
# 5. CPU mode
# 6. Batch processing
# 7. Advanced customization
```

---

## 📁 Output Files

After running, you'll get:

```
📁 Output Files Created:
├── output_viral.mp4          [Main output] Full video with subtitles
├── output_viral_9_16.mp4     [Vertical] TikTok/Instagram format
└── analysis_report.json      [Report] Viral moments analysis
```

---

## 🧩 Component Overview

### 1️⃣ AudioEngine (Whisper)
```python
from audio_engine import AudioEngine

engine = AudioEngine(model_size="large-v3-turbo")
audio = engine.convert_to_wav("video.mp4")
segments, info = engine.transcribe(audio)
```

**Use Cases:**
- Extract text from video
- Get word-level timestamps
- Support 99+ languages

**Performance:**
- tiny: ⚡⚡⚡⚡ (fast, less accurate)
- large-v3-turbo: ⚡ (recommended, balanced)
- large: 🐢 (slowest, most accurate)

---

### 2️⃣ ContentIntelligence (GPT)
```python
from content_intelligence import ContentIntelligence

ci = ContentIntelligence(api_key="sk-...")
moments = ci.find_best_moments(transcript)
# Returns: [{start: 10, end: 45, headline: "...", viral_score: 90}, ...]
```

**Features:**
- Find viral moments
- Generate headlines
- Assign engagement scores
- Works with or without API key (mock analysis)

---

### 3️⃣ VisionEngine (MediaPipe)
```python
from vision_engine import VisionEngine

vision = VisionEngine()
x, y, detected = vision.get_face_center(frame)
cropped = vision.crop_frame_9_16(frame, x, y)
```

**Features:**
- Detect faces in video frames
- Auto-crop to 9:16 (vertical) format
- Keep face centered
- Report detection statistics

---

### 4️⃣ VideoRenderer (MoviePy)
```python
from video_renderer import VideoRenderer

renderer = VideoRenderer()
renderer.render_viral_clip(
    input_video="video.mp4",
    output_name="output.mp4",
    moment_segments=moments,
    word_subtitles=words
)
```

**Features:**
- Render with subtitles
- Add animations/effects
- Support 9:16 format
- Configurable quality/speed

---

## 🎛️ Configuration Reference

### main_integrated.py Config Class

```python
class Config:
    # Input/Output Files
    INPUT_VIDEO = "test.mp4"
    OUTPUT_VIDEO = "output_viral.mp4"
    OUTPUT_VIDEO_9_16 = "output_viral_9_16.mp4"
    OUTPUT_REPORT = "analysis_report.json"
    
    # Audio Engine Settings
    WHISPER_MODEL = "large-v3-turbo"  # tiny, base, small, medium, large, large-v3-turbo
    DEVICE = "cuda"                   # cuda or cpu
    
    # Content Intelligence
    OPENAI_API_KEY = None  # Auto-loads from env variable
    CONTENT_ANALYSIS_NUM = 3           # Number of viral moments to find
    
    # Vision Engine
    FACE_CONFIDENCE = 0.5              # 0.0-1.0, higher = stricter
    
    # Video Rendering
    OUTPUT_FPS = 30                    # Frames per second
    VIDEO_CODEC = "libx264"            # Video codec
    PRESET = "medium"                  # ultrafast, fast, medium, slow
    
    # Feature Flags
    ENABLE_VISION = True
    ENABLE_9_16_FORMAT = True
    RENDER_OUTPUT = True
```

---

## ⚠️ Common Issues & Solutions

### "ModuleNotFoundError: No module named 'faster_whisper'"
```bash
pip install faster-whisper
```

### "No such file or directory: 'ffmpeg'"
**Windows:** 
```bash
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### "CUDA out of memory"
```bash
# Use smaller model
python main_integrated.py --model small

# OR use CPU
python main_integrated.py --device cpu
```

### "OpenAI API error"
```bash
# Check if API key is set
echo %OPENAI_API_KEY%  # Windows
echo $OPENAI_API_KEY   # Linux/macOS

# If empty, set it:
$env:OPENAI_API_KEY = "your-key"
```

### "Process takes too long"
```bash
# Use faster settings
python main_integrated.py --model base --preset fast --device cuda
```

---

## 📊 System Requirements

| Component | Minimum | Recommended | High-End |
|-----------|---------|-------------|----------|
| **CPU** | i5 4-core | i7 8-core | Ryzen 9 |
| **RAM** | 8GB | 16GB | 32GB |
| **GPU** | None | RTX 2060 | RTX 3090+ |
| **Storage** | 10GB | 20GB | 50GB |
| **Network** | Optional | Needed (API) | Needed (Models) |

---

## 🔧 Advanced Tips

### 1. Batch Process Multiple Videos
```python
import glob
from main_integrated import ViralVideoGenerator, Config

for video in glob.glob("*.mp4"):
    config = Config()
    config.INPUT_VIDEO = video
    config.OUTPUT_VIDEO = f"viral_{video}"
    generator = ViralVideoGenerator(config)
    generator.run()
```

### 2. Custom Prompt for Content Analysis
Edit `content_intelligence.py` line ~90:
```python
prompt = f"""
    [Customize this prompt for your needs]
    Analyze: {transcript_text}
"""
```

### 3. Custom Subtitle Styling
Edit `video_renderer.py`:
```python
txt_clip = TextClip(
    text,
    fontsize=100,      # Change size
    color="lime",      # Change color
    font="Arial-Bold", # Change font
    stroke_width=3     # Change outline
)
```

### 4. Use Different LLM
Replace OpenAI with:
```python
# Using Claude (Anthropic)
from anthropic import Anthropic
client = Anthropic()

# Or using local LLM
from ollama import OllamaLLM
```

---

## ✅ Next Steps

1. **Run Quick Test:**
   ```bash
   python check_dependencies.py
   ```

2. **Try Example:**
   ```bash
   python examples.py
   ```

3. **Process Your Video:**
   ```bash
   python main_integrated.py --input your_video.mp4
   ```

4. **Customize:**
   - Edit settings in `Config` class
   - Modify prompts in `content_intelligence.py`
   - Adjust styles in `video_renderer.py`

5. **Deploy:**
   - Batch process multiple videos
   - Integrate into workflow scripts
   - Build REST API wrapper

---

## 📚 File Structure Explained

```
main_integrated.py
├── Config                 # Configuration settings
├── ViralVideoGenerator    # Main orchestrator
│   ├── initialize_components()   # Create 4 components
│   ├── run_pipeline()           # Execute pipeline
│   │   ├── _step_1_audio_processing()     # Extract & transcribe
│   │   ├── _step_2_content_analysis()     # Analyze moments
│   │   ├── _step_3_vision_processing()    # Detect faces
│   │   └── _step_4_rendering()            # Render output
│   └── save_report()            # Save JSON report
└── main()                 # CLI entry point
```

---

## 🎓 Learning Resources

- **Whisper**: https://github.com/openai/whisper
- **MoviePy**: https://zulko.github.io/moviepy/
- **MediaPipe**: https://google.github.io/mediapipe/
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **FFmpeg**: https://ffmpeg.org/

---

## 🆘 Need Help?

1. Check [README.md](README.md) for detailed documentation
2. Review [examples.py](examples.py) for usage patterns
3. Check component files for inline documentation
4. Run with verbose output for debugging

---

**Ready to create viral videos! 🚀**

```bash
python main_integrated.py --input test.mp4
```
