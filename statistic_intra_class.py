import csv
import json
import os

from utils.util import *

def extract_seen_csv_data(file:str, class_mapping):
    data = {}
    for id, name in class_mapping.items():
        data[id] = (name, 0)

    for annotation in file["annotations"]:
        category_id = annotation["category_id"]
        if category_id in class_mapping:
            data[category_id] = (data[category_id][0], data[category_id][1] + 1)
    
    # Convert to list of dictionary for csv writer
    csv_data = []
    for id, (name, count) in data.items():
        data = {
            "Category ID": id,
            "Category Name": name,
            "Annotation Count": count
        }
        csv_data.append(data)

    return csv_data

def extract_unseen_csv_data(file:str, class_mapping):
    data = {}
    for id, name in class_mapping.items():
        data[id] = (name, 0)

    for annotation in file["annotations"]:
        category_id = annotation["category_id"]
        if category_id in class_mapping:
            data[category_id] = (data[category_id][0], data[category_id][1] + 1)
    
    # Convert to list of dictionary for csv writer
    csv_data = []
    for id, (name, count) in data.items():
        data = {
            "Category ID": id,
            "Category Name": name,
            "Annotation Count": count
        }
        csv_data.append(data)

    return csv_data

def extract_csv_data(json_data):
    data = {}
    for category in json_data["categories"]:
        category_id = category["id"]
        data[category_id] = (category["name"], 0)
    
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"] 
        data[category_id] = (data[category_id][0], data[category_id][1] + 1)

    # Convert to list of dictionary for csv writer
    csv_data = []
    for id, (name, count) in data.items():
        data = {
            "Category ID": id,
            "Category Name": name,
            "Annotation Count": count
        }
        csv_data.append(data)

    return csv_data


def write_csv(path, data):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main(train_file, val_file, seen_file, unseen_file, output_folder):

    seen_classes = read_classes_file(seen_file)
    unseen_classes = read_classes_file(unseen_file)

    os.makedirs(output_folder, exist_ok=True)

    print(f"Processing train file {train_file}")
    train_data = read_json(train_file)
    csv_train_data = extract_csv_data(train_data)
    output_path = os.path.join(output_folder, os.path.basename(train_file).replace(".json", ".csv"))
    print(f"Output path: {output_path}")
    write_csv(output_path, csv_train_data)

    print(f"Processing val file {val_file}")
    val_data = read_json(val_file)
    csv_val_data = extract_csv_data(val_data)
    output_path = os.path.join(output_folder, os.path.basename(val_file).replace(".json", ".csv"))
    print(f"Output path: {output_path}")
    write_csv(output_path, csv_val_data)

    print(f"Processing seen data {val_file}")
    csv_val_seen_data = extract_seen_csv_data(val_data, seen_classes)
    output_path = os.path.join(output_folder, os.path.basename(val_file).replace(".json", "_seen.csv"))
    print(f"Output path: {output_path}")
    write_csv(output_path, csv_val_seen_data)

    print(f"Processing unseen data {val_file}")
    csv_val_unseen_data = extract_unseen_csv_data(val_data, unseen_classes)
    output_path = os.path.join(output_folder, os.path.basename(val_file).replace(".json", "_unseen.csv"))
    print(f"Output path: {output_path}")
    write_csv(output_path, csv_val_unseen_data)

    print("-" * 20)
    print(f"Analyzing train data {train_file}")

    image_count = len(train_data["images"])
    annotation_count = len(train_data["annotations"])
    category_count = len(train_data["categories"])

    category_in_annotations = set()
    for annotation in train_data["annotations"]:
        category_id = annotation["category_id"]
        category_in_annotations.add(category_id)
    
    print(f"Image count: {image_count}, Annotation count: {annotation_count}, Category count: {category_count}")
    print(f"There are {len(category_in_annotations)} categories in annotations")

    print("-" * 20)
    print(f"Analyzing val data {val_file}")

    image_count = len(val_data["images"])
    annotation_count = len(val_data["annotations"])
    category_count = len(val_data["categories"])

    category_in_annotations = set()
    seen_categories = set()
    unseen_categories = set()
    seen_annotation_count = 0
    unseen_annotation_count = 0
    for annotation in val_data["annotations"]:
        category_id = annotation["category_id"]
        category_in_annotations.add(category_id)
        if category_id in seen_classes:
            seen_categories.add(category_id)
            seen_annotation_count += 1
        elif category_id in unseen_classes:
            unseen_categories.add(category_id)
            unseen_annotation_count += 1
        else:
            raise ValueError(f"Category ID {category_id} not found in seen or unseen classes")
    
    print(f"Image count: {image_count}, Annotation count: {annotation_count}, Category count: {category_count}")
    print(f"There are {len(category_in_annotations)} categories in annotations")
    print(f"Seen categories: {len(seen_categories)}")
    print(f"Unseen categories: {len(unseen_categories)}")
    print(f"Seen annotation count: {seen_annotation_count}")
    print(f"Unseen annotation count: {unseen_annotation_count}")

    print(f"Finished")

if __name__ == "__main__":
    train_file = "json/intra_class_train.json"
    val_file = "json/intra_class_val.json"
    seen_file = "category/intra-class_seen.txt"
    unseen_file = "category/intra-class_unseen.txt"
    output_folder = "statistic/"
    main(train_file, val_file, seen_file, unseen_file, output_folder)