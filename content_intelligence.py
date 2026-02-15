<<<<<<< HEAD
=======
<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
>>>>>>> aa72dfb (Initial project setup: WebPedPok YouTube video analysis and content intelligence system)
>>>>>>> SIJN
import json
import os
from typing import Dict, List, Any, Optional

class ContentIntelligence:
    """Component 2: Content Intelligence (NLP/LLM)
    
    ฟังก์ชัน: วิเคราะห์ Transcript เพื่อหา "Hook" และ "Viral Moments"
    ใช้ OpenAI GPT API (หรือ LLM อื่น)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo"):
        """
        Args:
            api_key: OpenAI API Key (ถ้าเป็น None จะหาจาก env variable OPENAI_API_KEY)
            model: ชนิดของ Model ที่ใช้ (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
        """
        self.model = model
        
        # หา API Key
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("⚠️  ไม่พบ OpenAI API Key")
            print("   - ตั้งค่า: export OPENAI_API_KEY='your-key' (Linux/Mac)")
            print("   - หรือ: set OPENAI_API_KEY=your-key (Windows)")
            print("   - หากไม่มี Key, ระบบจะใช้ Mock Analysis แทน")
            self.client = None
        else:
            try:
                import openai
                self.client = openai.OpenAI(api_key=api_key)
                print(f"🧠 กำลังสร้าง ContentIntelligence...")
                print(f"   - Model: {self.model}")
                print(f"   ✅ OpenAI API connected")
            except ImportError:
                print("⚠️  ไม่พบ 'openai' package - ติดตั้งด้วย: pip install openai")
                self.client = None
    
    def find_best_moments(self, transcript_text: str, num_moments: int = 3) -> List[Dict[str, Any]]:
        """หาช่วง "Hook moments" ที่น่าสนใจที่สุดจาก transcript
        
        Args:
            transcript_text: ข้อความที่แกะมาจากวิดีโอ
            num_moments: จำนวนช่วงเด็ดที่ต้องการ
            
        Returns:
            List[Dict] : รายการ moments พร้อม {
                "start": float,
                "end": float,
                "headline": str,
                "viral_score": int,
                "reason": str
            }
        """
        print(f"🧠 3. กำลังวิเคราะห์เนื้อหาด้วย ContentIntelligence...")
        
        if self.client is None:
            print("   ⚠️  ใช้ Mock Analysis (เพราะไม่มี API Key)")
            return self._mock_analysis(transcript_text, num_moments)
        
        # พร้อมธรรม LLM สำหรับการวิเคราะห์
        prompt = f"""
        วิเคราะห์ Transcript ต่อไปนี้และหา {num_moments} ช่วง "Hook/Viral Moments" ที่ดีที่สุด
        
        Transcript:
        {transcript_text}
        
        ภารกิจ:
        1. หา {num_moments} ช่วงที่น่าสนใจ/ตลกสนุก/ตื่นเต้น ที่สุด
        2. อนุมานเวลาประมาณ (start, end) จาก context (หากไม่มี timestamp ให้ประมาณ)
        3. สรุปหัวข้อ (Headline) ให้กระชับและดึงดูด
        4. คะแนน Viral Score (0-100) โดยพิจารณา:
           - ความตลกสนุก/ตื่นเต้น
           - ความน่าแบ่งปัน
           - Relatable ต่อผู้ชมหลาย
        5. อธิบาย "เพราะเหตุใด" ช่วงนี้จึงดี
        
        ตอบกลับในรูปแบบ JSON array เท่านั้น (ห้ามมีข้อความอื่น):
        [
            {{
                "start": 10.5,
                "end": 45.0,
                "headline": "...",
                "viral_score": 90,
                "reason": "..."
            }},
            ...
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a viral content expert. Analyze transcripts and find the best moments that would go viral on social media. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            # แยก JSON จากคำตอบ
            response_text = response.choices[0].message.content.strip()
            
            # ลองแยก JSON
            try:
                moments = json.loads(response_text)
            except json.JSONDecodeError:
                # ถ้า JSON ไม่สมบูรณ์ ลองค้นหา JSON ในข้อความ
                import re
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    moments = json.loads(json_match.group())
                else:
                    print("   ❌ ไม่สามารถแยก JSON จาก LLM - ใช้ Mock Analysis แทน")
                    moments = self._mock_analysis(transcript_text, num_moments)
            
            print(f"   ✅ วิเคราะห์สำเร็จ - พบ {len(moments)} moments")
            return moments
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print("   ⚠️  ใช้ Mock Analysis แทน")
            return self._mock_analysis(transcript_text, num_moments)
    
    def _mock_analysis(self, transcript_text: str, num_moments: int = 3) -> List[Dict[str, Any]]:
        """Mock analysis สำหรับเมื่อไม่มี API Key หรือมี Error
        
        ใช้ heuristics ง่ายๆ เพื่อหา "interesting moments"
        """
        moments = []
        
        # ตรวจหาคำสำคัญที่เกี่ยวข้องกับ viral content
        viral_keywords = [
            "ฮา", "ตลก", "ตื่นเต้น", "อนาคต", "เปลี่ยน",
            "วิวพิศวาส", "น่าอัศจรรย์", "ท้าทาย", "ชนะ",
            "impressed", "amazing", "incredible", "funny", "hilarious",
            "shocking", "wow", "awesome"
        ]
        
        # ตัดข้อความเป็น segments ง่ายๆ
        text_lower = transcript_text.lower()
        
        # 1st Mock Moment: ช่วงกลาง (ปกติจะดี)
        moments.append({
            "start": 15.0,
            "end": 45.0,
            "headline": "ช่วงที่ 1: บทนำหลัก",
            "viral_score": 75,
            "reason": "Mock analysis - ช่วงกลางมักมีความเน้นชัด"
        })
        
        # 2nd Mock Moment: หลังจากนั้น
        if num_moments >= 2:
            moments.append({
                "start": 50.0,
                "end": 80.0,
                "headline": "ช่วงที่ 2: จุดสุดท้าย",
                "viral_score": 82,
                "reason": "Mock analysis - จบลงอย่างแข็งแกร่ง"
            })
        
        # 3rd Mock Moment
        if num_moments >= 3:
            moments.append({
                "start": 25.0,
                "end": 55.0,
                "headline": "ช่วงที่ 3: ข้อมูลหลัก",
                "viral_score": 68,
                "reason": "Mock analysis - สำคัญแต่อาจจะนิ่มชา"
            })
        
        return moments[:num_moments]
