from utils.util import *

def remove_annotation(json_data, classes):
    class_ids_to_remove = set()
    for id, name in classes.items():
        class_ids_to_remove.add(id)
    
    filtered_annotations = []
    for annotation in json_data["annotations"]:
        if annotation["category_id"] not in class_ids_to_remove:
            filtered_annotations.append(annotation)

    filtered_images_ids = set()
    for annotation in filtered_annotations:
        filtered_images_ids.add(annotation["image_id"])

    filtered_images = []
    for image in json_data["images"]:
        if image["id"] in filtered_images_ids:
            filtered_images.append(image)

    filtered_categories = []
    for category in json_data["categories"]:
        if category["id"] not in class_ids_to_remove:
            filtered_categories.append(category)
    
    filtered_dataset = {
        "images": filtered_images,
        "annotations": filtered_annotations,
        "categories": filtered_categories
    }

    return filtered_dataset
    


def main(json_file:str, seen_file:str, unseen_file:str):
    json_data = read_json(json_file)

    seen_classes = read_classes_file(seen_file)
    unseen_classes = read_classes_file(unseen_file)

    seen_data = extract_json_data(json_data, seen_classes)
    unseen_data = extract_json_data(json_data, unseen_classes)

    seen_data = remove_annotation(seen_data, unseen_classes)
    unseen_data = remove_annotation(unseen_data, seen_classes)

    # Verify that seen_data does not contain any unseen classes
    seen_data_classes = set()
    for category in seen_data["categories"]:
        seen_data_classes.add(category["id"])
    for unseen_id, _ in unseen_classes.items():
        assert unseen_id not in seen_data_classes, f"Class {unseen_id} is present in seen data" 

    seen_data_classes = set()
    for annotation in seen_data["annotations"]:
        seen_data_classes.add(annotation["category_id"])
    for unseen_id, _ in unseen_classes.items():
        assert unseen_id not in seen_data_classes, f"Class {unseen_id} is present in seen data"


    # Verify that unseen_data does not contain any seen classes
    unseen_data_classes = set()
    for category in unseen_data["categories"]:
        unseen_data_classes.add(category["id"])
    for seen_id, _ in seen_classes.items():
        assert seen_id not in unseen_data_classes, f"Class {seen_id} is present in unseen data"

    unseen_data_classes = set()
    for annotation in unseen_data["annotations"]:
        unseen_data_classes.add(annotation["category_id"])
    for seen_id, _ in seen_classes.items():
        assert seen_id not in unseen_data_classes, f"Class {seen_id} is present in unseen data"

    val_seen_output_file = json_file.replace(".json", "_seen.json")
    print(f"Writing seen data to {val_seen_output_file}")
    write_json(val_seen_output_file, seen_data)

    val_unseen_output_file = json_file.replace(".json", "_unseen.json")
    print(f"Writing unseen data to {val_unseen_output_file}")
    write_json(val_unseen_output_file, unseen_data)


if __name__ == "__main__":
    json_file = "json\inter_class_val.json"
    seen_file = "category\inter-class_seen.txt"
    unseen_file = "category\inter-class_unseen.txt"
    output_folder = "json"
    main(json_file, seen_file, unseen_file) 