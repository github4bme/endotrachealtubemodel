import os
import argparse
import yaml

# Helper function to create symbolic links for images and labels in the validation set of a dataset
def create_symlinks_with_prefix(source_folder, target_folder):
    # Get the paths to the source and target validation folders
    source_val_path = get_val_path(source_folder)
    target_val_path = get_val_path(target_folder)
    
    # Define a prefix based on the dataset folder name
    prefix = source_folder + '_'
    
    # Paths for images and labels inside each dataset's validation folder
    images_dir = os.path.join(source_val_path, 'images')
    labels_dir = os.path.join(source_val_path, 'labels')
    
    # Create symbolic links for images
    if os.path.exists(images_dir):
        for image_file in os.listdir(images_dir):
            image_source = os.path.join(images_dir, image_file)
            # Add prefix to avoid filename conflicts
            image_target = os.path.join(target_val_path, 'images', prefix + image_file)
            
            # Create the symbolic link, skip if it already exists
            if os.path.exists(image_target) or os.path.islink(image_target):
                print(f'Skipping existing link: {image_target}')
            else:
                os.symlink(image_source, image_target)
                print(f'Linked: {image_source} -> {image_target}')
    
    # Create symbolic links for labels
    if os.path.exists(labels_dir):
        for label_file in os.listdir(labels_dir):
            label_source = os.path.join(labels_dir, label_file)
            # Add prefix to avoid filename conflicts
            label_target = os.path.join(target_val_path, 'labels', prefix + label_file)
            
            # Create the symbolic link, skip if it already exists
            if os.path.exists(label_target) or os.path.islink(label_target):
                print(f'Skipping existing link: {label_target}')
            else:
                os.symlink(label_source, label_target)
                print(f'Linked: {label_source} -> {label_target}')

# Helper function to get the path to the validation set of a dataset
def get_val_path(dataset_folder):
    return os.path.join(os.path.abspath('datasets'), dataset_folder, 'validation')

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
    # Creates symbolic links for images and labels in the validation set of a dataset, 
    # so that they can be combined into a single test set.
    # Because YOLOv8's path resolver cannot handle symbolic links with relative paths
    # (I'm not sure, but it seems to be the case for me), 
    # here I use absolute paths instead.
    # Since the absolute path of the 'datasets' folder might be different on different machines, 
    # I've added those symbolic links to gitignore. 
    # And you'll need to run this script to create them on your machine.
    # '''
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group(required=True) # Either create symlinks for all datasets or for a specific dataset
    group.add_argument('--for_all', action='store_true', help='Create symbolic links for all datasets.')
    group.add_argument('--source_folder', type=str, help='The name of the source folder containing the data.')
    args = arg_parser.parse_args()
    
    target_folder = 'combined_testset'
    # Create the target directories and data.yaml file if they don't exist
    os.makedirs(os.path.join('./datasets', target_folder, 'validation', 'images'), exist_ok=True)
    os.makedirs(os.path.join('./datasets', target_folder, 'validation', 'labels'), exist_ok=True)
    data_yaml: dict = {
        'train': './train/images',
        'val': './validation/images',
        'nc': 3,
        'names': ['trachea', 'epiglottis', 'uvula']
    }
    with open(os.path.join('./datasets', target_folder, 'data.yaml'), "w") as file:
        yaml.dump(data_yaml, file, default_flow_style=None)

    if args.for_all:
        for source_folder in os.listdir('./datasets'):
            if source_folder == target_folder:
                continue
            create_symlinks_with_prefix(source_folder, target_folder)
    else:
        create_symlinks_with_prefix(args.source_folder, target_folder)
    '''
    inspect_symlinks(f'./datasets/{target_folder}/validation/images')
    '''
