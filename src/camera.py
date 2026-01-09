import cv2
import time
import numpy as np
from .detector import Detector
from .segmenter import Segmenter
from .telegram_bot import TelegramBot

class Camera:
    def __init__(self):
        # Initialize video capture
        # Try index 0, if fails try 1
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
             self.video = cv2.VideoCapture(1)
        
        self.detector = Detector()
        self.segmenter = Segmenter()
        
        # Initialize Telegram Bot (Replace with actual token/chat_id or use env vars)
        # Placeholder values - User must update these
        self.telegram = TelegramBot(token='YOUR_TELEGRAM_TOKEN', chat_id='YOUR_CHAT_ID')
        
        self.last_alert_time = 0
        self.alert_cooldown = 10  # Seconds between alerts

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        if not ret:
            return None

        # 1. Resize for performance (optional, keeping original size for better detection if system allows)
        # frame = cv2.resize(frame, (640, 480))
        
        # 2. Get ROI (Purple Zone)
        mask, roi_contour = self.segmenter.get_roi(frame)
        
        # 3. Detect People
        detections = self.detector.detect(frame)
        
        person_in_roi = False
        
        # 4. Process Detections
        for det in detections:
            x1, y1, x2, y2 = det['box']
            center_point = ((x1 + x2) // 2, (y1 + y2) // 2)
            
            # Check if person is inside the ROI
            # If no ROI found (roi_contour is None), decide policy. 
            # Here: Only detect if inside purple zone. If no zone, no detection alert.
            is_inside = self.segmenter.is_point_in_roi(center_point, roi_contour)
            
            color = (0, 255, 0) # Green for outside
            if is_inside:
                person_in_roi = True
                color = (0, 0, 255) # Red for inside ROI
                
            # Draw Bounding Box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"{det['label']} {det['confidence']:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 5. Draw ROI
        frame = self.segmenter.draw_roi(frame, roi_contour)
        
        # 6. Handle Alerts
        if person_in_roi:
            current_time = time.time()
            if current_time - self.last_alert_time > self.alert_cooldown:
                print("[INFO] Person detected in Huaca! Sending alert...")
                self.telegram.send_message("⚠️ ALERTA: Persona detectada en la zona Huaca!")
                self.last_alert_time = current_time
                
                # Optional: Send photo? (Not implemented in basic version but possible)

        # Encode frame
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
