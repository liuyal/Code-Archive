import spacy
from spacy_langdetect import LanguageDetector

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

text = 'this is a text sample.'
doc = nlp(text)

print(doc._.language)