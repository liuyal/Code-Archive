# ----------------------------------------------------------------------
# DATE: 2020/07/10
# AUTHOR: Jerry Liu
# EMAIL: Liuyal@sfu.ca
#
# DESCRIPTION:
# Script for generating pattern oods from data set D1 and D2
# ----------------------------------------------------------------------
import os
import sys
import time
import datetime
import re
import threading
import csv
import queue
import spacy
import collections
import nltk
import shutil
import stat
import itertools


def delete_folder(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(path, ignore_errors=True)


def load_csv_data(file_name):
    file = open(file_name, "r+", encoding="utf8")
    data_output = file.readlines()
    header = data_output.pop(0)
    file.close()
    return header, data_output


def language_process(raw_text, nlp, words):
    # Functions are credited to TA Arjun Mahadevan
    url_pattern = re.compile(r'https://\S+|www\.\S+')
    replace_url = url_pattern.sub(r'', str(raw_text))
    # Remove url and punctuation base on regex pattern
    punctuation_pattern = re.compile(r'[^\w\s\-]')
    no_punctuation = punctuation_pattern.sub(r'', replace_url).lower()
    processed_text = re.sub(r'^[0-9]*$', '', no_punctuation)
    # Load NLTK's words library and filter out non-english words
    processed_text = " ".join(w for w in nltk.wordpunct_tokenize(processed_text) if w.lower() in words)
    doc = nlp(processed_text)
    # Tokenize text and remove words that are less than 3 letters
    output_words = [token.text for token in doc if token.is_stop is not True and token.is_punct is not True]
    output_words = [letters for letters in output_words if len(letters) > 2]
    word_collection = collections.Counter(output_words)

    return word_collection


def generate_item_set(data, length):
    # Generate itemset of patterns of length k
    results = {}
    for row in data:
        # index raw text
        text = row.split(',')[4].lower()
        # Tokenize text
        tokens = language_process(text, nlp, words)
        # Generate pattern of length k
        R = list(itertools.combinations(list(tokens), length))
        # Add to dictionary and count frequency
        for pattern in R:
            if pattern not in results.keys(): results[pattern] = 0
            results[pattern] += 1
    return collections.Counter(results)


if __name__ == "__main__":
    print("START Time: " + datetime.datetime.now().strftime("%Y%m%d %H:%M:%S") + "\n")

    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load("en_core_web_sm")
    words = set(nltk.corpus.words.words())

    # Clean up Folders
    for folder in os.listdir(os.getcwd()):
        if os.path.isdir(folder) and "pattern" not in folder: delete_folder(os.getcwd() + os.sep + folder)
    os.mkdir(os.getcwd() + os.sep + "output_odds")

    odds_list = []
    h1, data_set_1 = load_csv_data(os.getcwd() + os.sep + "d1.csv")
    h2, data_set_2 = load_csv_data(os.getcwd() + os.sep + "d2.csv")

    # Find comment token patterns in both D1 and D2 and calcualte odds
    for i in range(1, 5):
        tokens1 = generate_item_set(data_set_1, i)
        tokens2 = generate_item_set(data_set_2, i)
        for key in set(tokens1).intersection(set(tokens2)):
            if tokens1[key] >= 5:
                sup_d1 = tokens1[key]
                sup_d2 = tokens2[key]
                odds_list.append((key, float(sup_d2 / sup_d1)))

    # Sort list base on odds value
    sorted_odds_list = sorted(odds_list, key=lambda tup: tup[1], reverse=True)

    # Save odds list to csv
    file = open(os.getcwd() + os.sep + "output_odds" + os.sep + "odds_list.csv", "w+")
    for key, count in sorted_odds_list:
        file.write(",".join(key) + "," + str(count) + "\n")
    file.flush()
    file.close()

    print("END Time: " + datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
