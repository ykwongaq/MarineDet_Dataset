from utils.util import *
import os

def main(files:str):
    for file in files:
        json_data = read_json(file)
        for annotation in json_data["annotations"]:
            area = annotation["area"]
            if area < 32*32:
                annotation["label"] = -1
                annotation["negative_tags"] = ""
    
        output_file = file
        write_json(output_file, json_data)

if __name__ == "__main__":

    files = []
    files.append("final.json")

    folder = "json"
    for file in os.listdir(folder):
        if file.endswith(".json"):
            files.append(os.path.join(folder, file))
    
    main(files)
    