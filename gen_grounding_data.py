from utils.util import *
from utils.statistic import *

def filter(json_data):
    annotation_to_keep = []
    for annotation in json_data["annotations"]:
        if annotation["label"] != GENERATED_NEGATIVE and annotation["caption"] != "":
            annotation_to_keep.append(annotation)

    image_ids_to_keep = set()
    for annotation in annotation_to_keep:
        image_ids_to_keep.add(annotation["image_id"])

    images_to_keep = []
    for image in json_data["images"]:
        if image["id"] in image_ids_to_keep:
            images_to_keep.append(image)

    new_json_data = {
        "images": images_to_keep,
        "annotations": annotation_to_keep,
        "categories": json_data["categories"]
    }

    return new_json_data

def count_number_of_annotations(json_data):
    return len(json_data["annotations"])

def count_number_of_negative_annotation(json_data):
    count = 0
    for annotation in json_data["annotations"]:
        if annotation["label"] == GENERATED_NEGATIVE:
            count += 1
    return count

SMALL_BBOX_THRESHOLD = 32*32

def count_number_of_small_bbox(json_data):
    count = 0
    for annotation in json_data["annotations"]:
        if annotation["bbox"][2] * annotation["bbox"][3] < SMALL_BBOX_THRESHOLD:
            count += 1
    return count

def main(json_files:str):
    
    for file in json_files:
        print(f"Processing {file}")
        json_data = read_json(file)

        num_annotations = count_number_of_annotations(json_data)
        num_negative_annotations = count_number_of_negative_annotation(json_data)
        num_small_annotations = count_number_of_small_bbox(json_data)

        print(f"Number of annotations: {num_annotations}")
        print(f"Number of negative annotations: {num_negative_annotations}")

        new_json_data = filter(json_data)

        new_num_annotations = count_number_of_annotations(new_json_data)
        print(f"Number of annotations after removing negative captions: {new_num_annotations}")

        # assert new_num_annotations == num_annotations - num_negative_annotations - num, f"Number of annotations does not match. {new_num_annotations} != {num_annotations - num_negative_annotations}"
        # assert count_number_of_negative_annotation(new_json_data) == 0, "There are still negative captions in the dataset."
        
        output_path = file.replace(".json", "_grounding.json")
        print(f"Writing to {output_path}")
        write_json(output_path, new_json_data)


if __name__ == "__main__":

    files = [
        "json/class_level_train.json",
        "json/class_level_val_seen.json",
        "json/class_level_val_unseen.json",
        "json/class_level_val.json",
        "json/inter_class_train.json",
        "json/inter_class_val_seen.json",
        "json/inter_class_val_unseen.json",
        "json/inter_class_val.json",
        "json/intra_class_train.json",
        "json/intra_class_val_seen.json",
        "json/intra_class_val_unseen.json",
        "json/intra_class_val.json",
    ]

    main(files)