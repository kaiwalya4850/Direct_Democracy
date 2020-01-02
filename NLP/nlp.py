import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import spacy
nlp = spacy.load("en_core_web_sm")
#git pull
doc = nlp('Kaiwalya here, living in Anand, facing water logging problem since 2 hours near Sastri Medan')
print([(X.text, X.label_) for X in doc.ents])
