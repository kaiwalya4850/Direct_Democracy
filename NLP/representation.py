import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, session

appf = Flask(__name__)
appf.secret_key = 'any random string'


cred = credentials.Certificate("ftposs-50575d1883e8.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'E-gov')
n=[]
try:
    docs = doc_ref.stream()
    for doc in docs:
        a = doc.to_dict()
        n.append(a)
except:
    print(u'Missing data')
#print(n)

location_reports = []
def checkKey(dict, key):      
    if key in dict.keys(): 
        #print("Present, value is", dict[key]) 
        val = "yes"
    else:
        val = "no"
    return val


def report_gen(key_name,entity_reports_list):
    for i in range(len(n)):
        k = n[i]
        c = checkKey(k,key_name)
        if c is "yes":
            entity_reports_list.append(k)
        else:
            pass


report_gen("Location",location_reports)
#print(len(location_reports))
#data = list(location_reports[0].keys())
#print(data)

# To get reports ready to be shown on Flask Website #
# Pass above list with filtered reports #
# Gives you a list named final_reports #
final_reports = []
def report_for_flask(upper_list,rep):
    fin= ""
    for i in range(len(upper_list)):
        key_val = list(upper_list[i].keys())
        val_val = list(upper_list[i].values())
        for l in range(len(key_val)):
            stra = str(key_val[l])
            strb = str(val_val[l])
            strc = stra+": "+strb+ ", "
            fin = fin+strc
        i = i+1
        rep.append(fin)


report_for_flask(location_reports,final_reports)
#print((final_reports))



# Mid 2 stuff. Includes: Getting e-gov data ready to display, Getting to show number of votes, what is the vote(and who voted) #
# Other changes include, complete shift from wordpress to Flask static #
# Remove wordpress completely and make better # 
store1 = firestore.client()
doc_ref1 = store1.collection(u'E-gov')
n_id = []
n_data = []
try:
    docs = doc_ref1.stream()
    for doc in docs:
        a = doc.to_dict()
        n_data.append(a)
        doc_id = doc.id
        n_id.append(doc_id)
except:
    print(u'Missing data')
#print(n1)


# Setting data on firestore #
name = "Diseases"
data = "corona virus test 1"
dic = {u'values':data}
my_data = store.collection('NLP').document(name)
my_data.update({u'values': firestore.ArrayUnion([data])})
