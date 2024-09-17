from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from ultralytics.engine.results import Results, Boxes
import torch
import numpy as np
import cv2
from cv2 import VideoCapture
from cv2.typing import MatLike
import time

class Prediction:
    @staticmethod
    def predict_frame(model: YOLO, frame: MatLike) -> Annotator:
        '''
        Predicts on a frame using a model.
        '''
        results: list[Results] = model.predict(frame, verbose=True, imgsz=352)
        for result in results:
            annotator: Annotator = Annotator(frame)
            boxes: Boxes = result.boxes
            for box in boxes:
                b: (torch.Tensor | np.ndarray) = box.xyxy[0]
                c: (torch.Tensor | np.ndarray) = box.cls
                annotator.box_label(b, model.names[int(c)] + " " + str(box.conf))
        return annotator
    
    @staticmethod
    def predict_video(model_file: str, video_file: str) -> None:
        '''
        Predicts on a video file using a model file.
        '''
        model: YOLO = YOLO(model=model_file)
        
        video_capture: VideoCapture = VideoCapture(filename=video_file)
        
        frame_rate: float = video_capture.get(cv2.CAP_PROP_FPS)
        delay_per_frame: float = (1 / frame_rate) # Seconds
        
        successful_frame_read: bool = False
        current_frame: MatLike = None
        successful_frame_read, current_frame = video_capture.read()
        
        current_time: float = time.time()
        previous_time: float = current_time
        while successful_frame_read:
            # Predict
            annotator: Annotator = Prediction.predict_frame(model=model, frame=current_frame)
            
            # Display
            cv2.imshow("frame", annotator.result())
            
            # End video when press 'q'
            key: int = cv2.waitKey(1)
            if key == ord("q"):
                break
            
            # Wait for duration
            current_time = time.time()
            difference = current_time - previous_time
            previous_time = current_time
            time.sleep(max(delay_per_frame - difference, 0))
            
            # Read next frame
            successful_frame_read, current_frame = video_capture.read()
            
    def print_names(model_file: str) -> None:
        '''
        Prints the names of the classes in a model file.
        '''
        model: YOLO = YOLO(model=model_file)
        print(model.names)
        
if __name__ == "__main__":
    Prediction.predict_video(
        model_file="runs/detect/train3/weights/best.pt",
        video_file="full_videos_for_prediction/000090258_001.mp4"
    )
    
    # Prediction.print_names(model_file="runs/detect/train3/weights/best.pt")