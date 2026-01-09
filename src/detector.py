from ultralytics import YOLO
import cv2

class Detector:
    def __init__(self, model_path='yolov8n.pt'):
        print(f"[INFO] Loading YOLOv8 model from {model_path}...")
        try:
            self.model = YOLO(model_path)
            # Filter classes to only include 'person' (class 0 in COCO)
            self.target_classes = [0] 
        except Exception as e:
            print(f"[ERROR] Could not load model: {e}")
            self.model = None

    def detect(self, frame):
        if self.model is None:
            return []
        
        # Run inference
        results = self.model(frame, verbose=False)
        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                if cls_id in self.target_classes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    conf = float(box.conf[0])
                    detections.append({
                        'box': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': conf,
                        'class_id': cls_id,
                        'label': 'person'
                    })
        
        return detections
