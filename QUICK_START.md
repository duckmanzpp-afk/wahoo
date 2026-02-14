# 🎬 Quick Start Guide (3 วิธี)

## วิธีที่ 1️⃣: **ที่ง่ายที่สุด** (แนะนำ!)

### Windows:
```bash
# แค่ดับเบิลคลิก
RUN.bat
```

### macOS/Linux:
```bash
python quick_start.py
```

**ผลลัพธ์:**
- Auto-detect GPU หรือ CPU
- Auto-select model ที่เหมาะสม
- ถามว่า render ไหม
- ประมวลผลเอง ✅

---

## วิธีที่ 2️⃣: **Command Line** (สำหรับ Pro)

### YouTube URL:
```bash
python main_integrated.py --input "https://youtu.be/VIDEO_ID" --model auto --device auto
```

### ไฟล์วิดีโอ Local:
```bash
python main_integrated.py --input myvideo.mp4
```

### เฉพาะวิเคราะห์ (ไม่เรนเดอร์) - **เร็วที่สุด!**:
```bash
python main_integrated.py --input "https://youtu.be/VIDEO_ID" --no-render --no-vision
```

---

## วิธีที่ 3️⃣: **ปรับแต่ง Custom**

### CPU Mode (ทั่วไป):
```bash
python main_integrated.py \
  --input "https://youtu.be/VIDEO_ID" \
  --model tiny \
  --device cpu \
  --preset ultrafast \
  --no-vision
```

**ระยะเวลา:** 15-30 นาที

### GPU Mode (ถ้ามี NVIDIA GPU):
```bash
python main_integrated.py \
  --input "https://youtu.be/VIDEO_ID" \
  --model small \
  --device cuda \
  --preset medium
```

**ระยะเวลา:** 5-10 นาที

---

## 📊 ตัวเลือก

| Flag | โดยปกติ | ตัวอย่าง |
|------|--------|--------|
| `--input` | test.mp4 | `"https://youtu.be/abc"` หรือ `video.mp4` |
| `--output` | output_viral.mp4 | `my_result.mp4` |
| `--model` | large-v3-turbo | `tiny`, `small`, `base` |
| `--device` | cuda (ถ้ามี) | `cpu` หรือ `cuda` |
| `--preset` | medium | `ultrafast`, `fast`, `slow` |
| `--no-vision` | - | ปิดการตรวจจับใบหน้า (เร็วขึ้น) |
| `--no-render` | - | เฉพาะวิเคราะห์ (เร็วที่สุด) |
| `--no-9-16` | - | ไม่สร้างรูปแบบ 9:16 |

---

## 🎯 คำแนะนำ

### ✅ ถ้า CPU ช้า:
```bash
python quick_start.py
# หรือ
python main_integrated.py --input URL --no-render --no-vision
```

### ✅ ถ้ามี GPU:
```bash
python main_integrated.py --input URL --model small --device cuda
```

### ✅ ต้องรวดเร็ว:
```bash
python main_integrated.py --input URL --model tiny --device cpu --no-render --no-vision
```

---

## 📁 Output Files

```
✅ output_viral.mp4          - วิดีโอพร้อมซับไตเติล (16:9)
✅ output_viral_9_16.mp4     - วิดีโอแนวตั้ง (9:16)
✅ analysis_report.json     - ผลการวิเคราะห์ JSON
✅ youtube_download.mp4     - ไฟล์จาก YouTube (ถ้าใช้ URL)
```

---

## ⏱️ เวลาประมาณการ

| Settings | ระยะเวลา |
|----------|---------|
| CPU + tiny + no-render | 10-15 นาที |
| CPU + small + render | 30-45 นาที |
| GPU + small + render | 5-10 นาที |
| GPU + large-v3-turbo + render | 10-15 นาที |

---

## 🆘 Troubleshooting

### OOM (Out of Memory)
```bash
python main_integrated.py --input URL --model tiny --device cpu
```

### yt-dlp Error
```bash
pip install --upgrade yt-dlp
```

### Slow Processing
ใช้ `--no-render` ก่อน เพื่ออ่าน JSON report

---

**เริ่มทำงาน:**

```bash
python quick_start.py
```

สุดท้ายสร้าง step-by-step guide:  

<function_calls>
<invoke name="create_file">
<parameter name="content"># 🎬 STEP-BY-STEP: YouTube → Viral Video

## 📋 ขั้นตอนที่ 1: เตรียมตัว

