import json
import os

json_folder = "category_json"

for file in os.listdir(json_folder):
    if not file.endswith(".json"):
        continue

    file_path = os.path.join(json_folder, file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"File: {file}, category_count: {len(data)}")
    