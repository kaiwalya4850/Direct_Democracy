import google.cloud
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, session
import firestore_auth

app = Flask(__name__)
app.secret_key = 'any random string'

cred = credentials.Certificate("ftposs-50575d1883e8.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'REPORTS_CLASSIFIED')
#docs = doc_ref.where(u'Location', u'==', True).stream()

# Getting data and storing in n#
n=[]
try:
    docs = doc_ref.stream()
    for doc in docs:
        a = doc.to_dict()
        n.append(a)
except:
    print(u'Missing data')
print(len(n))
# Just in case query method fails and it did!
# To get count of all entities and their values #
def entity_cal(lst):
    z = list(lst[0])
    #print(z)
    for i in range((len(lst)-1)):
	    x = list(lst[i+1])
	    for j in range(len(x)):
		    y = x[j]
		    z.append(y)
		    j = j+1
	    i = i+1
    entity_list = list(set(z)) # list of entities on db # 
    #print(entity_list)
    final = []
    for i in range(len(entity_list)):
	    k = entity_list[i]
	    count = z.count(k)
	    app = str(k) + ":" + str(count)
	    final.append(app)
	    i = i+1
    return final

# Getting values in a list "values" #
values = []
for i in range(len(n)):
	k = list(n[i].values())
	k.pop(-1) #since every last element is a timestamp
	values.append(k)


a = entity_cal(values)
print(a)



