import json

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

def statistic_data(json_data, seen_classes:dict, unseen_classes:dict):
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





    return image_count, annotation_count, category_count