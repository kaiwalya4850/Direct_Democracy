import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("ftposs-9bbdd6e0ec3b.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'NLP')
n=0
try:
    docs = doc_ref.stream()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except:
    print(u'Missing data')
print(doc)