from ultralytics import YOLO
from data_format_util import DataFormatUtil

class Tester:
    @staticmethod
    def test(model_file: str, dataset_file: str) -> None:
        '''
        Test a model on a dataset.
        This will output the validation results to
        a new directory within runs/detect/
        called valN, where N is the next available
        number of run. Ensure that in your 
        AppData/Roaming/Ultralytics/settings.yaml file,
        the datasets_dir ends with this main project repo,
        like this:
        datasets_dir: C:\Users\Declan O'Brien\Documents\Capstone\EndotrachealTubeModel\
        '''
        model: YOLO = YOLO(model=model_file)
        validation_results = model.val(data=dataset_file)
        print(validation_results)
        
if __name__ == "__main__":
    Tester.test(
        model_file=DataFormatUtil.model_file_path_from_run_name("train3"),
        dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name("testset2")
    )