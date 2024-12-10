import cv2
import torch
from pathlib import Path


class Detector:
    def __init__(self, weights_path, camera_index=0):
        """Initialize the detector with a model and camera index."""
        self.weights_path = weights_path
        self.camera_index = camera_index

        self.mode_input = "webcam" if camera_index != "frame" else "frame"

        # Check if weights file exists
        if not Path(weights_path).is_file():
            print(f"Error: Weights file '{weights_path}' not found.")
            exit()

        # Load YOLOv5 model
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path=weights_path, force_reload=False
        ).to(device)

        if self.mode_input == "webcam":
            # Configure OpenCV
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                print("Error: Could not open the camera.")
                exit()

    def detect(self, frame_payload=None):
        """Run the detection loop."""
        print("Press 'q' to exit.")
        frame = None

        if self.mode_input == "webcam":

            ret, frame = self.cap.read()

            if not ret:
                print("Error: Failed to read frame from camera.")
                return

        frame = frame_payload if self.mode_input == "frame" else frame

        # Preprocess frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Inference
        with torch.amp.autocast("cuda" if torch.cuda.is_available() else "cpu"):
            results = self.model(rgb_frame)

        # Process results
        detections = results.xyxy[0].cpu().numpy()
        confidence = 0
        for *xyxy, conf, cls in detections:
            x1, y1, x2, y2 = map(int, xyxy)
            label = self.model.names[int(cls)]
            confidence_exactly = 0.7
            if conf > confidence_exactly:
                confidence = conf
                # Draw bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{label} {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
        return frame, confidence


if __name__ == "__main__":
    try:
        detector = Detector("best.pt", 0)
        detector.detect()
    except KeyboardInterrupt:
        print("\nDetection stopped.")
