
import firestore_auth
db=firestore_auth.auth()
doc_ref = db.collection(u'Votes').document(u'Draft Personal Data Protection Bill, 2018').collection(u'Votes')
docs = doc_ref.stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))