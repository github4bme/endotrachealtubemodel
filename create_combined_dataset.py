import os
import argparse
import yaml

# Helper function to create symbolic links for images and labels in a dataset
def create_symlinks_with_prefix(datasets_dir: str, source_folder: str, target_folder: str, data_split: str, datatype: str) -> None:
    # Get the paths to the source and target validation folders
    source_path = os.path.join(datasets_dir, source_folder, data_split, datatype)
    target_path = os.path.join(datasets_dir, target_folder, data_split, datatype)
    
    # Define a prefix based on the source folder name
    prefix = source_folder + '_'
    
    # Create symbolic links
    if os.path.exists(source_path):
        for file in os.listdir(source_path):
            source_file_path = os.path.join(source_path, file)
            target_file_path = os.path.join(target_path, prefix + file)
            if os.path.exists(target_file_path) or os.path.islink(target_file_path):
                print(f"Skipping {source_file_path} -> {target_file_path} (File already exists)")
            else:
                os.symlink(source_file_path, target_file_path)
                print(f"Created symlink: {source_file_path} -> {target_file_path}")
            
# Helper function to inspect the validity of symbolic links in a directory
def inspect_symlinks(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check if the file is a symbolic link
            if os.path.islink(file_path):
                # Get the target of the symlink
                target_path = os.readlink(file_path)
                # Check if the target exists
                if os.path.exists(target_path):
                    print(f"Valid symlink: {file_path} -> {target_path}")
                else:
                    print(f"Broken symlink: {file_path} -> {target_path} (Target does not exist)")
            else:
                print(f"Not a symlink: {file_path}")

if __name__ == '__main__':
    # '''
    # Create a combined dataset by creating symbolic links that point to the images and labels of multiple datasets.
    # Because YOLOv8's path resolver cannot handle symbolic links with relative paths
    # (I'm not sure, but it seems to be the case for me), 
    # here I use absolute paths instead.
    # Since the absolute path of the 'datasets' folder might be different on different machines, 
    # I've added those symbolic links to gitignore. 
    # And you'll need to run this script to create them on your machine.
    # '''
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group(required=True) # Either create symlinks for all datasets or for a specific new dataset
    group.add_argument('--for_all', action='store_true', help='Create symbolic links for all datasets.')
    group.add_argument('--source_folder', type=str, help='The name of the source folder containing the data.')
    args = arg_parser.parse_args()
    
    datasets_dir = os.path.abspath('datasets')
    target_folder = 'combined_dataset'
    # Create the target directories and data.yaml file if they don't exist
    os.makedirs(os.path.join(datasets_dir, target_folder, 'training', 'images'), exist_ok=True)
    os.makedirs(os.path.join(datasets_dir, target_folder, 'training', 'labels'), exist_ok=True)
    os.makedirs(os.path.join(datasets_dir, target_folder, 'validation', 'images'), exist_ok=True)
    os.makedirs(os.path.join(datasets_dir, target_folder, 'validation', 'labels'), exist_ok=True)
    data_yaml: dict = {
        'train': './training/images',
        'val': './validation/images',
        'nc': 3,
        'names': ['trachea', 'epiglottis', 'uvula']
    }
    with open(os.path.join(datasets_dir, target_folder, 'data.yaml'), "w") as file:
        yaml.dump(data_yaml, file, default_flow_style=None)

    if args.for_all:
        for source_folder in os.listdir(datasets_dir):
            if source_folder == target_folder:
                continue
            create_symlinks_with_prefix(datasets_dir, source_folder, target_folder, data_split='training', datatype='images')
            create_symlinks_with_prefix(datasets_dir, source_folder, target_folder, data_split='training', datatype='labels')
            create_symlinks_with_prefix(datasets_dir, source_folder, target_folder, data_split='validation', datatype='images')
            create_symlinks_with_prefix(datasets_dir, source_folder, target_folder, data_split='validation', datatype='labels')
    else:
        create_symlinks_with_prefix(datasets_dir, args.source_folder, target_folder, data_split='training', datatype='images')
        create_symlinks_with_prefix(datasets_dir, args.source_folder, target_folder, data_split='training', datatype='labels')
        create_symlinks_with_prefix(datasets_dir, args.source_folder, target_folder, data_split='validation', datatype='images')
        create_symlinks_with_prefix(datasets_dir, args.source_folder, target_folder, data_split='validation', datatype='labels')

    '''
    # Inspect the validity of the symbolic links
    inspect_symlinks(os.path.join(datasets_dir, target_folder))
    '''