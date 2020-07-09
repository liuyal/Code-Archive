import os, sys, time
import spacy
from collections import Counter


def tokenize_text(text):
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.replace("\n", "").lower())

    # Analyze syntax
    words = [token.text for token in doc if token.is_stop != True and token.is_punct != True]

    # Find most common tokens
    common_words = Counter(words).most_common(100)

    print("Most frequent words:")
    for i in range(0, len(common_words)):
        print(str(i + 1) + "," + common_words[i][0] + "," + str(common_words[i][1]))
    print("\nTotal Number of words: ", len(words))
    print("Number of distinct words: ", len(set(words)))

    return common_words


if __name__ == "__main__":
    file = open("text.txt", "r+", encoding="UTF8")
    text = file.read()
    file.close()

    tokenize_text(text)
