from utils.util import *

def main(json_file:str, ref_json_file):

    json_data = read_json(json_file)

    ref_json_data = read_json(ref_json_file)

    annotation_ids = set()
    for annotation in json_data["annotations"]:
        annotation_ids.add(annotation["id"])

    mapping = {}
    for annotaiton in ref_json_data["annotations"]:
        if annotaiton["id"] in annotation_ids:
            mapping[annotaiton["id"]] = annotaiton["segmentation"]

    for annotation in json_data["annotations"]:
        annotation["segmentation"] = mapping[annotation["id"]]

    # Make sure that all the annotation have segmentation
    for annotation in json_data["annotations"]: 
        assert annotation["segmentation"] != [], f"Annotation {annotation['id']} does not have segmentation."

    output_path = json_file.replace(".json", "_segmentation.json")
    write_json(output_path, json_data)

if __name__ == "__main__":
    json_file = "json\intra_class_val_unseen.json"
    ref_json_file = "combined_processed.json"
    main(json_file, ref_json_file)