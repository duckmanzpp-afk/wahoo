# 🚀 GitHub Upload Guide

## 📋 ขั้นตอน 1: สร้าง GitHub Repository

### ทำบน GitHub.com:
1. ไปที่ https://github.com/new
2. ใส่ชื่อ: `viral-video-generator`
3. Description: `AI-powered viral video generator from YouTube - Transcribe, Analyze & Render`
4. เลือก **Public** (ถ้าต้องการให้คนอื่นใช้)
5. ✅ กด "Create repository"

**Copy URL ที่ได้เช่น:** `https://github.com/YOUR_USERNAME/viral-video-generator.git`

---

## 🔧 ขั้นตอน 2: ตั้งค่า Git

### 1. ตั้งค่า Git Identity
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. ไปที่โฟลเดอร์ project
```bash
cd c:\Webpedpok
```

### 3. เริ่มต้น Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Viral Video Generator System

- 4 Components: Audio (Whisper), Content (GPT), Vision (MediaPipe), Rendering (MoviePy)
- YouTube download support
- Auto-device detection (CPU/GPU)
- Mock analysis fallback
- Quick start scripts included"
```

---

## 🔑 ขั้นตอน 3: Push ขึ้น GitHub

### ตัวเลือก A: HTTPS (ง่ายสุด)

```bash
git remote add origin https://github.com/YOUR_USERNAME/viral-video-generator.git
git branch -M main
git push -u origin main
```

**ถามให้ username/password:**
- Username: GitHub username
- Password: Personal Access Token (สร้างที่ Settings > Developer settings > Personal access tokens)

### ตัวเลือก B: SSH (ปลอดภัยสุด)

```bash
# 1. สร้าง SSH key (ถ้ายังไม่มี)
ssh-keygen -t ed25519 -C "your.email@example.com"
# ตอบ Enter ทั้งหมด

# 2. เพิ่ม SSH key ที่ GitHub:
# a) Copy key:
type %USERPROFILE%\.ssh\id_ed25519.pub
# b) ไปที่ GitHub > Settings > SSH Keys > New SSH Key
# c) Paste key

# 3. Setup remote
git remote add origin git@github.com:YOUR_USERNAME/viral-video-generator.git
git branch -M main
git push -u origin main
```

---

## 📝 ขั้นตอน 4: สร้าง README.md ที่ดี

(README.md อยู่แล้ว ✅ เพียงแต่เพิ่มเติมอีกนิด)

```bash
# ตรวจสอบ
cat README.md

# ถ้าต้องเพิ่มเติม:
echo "" >> README.md
echo "## 🌍 GitHub" >> README.md
echo "Repository: https://github.com/YOUR_USERNAME/viral-video-generator" >> README.md

git add README.md
git commit -m "Update: Add GitHub link"
git push
```

---

## ✅ ตรวจสอบ

หลังจาก push เสร็จแล้ว:

```bash
# ตรวจสอบ status
git status

# ดู commit history
git log --oneline

# ดู URL remote
git remote -v
```

Output ควรเป็น:
```
origin  https://github.com/YOUR_USERNAME/viral-video-generator.git (fetch)
origin  https://github.com/YOUR_USERNAME/viral-video-generator.git (push)
```

---

## 📂 ไฟล์ที่ upload

```
✅ Core Components (4 files):
   - audio_engine.py
   - content_intelligence.py
   - vision_engine.py
   - video_renderer.py

✅ Main Scripts:
   - main_integrated.py
   - main_upgraded.py
   - main.py

✅ Quick Start:
   - quick_start.py
   - youtube_downloader.py
   - examples.py

✅ Documentation:
   - README.md
   - SETUP.md
   - QUICK_START.md
   - IMPLEMENTATION_SUMMARY.md
   - requirements.txt

✅ Config:
   - .gitignore
   - .env.example
   - RUN.bat
   - check_dependencies.py
```

---

## 🆘 Troubleshooting

### "fatal: not a git repository"
```bash
git init
```

### "Please tell me who you are"
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### "remote origin already exists"
```bash
git remote rm origin
git remote add origin https://github.com/YOUR_USERNAME/viral-video-generator.git
```

### "Permission denied" (SSH)
- ตรวจสอบ SSH key ถูกติดตั้งที่ GitHub ไหม
- ลองใช้ HTTPS แทน

### Windows Terminal ไม่มี git
- Restart terminal หรือ PowerShell
- ตรวจสอบ PATH: `echo $env:Path`

---

## 🎉 ทำเสร็จแล้ว!

Repository ของคุณอยู่ที่:
```
https://github.com/YOUR_USERNAME/viral-video-generator
```

ยอดนิ่ม! ✨ คนอื่นสามารถ:
```bash
git clone https://github.com/YOUR_USERNAME/viral-video-generator.git
cd viral-video-generator
pip install -r requirements.txt
python quick_start.py
```

---

## 📌 Future Updates

```bash
# ทุกครั้งที่มีการแก้ไข:
git add .
git commit -m "Description of changes"
git push origin main
```

---

**Let's go viral! 🚀**
