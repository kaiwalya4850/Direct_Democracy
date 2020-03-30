import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("ftposs-50575d1883e8.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'NLP')
n={}
try:
    docs = doc_ref.stream()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
        a = doc.to_dict()
        n = a
except:
    print(u'Missing data')
print(doc)