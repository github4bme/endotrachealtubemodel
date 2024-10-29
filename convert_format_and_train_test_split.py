import cv2
from cv2 import VideoCapture
import os
import random
import yaml

def convert_format_and_train_test_split(dataset_name: str) -> None:
    # Imortant constants
    EXPORTED_DIRECTORY: str = "datasets_exported_from_cvat"   
    TARGET_DATASET_DIRECTORY: str = "datasets"
    TRAINING_PERCENTAGE: float = 0.8
    VALIDATION_PERCENTAGE: float = 1 - TRAINING_PERCENTAGE
    
    # Create desired directories
    os.makedirs(f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/training/images", exist_ok=True)
    os.makedirs(f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/training/labels", exist_ok=True)
    os.makedirs(f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/validation/images", exist_ok=True)
    os.makedirs(f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/validation/labels", exist_ok=True)
    
    # Write data.yaml file
    data_yaml: dict = {
        'train': './training/images',
        'val': './validation/images',
        'nc': 3,
        'names': ['trachea', 'epiglottis', 'uvula']
    }
    with open(f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/data.yaml", "w") as file:
        yaml.dump(data_yaml, file, default_flow_style=None)
    
    # If frames are already in the target directories return
    if os.listdir(f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/training/images") and os.listdir(f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/validation/images"):
        print("Frames already in target directory.")
        return
    
    video_capture: VideoCapture = VideoCapture(filename=f"{EXPORTED_DIRECTORY}/{dataset_name}.mp4")
    frame_file_names: list[str] = os.listdir(f"{EXPORTED_DIRECTORY}/{dataset_name}/labels/train")
    
    total_frames: int = len(frame_file_names)
    num_frames_covered: int = 0
    # Iterate through each frame
    for frame_file_name in frame_file_names:
        # Get frame number
        frame_number_string: str = frame_file_name.removeprefix("frame_").removesuffix(".txt")
        frame_number: int = int(frame_number_string)
        print(f"Processing frame {num_frames_covered}/{total_frames}")
        print(frame_number)
        
        # Get corresponding frame
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        _, frame = video_capture.read()
        
        # Get output directory based on random train-validation split
        random_number_from_zero_to_one: float = random.random()
        training_or_validation: str = "training" if random_number_from_zero_to_one < TRAINING_PERCENTAGE else "validation"
        output_directory: str = f"{TARGET_DATASET_DIRECTORY}/{dataset_name}/{training_or_validation}"
        
        # Save image
        cv2.imwrite(f"{output_directory}/images/scene{frame_number_string}.png", frame)
        
        # Save label
        # Read from source label file
        with open(f"{EXPORTED_DIRECTORY}/{dataset_name}/labels/train/{frame_file_name}", "r") as source_label_file:
            source_label = source_label_file.read()
            # Write to target label file
            with open(f"{output_directory}/labels/scene{frame_number_string}.txt", "w") as target_label_file:
                target_label_file.write(source_label)
                
        num_frames_covered += 1

if __name__ == "__main__":
    convert_format_and_train_test_split(dataset_name="047217044_001")