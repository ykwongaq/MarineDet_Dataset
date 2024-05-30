from utils.util import *
import csv

def read_taxonomy_all(taxonomy_file):
    data = []
    with open(taxonomy_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(dict(row))
    
    CATEGORY_TO_CLASS = {}
    for d in data:
        category = d['Category']
        clazz = d['Class']
        if category == "" or clazz == "":
            continue
        CATEGORY_TO_CLASS[category] = clazz
    return CATEGORY_TO_CLASS

def main(category_file, class_file, taxonomy_file):
    ID_TO_CATEGORY_name = read_classes_file(category_file)
    ID_TO_CLASS = read_classes_file(class_file)

    CLASS_TO_ID = {
        class_name: class_id for class_id, class_name in ID_TO_CLASS.items()
    }

    CATEGORY_TO_CLASS = read_taxonomy_all(taxonomy_file) 

    CATEGORY_ID_TO_CLASS_ID = {}
    for category_id, category_name in ID_TO_CATEGORY_name.items():
        if category_name in CATEGORY_TO_CLASS:
            class_name = CATEGORY_TO_CLASS[category_name]
            if class_name in CLASS_TO_ID:
                class_id = CLASS_TO_ID[class_name]
                CATEGORY_ID_TO_CLASS_ID[category_id] = class_id
        else:
            print("Class name not found in taxonomy for ", category_name)

    output_file = "category/category_id_to_class_id.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        for category_id, class_id in CATEGORY_ID_TO_CLASS_ID.items():
            file.write(f"{category_id} {class_id}\n")
    






if __name__ == "__main__":
    category_file = "category/all_category_670.txt"
    class_file = "category/all_class_33.txt"
    taxonomy_file = "category/taxonomy_all.csv"
    main(category_file, class_file, taxonomy_file)