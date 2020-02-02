import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy
from collections import Counter
import en_core_web_sm
import spacy
import nltk, re, pprint
from nltk.corpus import wordnet 
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from firestore_read import read_entities
def add_ruler(entity_name,entity_arr):
	ruler = EntityRuler(nlp, overwrite_ents=True)
	for d in entity_arr:
		ruler.add_patterns([{"label": str(entity_name), "pattern": d}])
	ruler.name = str(entity_name)
	return ruler
nlp = spacy.load('en_core_web_sm')


rulerAll = EntityRuler(nlp, overwrite_ents=True)

docs=read_entities()
for doc in docs:
	ruler=add_ruler(doc.id,doc.to_dict()['values'])

	nlp.add_pipe(ruler)

#print(nlp.pipe_names) # Let's review what are the entities in our model

# User input 
sentence = "Parth caught in security fraud, causing earthquake with traffic jam due to cattle since 2 hours in Vidyanagar, Anand!"
doc = nlp(sentence)
a = [(X.text, X.label_) for X in doc.ents]
#print(a) # List of the entities : reason
d = {}
tokenList = nltk.word_tokenize(sentence)
for ent in doc.ents:
	if ent.label_ == "GPE" or ent.label_ == "NORP" or ent.label_ == "LOC":
		d["Location"] = ent.text
		#print('location = ',ent.text)
	if ent.label_ == "TIME":
		d["Time"] = ent.text
s = sentence.replace(',','')
s = s.replace('.','')
s = s.replace('!','')
s = s.replace('?','')
s = s.lower()
doc = nlp(s)
a = [(X.text, X.label_) for X in doc.ents]
tokenList = nltk.word_tokenize(sentence)
for ent in doc.ents:
	d[ent.label_] = ent.text
print(d)