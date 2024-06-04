from utils.util import *

def main(json_file:str):

    json_data = read_json(json_file)

    category_ids = []
    for cateogry in json_data["categories"]:
        category_ids.append(cateogry["id"])

    id_mapping = {}
    for new_id, id in enumerate(category_ids):
        id_mapping[id] = new_id

    for category in json_data["categories"]:
        category["id"] = id_mapping[category["id"]]

    for annotation in json_data["annotations"]:
        annotation["category_id"] = id_mapping[annotation["category_id"]]

    output_file = json_file.replace(".json", "_id_rearranged.json")
    print(f"Writing to {output_file}")
    write_json(output_file, json_data)


if __name__ == "__main__":
    json_file = 'json\intra_class_val_unseen.json'
    main(json_file)