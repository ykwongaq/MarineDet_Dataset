from utils.util import *

def main(train_json_file:str, val_json_file:str):
    train_json_data = read_json(train_json_file)
    val_json_data = read_json(val_json_file)

    combine_images = train_json_data["images"] + val_json_data["images"]
    combine_annotations = train_json_data["annotations"] + val_json_data["annotations"]
    combine_categories = val_json_data["categories"]

    # Check all the image are unique
    image_ids = set()
    for image in combine_images:
        image_id = image["id"]
        assert image_id not in image_ids, f"Duplicate image id: {image_id}"
        image_ids.add(image_id)

    # Check all the annotation are unique
    annotation_ids = set()
    for annotation in combine_annotations:
        annotation_id = annotation["id"]
        assert annotation_id not in annotation_ids, f"Duplicate annotation id: {annotation_id}"
        annotation_ids.add(annotation_id)

    # Check all the category are unique
    category_ids = set()
    for category in combine_categories:
        category_id = category["id"]
        assert category_id not in category_ids, f"Duplicate category id: {category_id}"
        category_ids.add(category_id)


    combine_json_data = {
        "images": combine_images,
        "annotations": combine_annotations,
        "categories": combine_categories
    }

    output_file = "json\intra_class.json"
    write_json(output_file, combine_json_data)

if __name__ == "__main__":
    train_json_file = "json\intra_class_train.json"
    val_json_file = "json\intra_class_val.json"
    main(train_json_file, val_json_file)