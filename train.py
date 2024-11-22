from ultralytics import YOLO
from data_format_util import DataFormatUtil
import yaml
import csv
import datetime
import os
import argparse

def log_model_version(new_model_version: str, previous_model_version: str, dataset: str, csv_filename: str) -> None:
    print(f"Logging model version {new_model_version} with dataset {dataset} to {csv_filename}.")

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
            writer.writerow(['New Model Version', 'Previous Model Version Trained On', 'Additional Dataset Trained On', 'Timestamp', 'Details'])
        
        # Write the new entry
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        arg_file_link = f'=HYPERLINK("./runs/detect/{new_model_version}/args.yaml", "Link")'
        writer.writerow([new_model_version, previous_model_version, dataset, timestamp, arg_file_link])

class Trainer:
    @staticmethod
    def train(model_file: str, dataset_file: str, run_number: int) -> None:
        '''
        Train a model on a dataset.
        This will output the training results to
        a new directory within runs/detect/
        called trainN, where N is the provided run_number.
        '''
        model: YOLO = YOLO(model=model_file)
        results = model.train(data=dataset_file, epochs=11, project='runs/detect', name=f'train{run_number}', exist_ok=True)
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
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--model_name', type=str, help='Name of the model to train on.', required=True)
    arg_parser.add_argument('--dataset_name', type=str, help='Name of the dataset to train on.', required=True)
    arg_parser.add_argument('--run_number', type=int, help='The number of run (i.e, the N value in trainN).', required=True)
    args = arg_parser.parse_args()
    
    Trainer.train(
        model_file=DataFormatUtil.model_file_path_from_run_name(args.model_name),
        dataset_file=DataFormatUtil.dataset_file_path_from_dataset_name(args.dataset_name),
        run_number=args.run_number
    )
    log_model_version(new_model_version=f'train{args.run_number}', previous_model_version=args.model_name, dataset=args.dataset_name, csv_filename='model_versions.csv')