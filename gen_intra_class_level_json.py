from utils.util import *

import argparse
import csv
import json
import os
import random

from utils.util import *


def read_conversion_file(file:str):
    with open(file, "r", encoding="utf-8") as file:
        CATEGORY_ID_TO_CLASS_ID = {}
        lines = file.readlines()
        for line in lines:
            category_id, class_id = line.strip().split(" ")
            category_id = int(category_id)
            class_id = int(class_id)
            CATEGORY_ID_TO_CLASS_ID[category_id] = class_id
        return CATEGORY_ID_TO_CLASS_ID

def convert_category_to_class_id(json_data, CATEGORY_ID_TO_CLASS_ID):
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        class_id = CATEGORY_ID_TO_CLASS_ID[category_id]
        annotation["category_id"] = class_id
    return json_data

def filter_json_data(json_data, CATEGORY_ID_TO_CLASS_ID):
    # Filter out the annotations that are not in the conversion file
    # It is because some category does not have class

    filtered_annotations = []
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        if category_id in CATEGORY_ID_TO_CLASS_ID:
            filtered_annotations.append(annotation)
    
    filtered_image_id = set()
    for annotation in filtered_annotations:
        image_id = annotation["image_id"]
        filtered_image_id.add(image_id)
    
    # Filter out the images that are not in the filtered annotations
    filtered_images = []
    for image in json_data["images"]:
        image_id = image["id"]
        if image_id in filtered_image_id:
            filtered_images.append(image)
    
    filtered_json_datas = {
        "images": filtered_images,
        "annotations": filtered_annotations,
        "categories": json_data["categories"],
    }

    return filtered_json_datas


def main(json_file, seen_file, unseen_file, train_ratio):
    
    print(f"Reading seen classes from {seen_file}")
    ID_TO_SEEN_CLASS = read_classes_file(seen_file)
    print(f"There are {len(ID_TO_SEEN_CLASS.keys())} seen classes")

    print(f"Reading unseen classes from {unseen_file}")
    ID_TO_UNSEEN_CLASS = read_classes_file(unseen_file)
    print(f"There are {len(ID_TO_UNSEEN_CLASS.keys())} unseen classes")

    print(f"Reading final json file")
    json_data = read_json(json_file)
    print(f"Total images: {len(json_data['images'])}, total annotations: {len(json_data['annotations'])}, total category: {len(json_data['categories'])}")

    origin_image_count = len(json_data["images"])
    origin_annotation_count = len(json_data["annotations"])

    print("Extract seen classes from json")
    seen_json_data = extract_json_data(json_data, ID_TO_SEEN_CLASS)

    print(f"Split json data with train ratio {train_ratio}")
    train_json_data, val_json_data = split_json_data(seen_json_data, train_ratio)

    print(f"Train images: {len(train_json_data['images'])}, train annotations: {len(train_json_data['annotations'])}, train categories: {len(train_json_data['categories'])}")
    print(f"Val images: {len(val_json_data['images'])}, val annotations: {len(val_json_data['annotations'])}, val categories: {len(val_json_data['categories'])}")

    print("Extract unseen classes from json")
    unseen_json_data = extract_json_data(json_data, ID_TO_UNSEEN_CLASS)
    print(f"Unseen images: {len(unseen_json_data['images'])}, unseen annotations: {len(unseen_json_data['annotations'])}, unseen categories: {len(unseen_json_data['categories'])}")

    print("Join val and unseen json data")
    val_json_data = join_json_data(val_json_data, unseen_json_data)
    print(f"Val images: {len(val_json_data['images'])}, val annotations: {len(val_json_data['annotations'])}, val categories: {len(val_json_data['categories'])}")


    print("Remove overlapping data")
    train_json_data, val_json_data = remove_overlapping_data(train_json_data, val_json_data)

    print(f"Train images: {len(train_json_data['images'])}, train annotations: {len(train_json_data['annotations'])}, train categories: {len(train_json_data['categories'])}")
    print(f"Val images: {len(val_json_data['images'])}, val annotations: {len(val_json_data['annotations'])}, val categories: {len(val_json_data['categories'])}")


    print("Remove duplicated data")
    train_json_data = remove_duplicate_json_data(train_json_data)
    val_json_data = remove_duplicate_json_data(val_json_data)

    print(f"Train images: {len(train_json_data['images'])}, train annotations: {len(train_json_data['annotations'])}, train categories: {len(train_json_data['categories'])}")
    print(f"Val images: {len(val_json_data['images'])}, val annotations: {len(val_json_data['annotations'])}, val categories: {len(val_json_data['categories'])}")

    train_images_count = len(train_json_data["images"])
    train_annotations_count = len(train_json_data["annotations"])
    val_images_count = len(val_json_data["images"])
    val_annotations_count = len(val_json_data["annotations"])

    assert origin_image_count >= train_images_count + val_images_count, f"Train images count {train_images_count} + Val images count {val_images_count} > Origin image count {origin_image_count}"
    assert origin_annotation_count >= train_annotations_count + val_annotations_count, f"Train annotation count {train_annotations_count} + Val annotation count {val_annotations_count} > Origin annotation count {origin_annotation_count}"

    output_folder = "json/"
    os.makedirs(output_folder, exist_ok=True)

    train_json_file = os.path.join(output_folder, "intra_class_train.json")
    print(f"Save train json data to {train_json_file}")
    write_json(train_json_file, train_json_data)

    val_json_file = os.path.join(output_folder, "intra_class_val.json")
    print(f"Save val json data to {val_json_file}")
    write_json(val_json_file, val_json_data)

if __name__ == "__main__":
    json_file = "./final.json"
    seen_file = "category/intra-class_seen.txt"
    unseen_file = "category/intra-class_unseen.txt"
    train_ratio = 0.8
    main(json_file, seen_file, unseen_file, train_ratio)