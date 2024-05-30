from utils.util import *

def check_all_images_unique(json_data):
    image_ids = set()
    for image in json_data["images"]:
        image_id = image["id"]
        assert image_id not in image_ids, f"Image ID {image_id} is not unique"
        image_ids.add(image_id)
    assert len(image_ids) == len(json_data["images"]), f"Images are not unique"

def check_all_annotation_unique(json_data):
    annotation_ids = set()
    for annotation in json_data["annotations"]:
        annotation_id = annotation["id"]
        assert annotation_id not in annotation_ids, f"Annotation ID {annotation_id} is not unique"
        annotation_ids.add(annotation_id)
    assert len(annotation_ids) == len(json_data["annotations"]), f"Annotations are not unique"

def check_all_category_unique(json_data):
    category_ids = set()
    for category in json_data["categories"]:
        category_id = category["id"]
        assert category_id not in category_ids, f"Category ID {category_id} is not unique"
        category_ids.add(category_id)
    assert len(category_ids) == len(json_data["categories"]), f"Categories are not unique"

def check_annotation_have_corresponding_image(json_data):
    image_ids = set()
    for image in json_data["images"]:
        image_id = image["id"]
        image_ids.add(image_id)

    for annotation in json_data["annotations"]:
        image_id = annotation["image_id"]
        assert image_id in image_ids, f"Image ID {image_id} not found in images"
    

def check_categories_contain_all_id(json_data):
    categories_id = set()
    for category in json_data["categories"]:
        category_id = category["id"]  
        categories_id.add(category_id) 

    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        assert category_id in categories_id, f"Category ID {category_id} not found in categories"
        

def check_annotation_have_area_iscrowd(json_data):
    for annotation in json_data["annotations"]:
        assert "area" in annotation, f"Area not found in annotation {annotation}"
        assert "iscrowd" in annotation, f"Iscrowd not found in annotation {annotation}" 

def check_json_does_not_have_unseen_classes(json_data, unseen_classes:dict):
    unseen_category_ids = set(unseen_classes.keys())
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        assert category_id not in unseen_category_ids, f"Category ID {category_id} found in unseen classes"

def main(json_file, seen_file, unseen_file):
    
    json_data = read_json(json_file)

    seen_classes = read_classes_file(seen_file)
    unseen_classes = read_classes_file(unseen_file)

    print("Checking all images are unique")
    check_all_images_unique(json_data)

    print("Checking all annotations are unique")
    check_all_annotation_unique(json_data)

    print("Checking all categories are unique")
    check_all_category_unique(json_data)

    print("Checking all annotations have corresponding image")
    check_annotation_have_corresponding_image(json_data)

    print("Checking categories contain all id")
    check_categories_contain_all_id(json_data)

    print("Checking annotations have area and iscrowd")
    check_annotation_have_area_iscrowd(json_data)

    print("Checking json does not have unseen classes")
    check_json_does_not_have_unseen_classes(json_data, unseen_classes)

    print(f"Satistic data for {json_file}")
    statistic_data(json_data, seen_classes, unseen_classes)



if __name__ == "__main__":
    json_file = "json/intra_class_train.json"
    seen_file = "category/intra-class_seen.txt"
    unseen_file = "category/intra-class_unseen.txt"
    main(json_file, seen_file, unseen_file)