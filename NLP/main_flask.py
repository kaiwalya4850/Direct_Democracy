import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("ftposs-50575d1883e8.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'REPORTS_CLASSIFIED')
n=[]
try:
    docs = doc_ref.stream()
    for doc in docs:
        a = doc.to_dict()
        n.append(a)
except:
    print(u'Missing data')
#print(n)
k = 0
keys = []
value = []
for i in range(len(n)):
	z = n[k]
	key = z.keys()
	keys.append(key)
	val = z.values()
	value.append(val)
	k = k+1
print(keys[0][11])


