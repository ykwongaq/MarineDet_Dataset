import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import os

import numpy as np


from utils.util import *

# nltk.download("stopwords")
# nltk.download("punkt")


def main(csv_file: str, output_folder: str, top):

    os.makedirs(output_folder, exist_ok=True)

    csv_data = read_csv(csv_file)

    captions = []
    for data in csv_data:
        captions.append(data[CAPTION])

    # Load the set of English stopwords
    stop_words = set(stopwords.words("english"))

    # Tokenize each sentence into words and flatten the list
    words = [word for caption in captions for word in word_tokenize(caption.lower())]

    # Filter out stopwords and non-alphabetic words
    filtered_words = [
        word for word in words if word.isalpha() and word not in stop_words
    ]

    # Count the frequency of each word
    word_counts = Counter(filtered_words)

    # Sort the word counts by frequency in descending order and get the top 30
    most_common_words = word_counts.most_common(top)

    # Separate the words and their counts for plotting
    words, counts = zip(*most_common_words)

    # Create the bar chart
    plt.figure(figsize=(14, 8))
    plt.bar(np.arange(len(words)) * 5, counts, color="skyblue")

    # Add titles and labels
    plt.title(f"Top {top} Most Frequent Words", fontsize=16)
    plt.xlabel("Words", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)

    # Rotate x labels to avoid overlap
    plt.xticks(np.arange(len(words)) * 5, words, rotation=60, ha="right")

    # Display the plot
    plt.tight_layout()

    output_path = os.path.join(output_folder, "word_frequency.png")
    plt.savefig(output_path)


if __name__ == "__main__":
    csv_file = "data/mvk_caption.csv"
    output_folder = "./figures"
    top = 80
    main(csv_file, output_folder, top)
