import cv2
import numpy as np

class Segmenter:
    def __init__(self):
        # Define HSV range for purple color
        # Adjust these values based on the specific shade of purple in the image
        self.lower_purple = np.array([125, 50, 50])
        self.upper_purple = np.array([155, 255, 255])

    def get_roi(self, frame):
        """
        Detects the purple area in the frame and returns a mask and the contours.
        Returns:
            mask: Binary mask of the ROI.
            roi_contour: The largest contour found corresponding to the purple area.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_purple, self.upper_purple)
        
        # Clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Assume the largest purple area is our target zone (Huaca)
            largest_contour = max(contours, key=cv2.contourArea)
            return mask, largest_contour
        
        return mask, None

    def draw_roi(self, frame, contour):
        if contour is not None:
            cv2.drawContours(frame, [contour], -1, (255, 0, 255), 2)
            # Add text
            x, y, w, h = cv2.boundingRect(contour)
            cv2.putText(frame, "Zona Huaca (ROI)", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        return frame

    def is_point_in_roi(self, point, contour):
        if contour is None:
            return False
        return cv2.pointPolygonTest(contour, point, False) >= 0
