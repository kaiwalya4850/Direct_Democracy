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
# Other changes include, complete shift from wordpress to Flask static: DONE #
# Remove wordpress completely and make better: DONE # 

# Setting data on firestore #
#name = "Diseases"
#data = "corona virus test 1"
#dic = {u'values':data}
#my_data = store.collection('NLP').document(name)
#my_data.update({u'values': firestore.ArrayUnion([data])})


store1 = firestore.client()
doc_ref1 = store1.collection(u'E-gov')
egov_id = []
egov_data = []
try:
    docs = doc_ref1.stream()
    for doc in docs:
        a = doc.to_dict()
        egov_data.append(a)
        doc_id = doc.id
        egov_id.append(doc_id)
except:
    print(u'Missing data')


# Classifies the drafted and pending bills #
# Provides dictionary for the same, used in viewing all bills #
# USAGE, get data from firestore. Argument1 is list of ID(names) #
# Argument2 is the actual data in dictionary # 
def get_bill_link_status(names_of_bill,dict_of_link):
    bill_link = {}
    draft_bills = {}
    pending_bills = {}
    for i in range(len(names_of_bill)):
        linkx = list(dict_of_link[i].items())
        linkf = linkx[1][1]
        names = names_of_bill[i]
        d_or_p = linkx[0][1]
        if d_or_p == "Draft":
            draft_bills[names] = linkf
        else:
            pending_bills[names] = linkf
        i = i+1
    return draft_bills,pending_bills

d = get_bill_link_status(egov_id,egov_data)


store2 = firestore.client()
doc_ref2 = store2.collection(u'Votes')
vote_id = []
vote_data = []
try:
    docs = doc_ref2.stream()
    for doc in docs:
        a = doc.to_dict()
        vote_data.append(a)
        doc_id = doc.id
        vote_id.append(doc_id)
except:
    print(u'Missing data')

print(vote_id)



