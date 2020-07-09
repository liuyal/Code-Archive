# ----------------------------------------------------------------------
# DATE: 2020/05/20
# AUTHOR: Jerry Liu
# EMAIL: Liuyal@sfu.ca
#
# DESCRIPTION:
# Script for collecting Tweets from Twitter using Tweepy's Streaming API
# Extracted Tweets are formed into 2 data sets:
#   D1 - without any filter
#   D2 - Filtered with keyword COVID-19
# Each data set is processed to remove unwanted characters
# and non-English words Using regex, SpaCy, NLTK, etc.
# Remaining text is tokenized and counted for frequency of occurrence
# Using the set of frequencies a word map is generated
# ----------------------------------------------------------------------
import os
import sys
import time
import datetime
import threading
import json
import re
import queue
import tweepy
import spacy
import collections
import nltk
import colour
import numpy as np
import PIL
from PIL import Image
import wordcloud
import matplotlib.pyplot as plt

DEBUG_MODE = False


class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self, file_name, n_tweets):
        # Initialize class variables
        self.file_name = file_name
        self.n_tweets = n_tweets
        self.counter = 0
        self.text = []
        self.records = []
        self.stream = None
        super(TwitterStreamListener, self).__init__()

    def on_data(self, data):
        # Convert data in json format to dict
        # keep adding tweets until counter reaches n_tweets
        response = json.loads(data)
        save_data = []
        if self.counter < self.n_tweets:
            try:
                # Sort through API response data and collect useful information
                save_data.append(str(self.counter))
                save_data.append(str(response["id_str"]))
                save_data.append(str(response["created_at"]))
                save_data.append(str(response["timestamp_ms"]))
                save_data.append("")
                save_data.append(str(response["user"]["screen_name"]))
                save_data.append(str(response["user"]["verified"]))
                save_data.append(str(response["user"]["location"]).replace(",", "").replace("\n", " "))
                save_data.append(str(response["user"]["followers_count"]))

                # Check if retweet or quote and combine with original text
                text = str(response["text"])
                extended_tweet = 0
                retweeted_status = 0
                quoted_status = 0
                if "extended_tweet" in response.keys():
                    extended_tweet = 1
                    text = response["extended_tweet"]["full_text"]
                if "retweeted_status" in response.keys():
                    retweeted_status = 1
                    if "extended_tweet" in response["retweeted_status"].keys():
                        retweet = response["retweeted_status"]["extended_tweet"]["full_text"]
                    else:
                        retweet = response["retweeted_status"]["text"]
                    text = text + " " + retweet
                if "quoted_status" in response.keys():
                    quoted_status = 1
                    if "extended_tweet" in response["quoted_status"].keys():
                        quote = response["quoted_status"]["extended_tweet"]["full_text"]
                    else:
                        quote = response["quoted_status"]["text"]
                    text = text + " " + quote

                save_data.append(str(extended_tweet))
                save_data.append(str(retweeted_status))
                save_data.append(str(quoted_status))

                # check if keyword is queried correctly
                if filter_list[0] in text.lower():
                    save_data.append("1")
                else:
                    save_data.append("0")

                save_data[4] = text.replace("\n", " ").replace(",", " ")
                print("[" + self.file_name.replace(".csv", "").split("_")[-1] + "] " + ",".join(save_data))

                self.records.append(",".join(save_data))
                self.text.append(text)
                self.counter += 1
            except Exception as e:
                print("ERROR: ", self.counter, data)
                print(e)
        else:
            # Write tweet records into csv file
            data_header = "index,id,create_at,timestamp(ms),text,user_name,verified,location,followers_count,extended,retweeted,quoted,keyword"
            file = open(self.file_name, "a+", encoding="utf8")
            file.truncate(0)
            file.write(data_header + "\n" + "\n".join(self.records))
            file.flush()
            file.close()

            print(self.file_name + " Stream completed!")
            self.stream.disconnect()

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print(status_code)


def language_process(id, raw_text, nlp, words, q):
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

    q.put(word_collection)
    # sys.stdout.write("Thread " + str(id) + ": Complete\n")


def tokenize_text(file_name, top=100):
    file = open(file_name + ".csv", "r+", encoding="utf8")
    tweets = file.readlines()
    tweets.pop(0)
    file.close()

    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load("en_core_web_sm")
    words = set(nltk.corpus.words.words())

    q = queue.Queue()
    size = len(tweets)
    cycles = 5
    for run_range in range(0, cycles):
        thread_list = []
        start = int(run_range * size / cycles)
        end = int(((run_range + 1) * size / cycles))
        for index in range(start, end):
            # Text pre-processing to remove unwanted words, etc.
            raw_text = tweets[index].split(",")[4].replace("\n", "").lower()
            thread_list.append(threading.Thread(target=language_process, args=(index, raw_text, nlp, words, q)))
        [item.start() for item in thread_list]
        [item.join() for item in thread_list]

    counter_list = list(q.queue)
    distribution = sum(counter_list, collections.Counter())
    common_words = distribution.most_common(top)

    # # Write results to csv and print frequency for most common words
    print("\n" + file_name + " Distinct words: ", len(distribution))
    print(file_name + " Most frequent words:")
    file = open(file_name + "_result.csv", "a", encoding="utf8")
    file.truncate(0)
    file.write("word,frequency\n")
    for key, value in common_words:
        line = key + "," + str(float(value) / 1000.0)
        file.write(line + "\n")
        print(line)
    file.write("Number of distinct words," + str(len(distribution)) + "\n")
    file.close()

    return common_words


