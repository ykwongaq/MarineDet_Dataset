import re

from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords

GENERATED_POSITIVE = 0
GENERATED_NEGATIVE = 1
REFINED_POSITIVE = 2
NOT_LABELED = -1

def count_images(json_data):
    return len(json_data["images"])

def measure_image_resolution(json_data):
    heights = []
    widths = []
    for image in json_data["images"]:
        heights.append(image["height"])
        widths.append(image["width"])
    
    avg_height = sum(heights) / len(heights)
    avg_width = sum(widths) / len(widths)

    return avg_height, avg_width

def count_caption(json_data):
    caption_count  = 0
    for annotation in json_data["annotations"]:
        if annotation["caption"] != "":
            caption_count += 1
    return caption_count

def measure_caption_length(json_data):
    caption_lengths = []
    for annotation in json_data["annotations"]:
        caption = annotation["caption"]

        if annotation["area"] < 32*32:
            continue

        caption_lengths.append(len(caption.split()))
    return sum(caption_lengths) / len(caption_lengths)

def mesure_vocabulary_size_dataset(json_data):
    unique_words = set()

    captions = []
    for annotation in json_data["annotations"]:
        caption = annotation["caption"]
        if annotation["area"] < 32*32:
            continue
        captions.append(caption)
    
    for caption in captions:
        tokens = word_tokenize(caption.lower())
        words = [word for word in tokens if word.isalpha()]
        unique_words.update(words)
    
    return len(unique_words)

def mesure_vocabulary_size_per_image(json_data):
    vocab_sizes = []

    captions = []
    for annotation in json_data["annotations"]:
        if annotation["area"] >= 32*32:
            caption = annotation["caption"]
            captions.append(caption)

    for caption in captions:
        unique_words = set()
        tokens = word_tokenize(caption.lower())
        words = [word for word in tokens if word.isalpha()]
        unique_words.update(words)
        vocab_sizes.append(len(unique_words))

    return sum(vocab_sizes) / len(vocab_sizes)

def measure_top_common_words(json_data, top=30):
    captions = []
    for annotation in json_data["annotations"]:
        if annotation["area"] >= 32*32:
            caption = annotation["caption"]
            captions.append(caption)

    # Load the set of English stopwords
    stop_words = set(stopwords.words('english'))
    
    words = [word for caption in captions for word in word_tokenize(caption.lower())]
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    # Count the frequency of each word
    word_counts = Counter(filtered_words)

    # Sort the word counts by frequency in descending order and get the top 30
    most_common_words = word_counts.most_common(top)

    # Separate the words and their counts for plotting
    words, counts = zip(*most_common_words)

    return words, counts

def count_declared_categories(json_data):
    return len(json_data["categories"])

def count_categories_with_instance(json_data):
    category_ids = set()
    for annotation in json_data["annotations"]:
        category_ids.add(annotation["category_id"])
    return len(category_ids)

def count_categories_instances(json_data):
    ID_TO_CATEGORY_NAME = {}
    for category in json_data["categories"]:
        category_id = category["id"]
        category_name = category["name"]
        ID_TO_CATEGORY_NAME[category_id] = category_name

    category_counts = {}
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        category_name = ID_TO_CATEGORY_NAME[category_id]
        if category_name not in category_counts:
            category_counts[category_name] = 0
        category_counts[category_name] += 1
    
    # Sort the category_counts by count
    category_counts = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True))

    return category_counts

def count_bbox(json_data):
    bbox_count = 0
    for annotation in json_data["annotations"]:
        if "bbox" in annotation:
            bbox_count += 1
    return bbox_count

def count_small_bbox(json_data):
    small_bbox_count = 0
    for annotation in json_data["annotations"]:
        if "bbox" in annotation:
            area = annotation["area"]
            if area < 32*32:
                small_bbox_count += 1
    return small_bbox_count

def count_medium_bbox(json_data):
    medium_bbox_count = 0
    for annotation in json_data["annotations"]:
        if "bbox" in annotation:
            area = annotation["area"]
            if 32*32 <= area < 96*96:
                medium_bbox_count += 1
    return medium_bbox_count

def count_large_bbox(json_data):
    large_bbox_count = 0
    for annotation in json_data["annotations"]:
        if "bbox" in annotation:
            area = annotation["area"]
            if 96*96 <= area:
                large_bbox_count += 1
    return large_bbox_count

