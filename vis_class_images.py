from utils.util import *
import os
import shutil
import random

def main(json_file):
    
    json_data = read_json(json_file)

    CATEGORY_ID_TO_NAME = {}
    for category in json_data["categories"]:
        CATEGORY_ID_TO_NAME[category["id"]] = category["name"]
    
    IMAGE_ID_TO_FILENAME = {}
    for image in json_data["images"]:
        IMAGE_ID_TO_FILENAME[image["id"]] = image["file_name"]

    # Sample one image to save for each class in the dataset
    name_to_files = {}
    for annotation in json_data["annotations"]:
        class_id = annotation["category_id"]
        image_id = annotation["image_id"]
        filename = IMAGE_ID_TO_FILENAME[image_id]
        category_name = CATEGORY_ID_TO_NAME[class_id]
        if category_name not in name_to_files:
            name_to_files[category_name] = set()
        name_to_files[category_name].add(filename)

    output_items = {}
    for category_name, image_files in name_to_files.items():
        output_items[category_name] = random.sample(image_files, 1)[0]

    output_folder = "vis"
    for category_name, filename in output_items.items():
        output_folder_class = os.path.join(output_folder, category_name)
        if not os.path.exists(output_folder_class):
            os.makedirs(os.path.join(output_folder_class, "images"))
        shutil.copy(filename, os.path.join(output_folder_class, filename))

if __name__ == "__main__":
    json_file = "json\class_level_val.json"
    main(json_file)