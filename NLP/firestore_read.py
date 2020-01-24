import firestore_auth

db=firestore_auth.auth()

def read_entities():
	docs = db.collection(u'NLP').stream()
	return docs