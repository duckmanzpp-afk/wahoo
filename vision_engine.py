<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
>>>>>>> aa72dfb (Initial project setup: WebPedPok YouTube video analysis and content intelligence system)
import cv2
import numpy as np
from typing import Tuple, Optional, List

class VisionEngine:
    """Component 3: Computer Vision (Auto-Reframe)
    
    ฟังก์ชัน: ตรวจจับใบหน้า และ auto-crop วิดีโอเป็นแนวตั้ง (9:16)
    โดยให้ใบหน้าคนพูดอยู่กึ่งกลาง/บน
    """
    
    def __init__(self, confidence: float = 0.5):
        """
        Args:
            confidence: ความเชื่อมั่นในการตรวจจับใบหน้า (0-1)
        """
        try:
            import mediapipe as mp
            # Create face detection object
            face_detection = mp.solutions.face_detection.FaceDetection(
                model_selection=1,  # model_selection=1 สำหรับวิดีโอแสง
                min_detection_confidence=confidence
            )
            self.mp_face_detection = face_detection
            print(f"🔧 กำลังสร้าง VisionEngine...")
            print(f"   - Confidence: {confidence}")
            print(f"   ✅ MediaPipe Face Detection loaded")
        except (ImportError, AttributeError) as e:
            print("❌ ไม่พบ 'mediapipe' package หรือ import error")
            print(f"   Error: {e}")
            print("   ติดตั้งด้วย: pip install mediapipe")
            raise
    
    def get_face_center(self, frame: np.ndarray) -> Tuple[float, float, bool]:
        """ตรวจจับใบหน้า และคืนจุดกึ่งกลาง
        
        Args:
            frame: ภาพ frame (BGR format เหมือนจาก OpenCV)
            
        Returns:
            (x_center, y_center, detected): 
            - x_center: ตำแหน่ง X ของจุดกึ่งกลางใบหน้า (0-1 relative)
            - y_center: ตำแหน่ง Y ของจุดกึ่งกลางใบหน้า (0-1 relative)
            - detected: True หากตรวจจับใบหน้า
        """
        # แปลง BGR เป็น RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # ตรวจจับใบหน้า
        results = self.mp_face_detection.process(frame_rgb)
        
        if results.detections:
            # ใช้ใบหน้าตัวแรก (ปกติคือ person principal)
            bbox = results.detections[0].location_data.relative_bounding_box
            
            x_center = bbox.xmin + (bbox.width / 2)
            y_center = bbox.ymin + (bbox.height / 2)
            
            return x_center, y_center, True
        
        # ถ้าไม่เจอใบหน้า คืน default (กึ่งกลาง)
        return 0.5, 0.5, False
    
    def get_multiple_faces(self, frame: np.ndarray) -> List[Tuple[float, float]]:
        """ตรวจจับหลายใบหน้า คืนรายการจุดกึ่งกลาง
        
        Args:
            frame: ภาพ frame (BGR format)
            
        Returns:
            List[(x_center, y_center)]: รายการจุดกึ่งกลางของใบหน้า
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_face_detection.process(frame_rgb)
        
        face_centers = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x_center = bbox.xmin + (bbox.width / 2)
                y_center = bbox.ymin + (bbox.height / 2)
                face_centers.append((x_center, y_center))
        
        return face_centers
    
    def calculate_crop_window_9_16(
        self,
        frame_width: int,
        frame_height: int,
        face_x: float,
        face_y: float,
        padding_vertical: float = 0.2
    ) -> Tuple[int, int, int, int]:
        """คำนวณ crop window ให้เป็น 9:16 โดยให้ใบหน้าอยู่กลาง
        
        Args:
            frame_width: ความกว้างของ frame ต้นฉบับ
            frame_height: ความสูงของ frame ต้นฉบับ
            face_x: ตำแหน่ง X ของใบหน้า (0-1)
            face_y: ตำแหน่ง Y ของใบหน้า (0-1)
            padding_vertical: padding เพิ่มเติมจาก top (0.2 = 20% ของความสูง)
            
        Returns:
            (x1, y1, x2, y2): พิกัด crop window (pixels)
        """
        # อัตราส่วน 9:16 (width:height)
        target_ratio = 9 / 16
        
        # กำหนดความกว้างของ crop window
        # ใช้ความสูง frame ต้นฉบับเป็นข้อมูลอ้างอิง
        target_width = int(frame_height * target_ratio)
        target_height = frame_height
        
        # ถ้า target_width > frame_width ให้ปรับ
        if target_width > frame_width:
            target_width = frame_width
            target_height = int(target_width / target_ratio)
        
        # คำนวณจุดเริ่มต้น โดยให้ใบหน้าอยู่ตรงกลางสูง
        # แต่อยู่ตาม face_x horizontally
        # และ offset ขึ้นมาเล็กน้อยเพื่อให้มีพื้นที่บน
        
        # Horizontal: จัดศูนย์กลาง face
        center_x = int(face_x * frame_width)
        x1 = max(0, center_x - target_width // 2)
        x2 = min(frame_width, x1 + target_width)
        
        # ปรับถ้าเกินขอบ
        if x2 > frame_width:
            x2 = frame_width
            x1 = max(0, x2 - target_width)
        if x1 < 0:
            x1 = 0
            x2 = min(frame_width, x1 + target_width)
        
        # Vertical: ให้ใบหน้าอยู่สูงขึ้นมา (padding_vertical)
        target_y = int(frame_height * padding_vertical)
        y1 = max(0, int(face_y * frame_height) - target_y)
        y2 = min(frame_height, y1 + target_height)
        
        # ปรับถ้าเกินขอบ
        if y2 > frame_height:
            y2 = frame_height
            y1 = max(0, y2 - target_height)
        if y1 < 0:
            y1 = 0
            y2 = min(frame_height, y1 + target_height)
        
        return x1, y1, x2, y2
    
    def crop_frame_9_16(
        self,
        frame: np.ndarray,
        face_x: float,
        face_y: float,
        padding_vertical: float = 0.2
    ) -> np.ndarray:
        """ตัด frame ให้เป็น 9:16 โดยให้ใบหน้าอยู่กลาง
        
        Args:
            frame: ภาพ frame (BGR)
            face_x: ตำแหน่ง X ของใบหน้า (0-1)
            face_y: ตำแหน่ง Y ของใบหน้า (0-1)
            padding_vertical: padding from top
            
        Returns:
            cropped_frame: ภาพที่ตัดแล้ว
        """
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = self.calculate_crop_window_9_16(w, h, face_x, face_y, padding_vertical)
        
        return frame[y1:y2, x1:x2]
    
    def process_video_samples(self, video_path: str, sample_frames: int = 5) -> dict:
        """วิเคราะห์วิดีโอ เก็บ sample face positions
        
        Args:
            video_path: เส้นทางไฟล์วิดีโอ
            sample_frames: จำนวน frame ตัวอย่างที่ต้องการ
            
        Returns:
            dict: ข้อมูลการวิเคราะห์
        """
        print(f"👁️  4. กำลังวิเคราะห์วิดีโอเพื่อตรวจจับใบหน้า...")
        
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        face_positions = []
        
        # Sample frames ที่ระยะห่างเท่ากัน
        sample_indices = np.linspace(0, frame_count - 1, sample_frames, dtype=int)
        
        for frame_idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if ret:
                x_center, y_center, detected = self.get_face_center(frame)
                time_sec = frame_idx / fps if fps > 0 else 0
                
                face_positions.append({
                    "frame": frame_idx,
                    "time_sec": time_sec,
                    "face_x": x_center,
                    "face_y": y_center,
                    "detected": detected
                })
        
        cap.release()
        
        print(f"   ✅ วิเคราะห์สำเร็จ ({len(face_positions)} samples)")
        print(f"   Total frames: {frame_count}, FPS: {fps:.1f}")
        
        return {
            "video_path": video_path,
            "frame_count": frame_count,
            "fps": fps,
            "face_positions": face_positions,
            "detected_count": sum(1 for p in face_positions if p["detected"])
        }