def red_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    # Function for creating color gradient base on word font size (frequency)
    lmin = 20.0
    lmax = 65.0
    hue = 10
    saturation = 100
    luminance = int((lmax - lmin) * (float(font_size) / 500.0) + lmin)
    return "hsl({}, {}%, {}%)".format(hue, saturation, luminance)


def blue_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    # Function for creating color gradient base on word font size (frequency)
    lmin = 20.0
    lmax = 65.0
    hue = 200
    saturation = 100
    luminance = int((lmax - lmin) * (float(font_size) / 500.0) + lmin)
    return "hsl({}, {}%, {}%)".format(hue, saturation, luminance)


def purple_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    # Function for creating color gradient base on word font size (frequency)
    lmin = 20.0
    lmax = 65.0
    hue = 275
    saturation = 100
    luminance = int((lmax - lmin) * (float(font_size) / 500.0) + lmin)
    return "hsl({}, {}%, {}%)".format(hue, saturation, luminance)


def generate_masked_wc(file_name, mask, word_count, color_func, max_font=500, min_font=15):
    word_cloud = wordcloud.WordCloud(width=1200, height=1200, mask=mask)
    word_cloud.max_font_size = max_font
    word_cloud.min_font_size = min_font
    word_cloud.background_color = "white"
    word_cloud.color_func = color_func
    wc_image = word_cloud.generate_from_frequencies(word_count)
    plt.figure(figsize=(12, 12), facecolor=None)
    plt.imshow(wc_image, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(file_name, bbox_inches='tight', transparent=True)
    image = Image.open(file_name)
    image.show()


def create_word_cloud(file_name, data, color_func):
    # Create Word cloud object and set attributes
    print("Creating World Cloud for: " + file_name)
    words = []
    for key, value in data:
        for i in range(0, int(value)):
            words.append(key)
    generate_masked_wc(file_name + ".png", None, collections.Counter(words), color_func)


def create_Venn_word_cloud(file_name, top_words1, top_words2, mask_type):
    words1 = []
    for key, value in top_words1:
        for i in range(0, int(value)):
            words1.append(key)
    words2 = []
    for key, value in top_words2:
        for i in range(0, int(value)):
            words2.append(key)
    diff_word1 = []
    for key, value in top_words1:
        if key in set(words1).difference(set(words2)):
            for i in range(0, int(value)):
                diff_word1.append(key)
    diff_word2 = []
    for key, value in top_words2:
        if key in set(words2).difference(set(words1)):
            for i in range(0, int(value)):
                diff_word2.append(key)
    common_words = []
    for key, value in top_words1 + top_words2:
        if key in set(words1).intersection(set(words2)):
            for i in range(0, int(value)):
                common_words.append(key)

    words1_count = collections.Counter(diff_word1)
    words2_count = collections.Counter(diff_word2)
    combined_words_count = collections.Counter(common_words)

    mid_mask = np.array(Image.open("masks" + os.sep + mask_type + os.sep + "mid.png"))
    left_mask = np.array(Image.open("masks" + os.sep + mask_type + os.sep + "left.png"))
    right_mask = np.array(Image.open("masks" + os.sep + mask_type + os.sep + "right.png"))

    generate_masked_wc(file_name + "_venn_mid.png", mid_mask, combined_words_count, purple_color_func)
    generate_masked_wc(file_name + "_venn_left.png", left_mask, words1_count, blue_color_func)
    generate_masked_wc(file_name + "_venn_right.png", right_mask, words2_count, red_color_func)


def stream_thread(auth, file_name, n_tweets, languages, filter_list=None):
    # Create listener object and pass in OAUTH credentials and steam object
    listener = TwitterStreamListener(file_name=file_name, n_tweets=n_tweets)
    stream = tweepy.Stream(auth, listener, tweet_mode='extended')
    # Assign reference to stream in listener
    listener.stream = stream
    # Check if need filter or not
    if filter_list is not None:
        stream.filter(track=filter_list, languages=languages, encoding='utf8')
    else:
        stream.sample(languages=languages)

    global data_queue
    data_queue[file_name] = " ".join(listener.text)


if __name__ == '__main__':
    # Keys and secrets for OAUTH
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    # Data set names with time stamp
    time_stamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    if not DEBUG_MODE:
        data_set_1 = time_stamp + "_" + "d1"
        data_set_2 = time_stamp + "_" + "d2"
    else:
        data_set_1 = "d1"
        data_set_2 = "d2"

    # Initialize filter list, languages, number of tweets to capture
    filter_list = ['COVID-19']
    languages = ['en']
    n_tweets = 1000
    thread_list = []
    data_queue = {}

    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Start a stream threads for each data set
    if not DEBUG_MODE or (not os.path.isfile(data_set_1 + ".csv") or not os.path.isfile(data_set_2 + ".csv")):
        thread_list.append(threading.Thread(target=stream_thread, args=(auth, data_set_1 + ".csv", n_tweets, languages, None)))
        thread_list.append(threading.Thread(target=stream_thread, args=(auth, data_set_2 + ".csv", n_tweets, languages, filter_list)))
        [item.start() for item in thread_list]
        [item.join() for item in thread_list]

    # Tokenize and process the texts find common words
    print("\nRunning Tokenizer on texts...")
    top_words1 = tokenize_text(data_set_1)
    top_words2 = tokenize_text(data_set_2)

    # Create word clouds using word cloud function
    print("\nCreating Word Clouds...")
    create_word_cloud(data_set_1, top_words1, blue_color_func)
    create_word_cloud(data_set_2, top_words2, red_color_func)

    print("Creating Venn World Cloud..")
    create_Venn_word_cloud(data_set_1, top_words1, top_words2, "mask2")

    time.sleep(5)
    print("\n[EOS]")
