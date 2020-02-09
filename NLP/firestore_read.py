

def read_entities(db):
	docs = db.collection(u'NLP').stream()
	return docs