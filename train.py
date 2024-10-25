from ultralytics import YOLO
from data_format_util import DataFormatUtil

class Trainer:
    @staticmethod
    def train(model_file: str, dataset_file: str) -> None:
        '''
        Train a model on a dataset.
        This will output the training results to
        a new directory within runs/detect/
        called trainN, where N is the next available
        number of run.
        '''
        model: YOLO = YOLO(model=model_file)
        results = model.train(data=dataset_file)
        print(results)
        
    def train_for_demo(model_file: str, dataset_file: str) -> None:
        '''
        Train a model on a dataset.
        This will output the training results to
        a new directory within runs/detect/
        called trainN, where N is the next available
        number of run.
        '''
        model: YOLO = YOLO(model=model_file)
        results = model.train(data=dataset_file, epochs=5)
        print(results)
    
if __name__ == "__main__":
    # Trainer.train(
    #     model_file=DataFormatUtil.model_file_path_from_run_name("train3"),
    #     dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name("testset2")
    # )
    
    # Trainer.train_for_demo(
    #     model_file=DataFormatUtil.model_file_path_from_run_name("train3"),
    #     dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name("testset2")
    # )
    
    Trainer.train(
        model_file=DataFormatUtil.model_file_path_from_run_name("train3"),
        dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name("047217044_001")
    )