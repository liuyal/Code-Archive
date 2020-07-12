import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

text = """Hello Mr. Smith, how are you doing today?"""

tokenized_sent = sent_tokenize(text)
print(tokenized_sent)

tokenized_word = word_tokenize(text)
print(tokenized_word)

fdist = FreqDist(tokenized_word)
print(fdist.most_common(10))

stop_words = set(stopwords.words("english"))
print(stop_words, "\n")

filtered_sent = []
for w in tokenized_word:
    if w not in stop_words:
        filtered_sent.append(w)
print("Tokenized Sentence:", tokenized_word)
print("Filterd Sentence:", filtered_sent, "\n")

ps = PorterStemmer()
stemmed_words = []
for w in filtered_sent:
    stemmed_words.append(ps.stem(w))
print("Filtered Sentence:", filtered_sent)
print("Stemmed Sentence:", stemmed_words, "\n")

lem = WordNetLemmatizer()
stem = PorterStemmer()
word = "flying"
print("Lemmatized Word:", lem.lemmatize(word, "v"))
print("Stemmed Word:", stem.stem(word), "\n")

sent = "Albert Einstein was born in Ulm, Germany in 1879."
tokens = nltk.word_tokenize(sent)
print(tokens)
print(nltk.pos_tag(tokens), "\n")
