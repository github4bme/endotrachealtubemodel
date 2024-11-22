from ultralytics import YOLO
from data_format_util import DataFormatUtil
import yaml
import csv
import datetime
import os
import argparse

def log_test_history(results_dir: str, model_version: str, dataset: str, csv_filename: str) -> None:
    print(f"Logging test results for {model_version} with dataset {dataset} to {csv_filename}.")

    # If the dataset is combined_dataset, log the individual datasets
    if dataset == 'combined_dataset':
        yaml_file = os.path.join('datasets', 'combined_dataset', 'data.yaml')
        with open(yaml_file, 'r') as file:
            data_yaml = yaml.load(file, Loader=yaml.FullLoader)
        datasets_contained = data_yaml['datasets_contained']
        dataset = f"Combined dataset containing [{', '.join(datasets_contained)}]"

    # Open the CSV file in append mode
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header if the file is new
        if not os.path.isfile(csv_filename):
            writer.writerow(['Results Directory', 'Model Version', 'Dataset tested on', 'Timestamp', 'Link'])
        
        # Write the new entry
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results_dir_link = f'=HYPERLINK("./runs/detect/{results_dir}", "Link")'
        writer.writerow([results_dir, model_version, dataset, timestamp, results_dir_link])

class Tester:
    @staticmethod
    def test(model_file: str, dataset_file: str, run_number: int) -> None:
        # '''
    #     Test a model on a dataset.
    #     This will output the validation results to
    #     a new directory within runs/detect/
    #     called valN, where N is the provided run_number.
    #     . Ensure that in your 
    #     AppData/Roaming/Ultralytics/settings.yaml file,
    #     the datasets_dir ends with this main project repo,
    #     like this:
    #     datasets_dir: C:\Users\Declan O'Brien\Documents\Capstone\EndotrachealTubeModel
    #     '''
        model: YOLO = YOLO(model=model_file)
        validation_results = model.val(data=dataset_file, project='runs/detect', name=f'val{run_number}', exist_ok=True)
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
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--model_name', type=str, help='Name of the model to test on.', required=True)
    arg_parser.add_argument('--dataset_name', type=str, help='Name of the dataset to test on.', required=True)
    arg_parser.add_argument('--run_number', type=int, help='The number of run (i.e, the N value in valN).', required=True)
    args = arg_parser.parse_args()

    Tester.test(
        model_file=DataFormatUtil.model_file_path_from_run_name(args.model_name),
        dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name(args.dataset_name),
        run_number=args.run_number
    )
    log_test_history(f'val{args.run_number}', args.model_name, args.dataset_name, 'test_history.csv')