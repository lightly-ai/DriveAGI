import json
import shutil
import os
import sys

def copy_images(json_file, output_dir):

    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Process each sample in the JSON data
    for _, sample in enumerate(data['samples']):
        source_path = sample['path']
        extension = os.path.splitext(source_path)[1]  # Get extension from source file
        target_filename = f"{sample['id_']}{extension}"
        target_path = os.path.join(output_dir, target_filename)

        # Copy the file
        if not os.path.exists(target_path):
            try:
                shutil.copy(source_path, target_path)
                print(f"Copied '{source_path}' to '{target_path}'")
            except Exception as e:
                print(f"Error: {e}")
        else:
            pass
            #print(f"'{target_path}' already exists")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_json_file> <output_directory>")
    else:
        json_file = sys.argv[1]
        output_dir = sys.argv[2]
        copy_images(json_file, output_dir)