def count_bbox_per_image(json_data):
    ID_TO_COUNT = {}

    for annotation in json_data["annotations"]:
        image_id = annotation["image_id"]
        if "bbox" not in annotation:
            continue

        if image_id not in ID_TO_COUNT:
            ID_TO_COUNT[image_id] = 0
        ID_TO_COUNT[image_id] += 1

    return sum(ID_TO_COUNT.values()) / len(ID_TO_COUNT)


def count_small_bbox_per_image(json_data):
    ID_TO_COUNT = {}

    # Initialize
    for image in json_data["images"]:
        image_id = image["id"]
        ID_TO_COUNT[image_id] = 0

    for annotation in json_data["annotations"]:
        image_id = annotation["image_id"]
        if "bbox" not in annotation:
            continue

        area = annotation["area"]
        if area < 32*32:
            ID_TO_COUNT[image_id] += 1

    return sum(ID_TO_COUNT.values()) / len(ID_TO_COUNT)

def count_medium_bbox_per_image(json_data):
    ID_TO_COUNT = {}

    # Initialize
    for image in json_data["images"]:
        image_id = image["id"]
        ID_TO_COUNT[image_id] = 0

    for annotation in json_data["annotations"]:
        image_id = annotation["image_id"]
        if "bbox" not in annotation:
            continue

        area = annotation["area"]
        if 32*32 <= area < 96*96:
            ID_TO_COUNT[image_id] += 1

    return sum(ID_TO_COUNT.values()) / len(ID_TO_COUNT)

def count_large_bbox_per_image(json_data):
    ID_TO_COUNT = {}

    # Initialize
    for image in json_data["images"]:
        image_id = image["id"]
        ID_TO_COUNT[image_id] = 0

    for annotation in json_data["annotations"]:
        image_id = annotation["image_id"]
        if "bbox" not in annotation:
            continue

        area = annotation["area"]
        if 96*96 <= area:
            ID_TO_COUNT[image_id] += 1

    return sum(ID_TO_COUNT.values()) / len(ID_TO_COUNT)

def count_generated_positive_label(json_data):
    count = 0
    for annotation in json_data["annotations"]:
        if annotation["label"] == GENERATED_POSITIVE:
            count += 1
    return count

def count_generated_negative_label(json_data):
    count = 0
    for annotation in json_data["annotations"]:
        if annotation["label"] == GENERATED_NEGATIVE:
            count += 1
    return count

def count_refined_positive_label(json_data):
    count = 0
    for annotation in json_data["annotations"]:
        if annotation["label"] == REFINED_POSITIVE:
            count += 1
    return count

def count_not_labeled_label(json_data):
    count = 0
    for annotation in json_data["annotations"]:
        if annotation["label"] == NOT_LABELED:
            count += 1
    return count

def count_different_negative_tags(json_data):
    tags = set()
    for annotation in json_data["annotations"]:
        negatives_tags = annotation["negative_tags"]
        if negatives_tags == "":
            continue
        negatives_tags = negatives_tags.split(",")
        tags.update(negatives_tags)
    return len(tags)

def count_negative_tags(json_data):
    tags_count = {}
    for annotation in json_data["annotations"]:
        negatives_tags = annotation["negative_tags"]
        if negatives_tags == "":
            continue

        if annotation["area"] < 32*32:
            continue

        negatives_tags = negatives_tags.split(",")
        for tag in negatives_tags:
            if tag not in tags_count:
                tags_count[tag] = 0
            tags_count[tag] += 1    
    return tags_count

def count_negative_tags_per_image(json_data):
    ID_TO_COUNT = {}

    for annotation in json_data["annotations"]:
        image_id = annotation["image_id"]

        negatives_tags = annotation["negative_tags"]

        
        if annotation["area"] < 32*32:
            continue

        if negatives_tags == "":
            continue
        negatives_tags = negatives_tags.split(",")
        if image_id not in ID_TO_COUNT:
            ID_TO_COUNT[image_id] = 0
        ID_TO_COUNT[image_id] += len(negatives_tags)

    return sum(ID_TO_COUNT.values()) / len(ID_TO_COUNT)

def count_categories(classes_mapping):
    return len(classes_mapping)

def count_annotations_based_on_mapping(json_data, classes_mapping):
    count = 0
    for annotation in json_data["annotations"]:
        category_id = annotation["category_id"]
        if category_id in classes_mapping:
            count += 1
    return count
