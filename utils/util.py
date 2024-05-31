import json
import random

def read_json(file:str):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)
    
def write_json(file:str, json_data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(json_data, f)

    
def read_classes_file(file:str):
    ID_TO_NAME = {}
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            segments = line.strip().split(";")
            class_id = int(segments[0])
            class_name = segments[1]
            ID_TO_NAME[class_id] = class_name
    return ID_TO_NAME

def categories_to_coco(categories:dict):
    coco_categories = []
    for id, name in categories.items():
        category = {
            "id": id,
            "name": name,
            "supercategory": name,
        }
        coco_categories.append(category)
    return coco_categories

def extract_json_data(json_data:str, classes_mapping:dict):
    target_class_ids = set(classes_mapping.keys())

    extracted_annotations = []
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        if category_id in target_class_ids:
            extracted_annotations.append(annotation)
    
    extracted_image_ids = set()
    for annotation in extracted_annotations:
        image_id = annotation["image_id"]
        extracted_image_ids.add(image_id)

    extracted_images = []
    for image in json_data["images"]:
        image_id = image["id"]
        if image_id in extracted_image_ids:
            extracted_images.append(image)

    categories = categories_to_coco(classes_mapping)
    
    extracted_json_data = {
        "images": extracted_images,
        "annotations": extracted_annotations,
        "categories": categories,
    }

    return extracted_json_data

def remove_overlapping_data(train_json_data, val_json_data):
    # There may have some overlapping images between train and val set
    # If there are any overlapping images, then remove them from the train set and keep them in the val set
    train_image_ids = set()
    for image in train_json_data["images"]:
        image_id = image["id"]
        train_image_ids.add(image_id)

    val_image_ids = set()
    for image in val_json_data["images"]:
        image_id = image["id"]
        val_image_ids.add(image_id)

    overlapping_image_ids = train_image_ids.intersection(val_image_ids)
    train_image_ids -= overlapping_image_ids

    # Collect training images and annotation based on the image ids
    train_images = []
    val_images = []
    for image in train_json_data["images"]:
        image_id = image["id"]
        if image_id in train_image_ids:
            train_images.append(image)
        else:
            val_images.append(image)

    for image in val_json_data["images"]:
        image_id = image["id"]
        if image_id in val_image_ids:
            val_images.append(image)
        else:
            train_images.append(image)

    # Collect training annotations and validation annotations based on the image ids
    train_annotations = []
    val_annotations = []
    for annotation in train_json_data["annotations"]:
        image_id = annotation["image_id"]
        if image_id in train_image_ids:
            train_annotations.append(annotation)
        else:
            val_annotations.append(annotation)

    for annotation in val_json_data["annotations"]:
        image_id = annotation["image_id"]
        if image_id in val_image_ids:
            val_annotations.append(annotation)
        else:
            train_annotations.append(annotation)
    
    train_json_data = {
        "images": train_images,
        "annotations": train_annotations,
        "categories": train_json_data["categories"]
    }

    val_json_data = {
        "images": val_images,
        "annotations": val_annotations,
        "categories": val_json_data["categories"]
    }

    return train_json_data, val_json_data



def split_json_data(json_data, train_ratio:float):
    # Split the json_data based on images
    images = json_data["images"]
    random.shuffle(images)

    train_image_count = int(len(images) * train_ratio)
    train_images = images[:train_image_count]
    val_images = images[train_image_count:]

    # Collect training image ids and validation image ids
    train_image_ids = set()
    for image in train_images:
        train_image_ids.add(image["id"])
    
    val_image_ids = set()
    for image in val_images:
        val_image_ids.add(image["id"])
    
    # If there are overlapping image ids, then remove them from train set and keep them in val set
    overlapping_image_ids = train_image_ids.intersection(val_image_ids)
    train_image_ids -= overlapping_image_ids

    # Collect training images and annotation based on the image ids
    training_images = []
    val_images = []
    for image in json_data["images"]:
        image_id = image["id"]
        if image_id in train_image_ids:
            training_images.append(image)
        else:
            val_images.append(image)

    train_annotations = []
    val_annotations = []
    for annotation in json_data["annotations"]:
        image_id = annotation["image_id"]
        if image_id in train_image_ids:
            train_annotations.append(annotation)
        else:
            val_annotations.append(annotation)

    train_json_data = {
        "images": training_images,
        "annotations": train_annotations,
        "categories": json_data["categories"]
    }

    val_json_data = {
        "images": val_images,
        "annotations": val_annotations,
        "categories": json_data["categories"]
    }
    
    return train_json_data, val_json_data

def remove_duplicate_json_data(json_data):
    # Remove duplicate images
    image_ids = set()
    unique_images = []
    for image in json_data["images"]:
        image_id = image["id"]
        if image_id not in image_ids:
            unique_images.append(image)
            image_ids.add(image_id)

    # Remove duplicate annotations
    annotation_ids = set()
    unique_annotations = []
    for annotation in json_data["annotations"]:
        annotation_id = annotation["id"]
        if annotation_id not in annotation_ids:
            unique_annotations.append(annotation)
            annotation_ids.add(annotation_id)

    # Create a new json data
    new_json_data = {
        "images": unique_images,
        "annotations": unique_annotations,
        "categories": json_data["categories"]
    }

    return new_json_data

def join_json_data(json_data1, json_data2):
    # Join the images, annotations, and categories
    images = json_data1["images"] + json_data2["images"]
    annotations = json_data1["annotations"] + json_data2["annotations"]
    categories = json_data1["categories"] + json_data2["categories"]

    # Create a new json data
    new_json_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    return new_json_data


def statistic_data(json_data, seen_classes:dict = None, unseen_classes:dict = None):
    image_count = len(json_data["images"]) 
    annotation_count = len(json_data["annotations"])
    category_count = len(json_data["categories"])

    print(f"Image count: {image_count}, Annotation count: {annotation_count}, Category count: {category_count}")

    if seen_classes is None or unseen_classes is None:
        return
    
    seen_category_ids = set(seen_classes.keys())
    unseen_category_ids = set(unseen_classes.keys())

    seen_annotation_count = 0
    unseen_annotation_count = 0
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        if category_id in seen_category_ids:
            seen_annotation_count += 1
        elif category_id in unseen_category_ids:
            unseen_annotation_count += 1
        else:
            raise Exception(f"Category ID {category_id} not found in seen or unseen classes")
    
    print(f"Seen annotation count: {seen_annotation_count}, Unseen annotation count: {unseen_annotation_count}")

    # Count the number of sample of each seen classes
    seen_class_samples = {}
    for id, name in seen_classes.items():
        seen_class_samples[id, name] = 0

    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        if category_id in seen_category_ids:
            seen_class_samples[category_id, seen_classes[category_id]] += 1

    # Sort the seen_class_samples based on the class id
    seen_class_samples = dict(sorted(seen_class_samples.items(), key=lambda x: x[0][0]))

    print()
    print("Seen class samples:")
    for (id, name), count in seen_class_samples.items():
        print(f"ID: {id} Class: {name}, Count: {count}")

    # Print out the classes that have no samples
    print()
    print("Seen classes that does not have instances")
    no_instance_seen_class_count = 0 
    for (id, name), count in seen_class_samples.items():
        if seen_class_samples[id, name] == 0:
            print(f"ID: {id} Class: {name}")
            no_instance_seen_class_count += 1
    print(f"Total: {no_instance_seen_class_count}")

    # Count the number of samples of each unseen classes
    unseen_class_samples = {}
    for id, name in unseen_classes.items():
        unseen_class_samples[id, name] = 0
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        if category_id in unseen_category_ids:
            unseen_class_samples[category_id, unseen_classes[category_id]] += 1
    
    # Sort the seen_class_samples based on the class id
    unseen_class_samples = dict(sorted(unseen_class_samples.items(), key=lambda x: x[0][0]))

    print()
    print("Unseen class samples:")
    for (id, name), count in unseen_class_samples.items():
        print(f"ID: {id} Class: {name}, Count: {count}")

    # Print out the classes that have no samples
    print()
    print("Unseen classes that does not have instances")
    no_instance_unseen_class_count = 0
    for (id, name), count in unseen_class_samples.items():
        if unseen_class_samples[id, name] == 0:
            print(f"ID: {id} Class: {name}")
            no_instance_unseen_class_count += 1
    print(f"Total: {no_instance_unseen_class_count}")

def write_txt(file:str, lines:list):
    with open(file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")