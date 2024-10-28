class DataFormatUtil:
    @staticmethod
    def model_file_path_from_run_name(run_name: str) -> str:
        '''
        Returns the model file path from a run name.
        '''
        return f"runs/detect/{run_name}/weights/best.pt"
    
    @staticmethod
    def dataset_file_path_from_dataset_name(dataset_name: str) -> str:
        '''
        Returns the dataset file path from a dataset name.
        '''
        return f"/Users/jakeyablok/EndotrachealTubeModel/datasets/{dataset_name}/data.yaml"
    
    @staticmethod
    def video_for_prediction_file_path_from_video_name(video_name: str) -> str:
        '''
        Returns the video file path from a video name.
        '''
        return f"full_videos_for_prediction/{video_name}"
    
    @staticmethod
    def full_predicted_video_file_path_from_video_name(video_name: str) -> str:
        '''
        Returns the full predicted video file path from a video name.
        '''
        return f"full_predicted_videos/{video_name}"