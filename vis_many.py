import argparse
import os
import random

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from tqdm import tqdm

from utils.util import *


def main(args):

    json_file = args.json_file
    json_data = read_json(json_file)

    bbox_limit = args.bbox_limit
    caption_len_limit = args.caption_len_limit
    category_name_len_limit = args.category_name_len_limit

    CATEGORY_ID_TO_NAME = {}
    for category in json_data['categories']:
        CATEGORY_ID_TO_NAME[category['id']] = category['name']

    IMAGE_ID_TO_FILE_NAME = {}
    for image in json_data['images']:
        IMAGE_ID_TO_FILE_NAME[image['id']] = image['file_name']

    # Filter out the images that contain too much bounding box
    IMAGE_BBOX_COUNT = {}
    for annotation in json_data['annotations']:
        image_id = annotation['image_id']
        if image_id not in IMAGE_BBOX_COUNT:
            IMAGE_BBOX_COUNT[image_id] = 0
        IMAGE_BBOX_COUNT[image_id] += 1
    
    filtered_image_ids = []
    for image_id, bbox_count in IMAGE_BBOX_COUNT.items():
        if bbox_count <= bbox_limit:
            filtered_image_ids.append(image_id)

    annotations = json_data['annotations']
    
    filtered_annotations = []
    for annotation in tqdm(annotations, desc="Filtering annotations"):
        image_id = annotation['image_id']
        if image_id not in filtered_image_ids:
            continue

        if len(annotation['caption'].split()) > caption_len_limit:
            continue
        
        category_name = CATEGORY_ID_TO_NAME[annotation['category_id']]
        if len(category_name) > category_name_len_limit:
            continue

        if annotation["area"] < 32*32:
            continue

        if annotation["label"] != 2:
            continue
        
        filtered_annotations.append(annotation)
    
    print(f"Number of filtered annotations: {len(filtered_annotations)}")

    # Visualize the data
    num_annotation = args.num

    vis_annotations = random.sample(filtered_annotations, num_annotation)
    for idx, vis_annotation in enumerate(vis_annotations):
        output_width_px, output_height_px = 640, 480
        dpi = 100

        output_width_in = output_width_px / dpi
        output_height_in = output_height_px / dpi

        fig, ax = plt.subplots(1, figsize=(output_width_in, output_height_in), dpi=dpi)
        # Remove whitespace and fill the result image
        image_id = vis_annotation['image_id']
        image_file = IMAGE_ID_TO_FILE_NAME[image_id]
        image = plt.imread(image_file)
        ax.imshow(image)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        # Set the aspect ratio of the axes to be equal
        ax.set_aspect('auto')
        rect = patches.Rectangle((vis_annotation['bbox'][0], vis_annotation['bbox'][1]), vis_annotation['bbox'][2], vis_annotation['bbox'][3], linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.axis("off")

        bbox = vis_annotation["bbox"]
        category_name = CATEGORY_ID_TO_NAME[vis_annotation['category_id']]
        ax.text(bbox[0]+5, bbox[1]-10, f"{category_name}", fontsize=13, color="white", backgroundcolor="red")
        print("-"*40)
        print(f"Image: {image_file}")
        print(f"Caption: {vis_annotation['caption']}")
        print(f"Category: {CATEGORY_ID_TO_NAME[vis_annotation['category_id']]}")

        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, f"vis_{idx}.png")
        print(f"Saving the visualization to {output_file}")
        plt.tight_layout()
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0, transparent=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize the data')
    parser.add_argument('--json_file', type=str, default="final.json", help='json file path')
    parser.add_argument('--bbox_limit', type=int, default=3, help='bbox limit')
    parser.add_argument('--output_dir', type=str, default="vis", help='output directory')
    parser.add_argument('--caption_len_limit', type=int, default=40, help='caption length limit')
    parser.add_argument('--category_name_len_limit', type=int, default=14, help='category name length limit')
    parser.add_argument("--num", type=int, default=10, help="Number of visualizations")
    
    args = parser.parse_args()
    main(args)