```bash
# ไปที่ folder
cd c:\Webpedpok

# ตรวจสอบ dependencies
python check_dependencies.py
```

---

## 🚀 ขั้นตอนที่ 2: เลือกวิธีใช้

### **ง่ายสุด** (แนะนำ) ⭐
```bash
python quick_start.py
```
- Auto-detect GPUตรวจเพื่อไม่ต้องคิดเอง
- ให้เลือก render หรือไม่
- ทั้งหมดอยู่ในชีวิต 🎉

### **บริหารจัดการเต็มที่**
```bash
python main_integrated.py --input "YOUTUBE_URL" --output myresult.mp4 --model small --device cpu --no-vision
```

### **เฉพาะวิเคราะห์** (เร็วที่สุด)
```bash
python main_integrated.py --input "YOUTUBE_URL" --no-render --no-vision
```
- ไม่ render วิดีโอ (ประหยัด เวลา 80%)
- ได้ JSON report พอ
- ⏱️ ~10 นาที CPU

---

## 💡 ตัวอย่างการใช้งาน

### Example 1: YouTube Video
```bash
python quick_start.py
# ป้อน: https://youtu.be/95-uxjvP2vw
# เลือก: option 2 (analysis only)
# รอ: 10-15 นาที
# ได้: analysis_report.json
```

### Example 2: Local File
```bash
python main_integrated.py --input myvideo.mp4 --no-vision
```

### Example 3: ต้อง Full Output (Render)
```bash
# ถ้ามี GPU:
python main_integrated.py --input "YOUTUBE_URL" --model small --device cuda --preset fast

# ถ้าเป็น CPU:
# อาจใช้เวลา 30 นาที - อดทน 😅
python main_integrated.py --input "YOUTUBE_URL" --model tiny --device cpu --preset ultrafast
```

---

## 📊 อ่านผลลัพธ์

### analysis_report.json
```json
{
  "input_video": "youtube_download.mp4",
  "language": "th",
  "segments_count": 42,
  "moments": [
    {
      "start": 15.5,
      "end": 45.0,
      "headline": "ช่วงที่ดีที่สุด",
      "viral_score": 92
    }
  ]
}
```

### วิดีโอเอาต์พุต
- `output_viral.mp4` - วิดีโอปกติ + ซับไตเติล
- `output_viral_9_16.mp4` - แนวตั้ง (TikTok style)

---

## ⏰ ระยะเวลาคาดหมาย

```
YouTube Download:      1-3 นาที (ขึ้นอยู่กับขนาดวิดีโอ)
Audio Transcribe:      5-30 นาที (ขึ้นอยู่กับ CPU/GPU)
Content Analysis:      1-2 นาที
Video Rendering:       5-15 นาที (ขึ้นอยู่กับ settings)
────────────────────────────────
รวม (ไม่ render):       10-15 นาที ✅ แนะนำ!
รวม (full render):     20-45 นาที
```

---

## 🎯 Tips & Tricks

### 💨 เร็วสุด
```bash
python main_integrated.py --input URL --model tiny --device cpu --no-render --no-vision
# ⏱️ 10-15 นาที
```

### 🎬 ดีที่สุด (ต้อง GPU)
```bash
python main_integrated.py --input URL --model large-v3-turbo --device cuda --preset slow
# ⏱️ 15-20 นาที
```

### 💻 CPU-Friendly
```bash
python main_integrated.py --input URL --model small --device cpu --no-vision
# ⏱️ 20-30 นาที
# มี render แต่ไม่ face tracking
```

---

## ❓ คำถามที่ถาม บ่อย

### Q: ทำไมช้า?
**A:** CPU ช้า ลองใช้ `--no-render` ก่อน

### Q: ต้องใช้ API Key ไหม?
**A:** ไม่จำเป็น - ใช้ Mock Analysis ถ้าไม่มี

### Q: วิดีโอยาวเท่าไหร่ OK?
**A:** 5-30 นาที ดีสุด (90 นาที > ใช้เวลานาน)

### Q: ต้องดาวน์โหลด model ไหม?
**A:** ใช่ - ครั้งแรก (1-5 GB ขึ้นอยู่กับ model)

### Q: Subtitle เป็นภาษาอะไร?
**A:** ตามวิดีโออิ้น (auto-detect)

---

## 🎉 ทำไว้ดีแล้ว!

```bash
python quick_start.py
```

สั้นงดงง - เพียง 2 บรรทัด แล้วจะมีวิดีโอ viral! 🚀
