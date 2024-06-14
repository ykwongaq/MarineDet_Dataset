# import pandas for data wrangling
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.util import *
from distinctipy import distinctipy

def get_label_rotation(angle, offset):
    # Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle + offset)
    if angle <= np.pi:
        alignment = "right"
        rotation = rotation + 180
    else: 
        alignment = "left"
    return rotation, alignment

def add_labels(angles, values, labels, offset, ax):
    
    # This is the space between the end of the bar and the label
    padding = 4
    
    # Iterate over angles, values, and labels, to add all of them.
    for angle, value, label, in zip(angles, values, labels):
        angle = angle
        
        # Obtain text rotation and alignment
        rotation, alignment = get_label_rotation(angle, offset)

        # And finally add the text
        ax.text(
            x=angle, 
            y=value + padding, 
            s=label, 
            ha=alignment, 
            va="center", 
            rotation=rotation, 
            rotation_mode="anchor"
        ) 


def main(json_file:str, mapping_file:str, class_file:str):

    json_data = read_json(json_file)

    ID_TO_NAME = {}
    for category in json_data["categories"]:
        ID_TO_NAME[category["id"]] = category["name"]
    # print(f"ID_TO_NAME: {len(ID_TO_NAME)}")
    ID_TO_COUNT = {}
    # Initialize the dictionary with the categories
    for category in json_data["categories"]:
        ID_TO_COUNT[category["id"]] = 0
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        ID_TO_COUNT[category_id] = ID_TO_COUNT.get(category_id, 0) + 1
    # print(f"ID_TO_COUNT: {len(ID_TO_COUNT)}")

    CATEGORY_ID_TO_CLASS_ID = {}
    with open(mapping_file, "r") as f:
        for line in f:
            category_id, class_id = line.strip().split(" ")
            CATEGORY_ID_TO_CLASS_ID[int(category_id)] = int(class_id)

    CLASS_ID_TO_NAME = {}
    class_data = read_json(class_file)
    for category in class_data["categories"]:
        CLASS_ID_TO_NAME[category["id"]] = category["name"]

    CATEGORY_ID_TO_CLASS_NAME = {}
    for category_id, class_id in CATEGORY_ID_TO_CLASS_ID.items():
        CATEGORY_ID_TO_CLASS_NAME[category_id] = CLASS_ID_TO_NAME[class_id]
    # print(f"CATEGORY_ID_TO_CLASS_NAME: {len(CATEGORY_ID_TO_CLASS_NAME)}")

    # Filter out the data by category id that is not in the CATEGORY_ID_TO_CLASS_ID
    ID_TO_COUNT = {k: v for k, v in ID_TO_COUNT.items() if k in CATEGORY_ID_TO_CLASS_ID}
    # print(f"ID_TO_COUNT: {len(ID_TO_COUNT)}")
    ID_TO_NAME = {k: v for k, v in ID_TO_NAME.items() if k in CATEGORY_ID_TO_CLASS_ID}
    # print(f"ID_TO_NAME: {len(ID_TO_NAME)}")

    # Sort the data by category id
    ID_TO_COUNT = dict(sorted(ID_TO_COUNT.items(), key=lambda item: item[0]))
    ID_TO_NAME = dict(sorted(ID_TO_NAME.items(), key=lambda item: item[0]))
    CATEGORY_ID_TO_CLASS_NAME = dict(sorted(CATEGORY_ID_TO_CLASS_NAME.items(), key=lambda item: item[0]))

    # We only display top 10 class in the figure, so that we will filter out the others
    limit = 40
    CLASS_ID_TO_COUNT = {}
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        if category_id not in CATEGORY_ID_TO_CLASS_ID:
            continue
        class_id = CATEGORY_ID_TO_CLASS_ID[category_id]
        CLASS_ID_TO_COUNT[class_id] = CLASS_ID_TO_COUNT.get(class_id, 0) + 1

    CLASS_ID_TO_COUNT = dict(sorted(CLASS_ID_TO_COUNT.items(), key=lambda item: item[1], reverse=True))
    CLASS_ID_TO_COUNT = dict(list(CLASS_ID_TO_COUNT.items())[:limit])

    ID_TO_COUNT = {k: v for k, v in ID_TO_COUNT.items() if CATEGORY_ID_TO_CLASS_ID[k] in CLASS_ID_TO_COUNT}
    ID_TO_NAME = {k: v for k, v in ID_TO_NAME.items() if CATEGORY_ID_TO_CLASS_ID[k] in CLASS_ID_TO_COUNT}
    CATEGORY_ID_TO_CLASS_NAME = {k: v for k, v in CATEGORY_ID_TO_CLASS_NAME.items() if k in ID_TO_NAME}

    rng = np.random.default_rng(123)    
    # Build a dataset
    df = pd.DataFrame({
        "name": [ID_TO_NAME[i] for i in ID_TO_COUNT.keys()],
        "value": [ID_TO_COUNT[i] for i in ID_TO_COUNT.keys()],
        "group": [CATEGORY_ID_TO_CLASS_NAME[i] for i in ID_TO_COUNT.keys()],
    })

    df = df.sort_values(by='group')

    # print(df)
    # All this part is like the code above
    VALUES = df["value"].values
    LABELS = df["name"].values
    GROUP = df["group"].values

    PAD = 3
    ANGLES_N = len(VALUES) + PAD * len(np.unique(GROUP))
    ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
    WIDTH = (2 * np.pi) / len(ANGLES)

    GROUPS_SIZE = [len(i[1]) for i in df.groupby("group")]

    offset = 0
    IDXS = []
    for size in GROUPS_SIZE:
        IDXS += list(range(offset + PAD, offset + size + PAD))
        offset += size + PAD

    # Determines where to place the first bar. 
    # By default, matplotlib starts at 0 (the first bar is horizontal)
    # but here we say we want to start at pi/2 (90 deg)
    OFFSET = np.pi / 2

    fig, ax = plt.subplots(figsize=(25, 10), subplot_kw={"projection": "polar"})
    ax.set_theta_offset(OFFSET)
    ax.set_ylim(-100, 100)
    ax.set_frame_on(False)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Generate a set of distinct colors
    num_groups = len(df['group'].unique())
    colors = distinctipy.get_colors(num_groups)

    GROUPS_SIZE = [len(i[1]) for i in df.groupby("group")]

    # Assign distinct colors to each item in the group
    COLORS = [colors[i] for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]

    # GROUPS_SIZE = [len(i[1]) for i in df.groupby("group")]

    # COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]

    ax.bar(
        ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS, 
        # edgecolor="white", linewidth=2
        linewidth=1
    )

    # Create a legend for the groups
    group_labels = sorted(list(df["group"].unique()))
    # Map group names to colors
    group_color_map = {group: COLORS[df['group'].tolist().index(group)] for group in group_labels}
    handles = [plt.Rectangle((0,0),1,1, color=group_color_map[group]) for group in group_labels]
    ax.legend(handles, group_labels, loc='upper right', bbox_to_anchor=(2.0, 1.0), ncol=5, title="Classes", fontsize="small")

    # add_labels(ANGLES[IDXS], VALUES, LABELS, OFFSET, ax)

    # Extra customization below here --------------------

    # This iterates over the sizes of the groups adding reference
    # lines and annotations.

    offset = 0 
    for group, size in zip(df["group"], GROUPS_SIZE):
        # Add line below bars
        x1 = np.linspace(ANGLES[offset + PAD], ANGLES[offset + size + PAD - 1], num=50)
        ax.plot(x1, [-5] * 50, color="#333333")

        offset += size + PAD

    output_file = "vis/diversity.png"
    print(f"Saving plot to {output_file}...")
    plt.savefig(output_file, bbox_inches='tight')

if __name__ == "__main__":
    json_file = "final.json"
    id_mapping = "category\category_id_to_class_id.txt"
    class_file = "json\class_level_val.json"
    main(json_file, id_mapping, class_file)