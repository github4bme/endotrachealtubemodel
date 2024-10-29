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
        results = model.train(data=dataset_file, epochs=11)
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
        results = model.train(data=dataset_file, epochs=11)
        print(results)
    
if __name__ == "__main__":
    model_name = input("Please enter name of model to train on.\n")
    dataset_name = input("Please enter name of new dataset to train on.\n")

    Trainer.train(
        model_file=DataFormatUtil.model_file_path_from_run_name(model_name),
        dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name(dataset_name)
    )