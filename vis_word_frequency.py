import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import os
from matplotlib.ticker import MaxNLocator
import numpy as np

from utils.util import *
from wordcloud import WordCloud

def main(json_file: str, output_folder: str, top):

    os.makedirs(output_folder, exist_ok=True)

    json_data = read_json(json_file)

    captions = []
    for annotation in json_data["annotations"]:
        captions.append(annotation["caption"])

    # Load the set of English stopwords
    stop_words = set(stopwords.words("english"))

    # Tokenize each sentence into words and flatten the list
    words = [word for caption in captions for word in word_tokenize(caption.lower())]

    # Filter out stopwords and non-alphabetic words
    filtered_words = [
        word for word in words if word.isalpha() and word not in stop_words
    ]

    word_count = {}
    for word in filtered_words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    # Sort the word count dictionary in descending order
    word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

    # Wrtie top 200 words to file
    top = 200
    with open("temp.txt", "w") as f:
        for i, (word, count) in enumerate(word_count.items()):
            if i >= top:
                break
            f.write(f"{word}: {count}\n")

    # Create the word cloud
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(word_count)
    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    output_path = os.path.join(output_folder, f"caption_wordcloud.png")
    plt.savefig(output_path)
    plt.clf()


if __name__ == "__main__":
    csv_file = "final.json"
    output_folder = "./figures/"
    top = 100
    main(csv_file, output_folder, top)
