import json
import os

from utils.util import *

def to_json(file:str):
    categories = []
    print(f"Processing {file}")
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            segments = line.strip().split(";")
            category_name = segments[1]
            categories.append(category_name)
    return categories


json_folder = "category/"
output_folder = "category_json/"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(json_folder):
    
    if not file.endswith(".txt"):
        continue

    if file == "category_id_to_class_id.txt":
        continue

    print(f"Processing {file}")

    file_path = os.path.join(json_folder, file)
    json_data = to_json(file_path)

    output_file = os.path.join(output_folder, file.replace(".txt", ".json"))

    write_json(output_file, json_data)


