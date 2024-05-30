import os

from utils.util import *

def clean_json(json_data):
    for annotation in json_data["annotations"]:
        annotation.pop("point_coords", None)
        annotation.pop("point_coords_label", None)
        annotation.pop("category", None)
    return json_data

def main():
    input_json_file = "final_v3_processed.json"
    output_json_file = "./final.json"

    json_data = read_json(input_json_file)
    json_data = clean_json(json_data)

    category_path = "category/all_category_670.txt"
    ID_TO_CATEGORY = read_classes_file(category_path)

    categories = []
    for id, category in ID_TO_CATEGORY.items():
        print(f"Adding category {category} with id {id}")
        categories.append({
            "id": id,
            "name": category,
            "supercategory": category
        })

    new_json_data = {
        "images": json_data["images"],
        "annotations": json_data["annotations"],
        "categories": categories
    }

    print(f"Writing to {output_json_file}")
    write_json(output_json_file, new_json_data)

if __name__ == "__main__":
    main()


