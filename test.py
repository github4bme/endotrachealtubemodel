from ultralytics import YOLO
from data_format_util import DataFormatUtil
import os

class Tester:
    @staticmethod
    def test(model_file: str, dataset_file: str) -> None:
        # '''
    #     Test a model on a dataset.
    #     This will output the validation results to
    #     a new directory within runs/detect/
    #     called valN, where N is the next available
    #     number of run. Ensure that in your 
    #     AppData/Roaming/Ultralytics/settings.yaml file,
    #     the datasets_dir ends with this main project repo,
    #     like this:
    #     datasets_dir: C:\Users\Declan O'Brien\Documents\Capstone\EndotrachealTubeModel
    #     '''
        model: YOLO = YOLO(model=model_file)
        validation_results = model.val(data=dataset_file)
        print(validation_results)
        
    @staticmethod
    def test_on_multiple_validation_datasets(model_file: str, dataset_files: list[str]) -> None:
    #     '''
    #     Test a model on multiple datasets.
    #     This will output the validation results to
    #     a new directory within runs/detect/
    #     called valN, where N is the next available
    #     number of run. Ensure that in your 
    #     AppData/Roaming/Ultralytics/settings.yaml file,
    #     the datasets_dir ends with this main project repo,
    #     like this:
    #     datasets_dir: C:\Users\Declan O'Brien\Documents\Capstone\EndotrachealTubeModel
    #     '''
        model: YOLO = YOLO(model=model_file)
        for dataset_file in dataset_files:
            validation_results = model.val(data=dataset_file)
            print(validation_results)
            
    @staticmethod
    def test_on_all_validation_datasets(model_file: str) -> None:
        # '''
        # Test a model on all datasets.
        # This will output the validation results to
        # a new directory within runs/detect/
        # called valN, where N is the next available
        # number of run. Ensure that in your 
        # AppData/Roaming/Ultralytics/settings.yaml file,
        # the datasets_dir ends with this main project repo,
        # like this:
        # datasets_dir: C:\Users\Declan O'Brien\Documents\Capstone\EndotrachealTubeModel
        # '''
        validation_dataset_files: list[str] = os.listdir("datasets")
        model: YOLO = YOLO(model=model_file)
        for dataset_file in validation_dataset_files:
            validation_results = model.val(data=DataFormatUtil.dataset_file_path_from_dataset_name(dataset_file))
            print(validation_results)
        
if __name__ == "__main__":
    # Tester.test(
    #     model_file=DataFormatUtil.model_file_path_from_run_name("train3"),
    #     dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name("testset2")
    # )
    
    Tester.test_on_multiple_validation_datasets(
        model_file=DataFormatUtil.model_file_path_from_run_name("train3"),
        dataset_files=[
            DataFormatUtil.dataset_file_path_from_dataset_name("047217044_001"),
            DataFormatUtil.dataset_file_path_from_dataset_name("testset2")
        ]
    )
    
    # Tester.test_on_all_validation_datasets(
    #     model_file=DataFormatUtil.model_file_path_from_run_name("train3")
    # )