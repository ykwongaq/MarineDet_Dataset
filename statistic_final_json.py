from utils.util import *
from utils.statistic import *
import os
import re

from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords

LOG = []

def log(message):
    print(message)
    LOG.append(message)

def main(json_file:str, output_folder:str):

    os.makedirs(output_folder, exist_ok=True)

    print(f"Processing json file {json_file}")
    json_data = read_json(json_file)

    log("---- Images ----")

    image_count = count_images(json_data)
    log(f"Image count: {image_count}")

    avg_img_h, avg_img_w = measure_image_resolution(json_data)
    log(f"Average image height: {avg_img_h}, Average image width: {avg_img_w}")

    log("---- Captions ----")
    caption_count = count_caption(json_data)
    log(f"Caption count: {caption_count}")

    avg_caption_length = measure_caption_length(json_data)
    log(f"Average caption length: {avg_caption_length}")

    vocab_size_dataset = mesure_vocabulary_size_dataset(json_data)
    log(f"Vocabulary size (dataset): {vocab_size_dataset}")

    vocab_size_per_image = mesure_vocabulary_size_per_image(json_data)
    log(f"Vocabulary size (per image): {vocab_size_per_image}")

    top = 30
    words, counts = measure_top_common_words(json_data, top)
    log(f"Top {top} common words:")
    for word, count in zip(words, counts):
        log(f"{word}: {count}")
    
    log("---- Categories ----")

    category_count = count_declared_categories(json_data)
    log(f"Category count: {category_count}")

    category_with_instance_count = count_categories_with_instance(json_data)
    log(f"Category with instance count: {category_with_instance_count}")

    category_instance_count = count_categories_instances(json_data)
    log("Category instances:")
    log(f"{category_instance_count}")

    log("---- Bounding Box ----")
    bbox_count = count_bbox(json_data)
    log(f"Bounding box count: {bbox_count}")

    small_bbox_count = count_small_bbox(json_data)
    log(f"Small bounding box count: {small_bbox_count}")

    medium_bbox_count = count_medium_bbox(json_data)
    log(f"Medium bounding box count: {medium_bbox_count}")

    large_bbox_count = count_large_bbox(json_data)
    log(f"Large bounding box count: {large_bbox_count}")

    bbox_count_per_image = count_bbox_per_image(json_data)
    log(f"Bounding box count per image: {bbox_count_per_image}")

    small_bbox_count_per_image = count_small_bbox_per_image(json_data)
    log(f"Small bounding box count per image: {small_bbox_count_per_image}")

    medium_bbox_count_per_image = count_medium_bbox_per_image(json_data)
    log(f"Medium bounding box count per image: {medium_bbox_count_per_image}")

    large_bbox_count_per_image = count_large_bbox_per_image(json_data)
    log(f"Large bounding box count per image: {large_bbox_count_per_image}")

    log("---- Label ----")
    generated_positive_count = count_generated_positive_label(json_data)
    log(f"Generated positive label count: {generated_positive_count}")

    generated_negative_count = count_generated_negative_label(json_data)
    log(f"Generated negative label count: {generated_negative_count}")

    refined_positive_count = count_refined_positive_label(json_data)
    log(f"Refined positive label count: {refined_positive_count}")

    not_labeled_count = count_not_labeled_label(json_data)
    log(f"Not labeled count: {not_labeled_count}")

    
    log("---- Negative Tags ----")
    different_negative_tags = count_different_negative_tags(json_data)
    log(f"Different negative tags: {different_negative_tags}")

    tags_count = count_negative_tags(json_data)
    for tag, count in tags_count.items():
        log(f"{tag}: {count}")

    tags_count_per_image = count_negative_tags_per_image(json_data)
    log(f"Negative tags per image: {tags_count_per_image}")

    assert len(json_data["annotations"]) == generated_positive_count + generated_negative_count + refined_positive_count + not_labeled_count, f"Annotation count: {len(json_data['annotations'])}, Generated positive count: {generated_positive_count}, Generated negative count: {generated_negative_count}, Refined positive count: {refined_positive_count}, Not labeled count: {not_labeled_count}"
    assert caption_count == medium_bbox_count + large_bbox_count, f"Caption count: {caption_count}, Medium bbox count: {medium_bbox_count}, Large bbox count: {large_bbox_count}"
    assert not_labeled_count == small_bbox_count, f"Not labeled count: {not_labeled_count}, Small bbox count: {small_bbox_count}"
    assert medium_bbox_count + large_bbox_count == generated_positive_count + generated_negative_count + refined_positive_count, f"Medium bbox count: {medium_bbox_count}, Large bbox count: {large_bbox_count}, Generated positive count: {generated_positive_count}, Generated negative count: {generated_negative_count}, Refined positive count: {refined_positive_count}"

    output_path = os.path.join(output_folder, os.path.basename(json_file).replace(".json", "_statistic.txt"))
    write_txt(output_path, LOG)



if __name__ == "__main__":
    json_file = "final.json"
    output_folder = "statistic/"
    main(json_file, output_folder)