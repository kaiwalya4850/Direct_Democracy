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


#report_for_flask(location_reports,final_reports)
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
'''
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
'''
'''
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

vote_dict = {}

for i in range(len(vote_data)):
    vote_dict[vote_id[i]] = vote_data[i]

# Pass vote_id from above #
# Gets: Total number of votes(index 0), how many yes(index 1) and no(index 2) #
'''


'''
# Macro analysis #
store2 = firestore.client()
doc_ref2 = store2.collection(u'WEAK_NO_CLASSIFIED')
non = []
try:
    docs = doc_ref2.stream()
    for doc in docs:
        doc_id = doc.id
        non.append(doc_id)    
except:
    print(u'Missing data')

print(non)       

store2 = firestore.client()
doc_ref2 = store2.collection(u'REPORTS')
macro_id = []
macro_data = []
try:
    docs = doc_ref2.stream()
    for doc in docs:
        a = doc.to_dict()
        macro_data.append(a)
        doc_id = doc.id
        macro_id.append(doc_id)    
except:
    print(u'Missing data')

#print(macro_data,macro_id)

final_unclassified = {}
for i in range(len(macro_id)):
    if macro_id[i] in non:
        final_unclassified[macro_id[i]] = macro_data[i]['report']

print(final_unclassified)

my_data = store.collection('REPORTS_CLASSIFIED').document('A0ZBircQ3VsmIiqcD8zi')
my_data.set({u'Location':"Vadodara",u'Something else':'Anything',u'lets see':''})
'''

store1 = firestore.client()
doc_ref1 = store1.collection(u'REPORTS')
rep_id = []
rep_data = []
try:
    docs = doc_ref1.stream()
    for doc in docs:
        a = doc.to_dict()
        rep_data.append(a)
        doc_id = doc.id
        rep_id.append(doc_id)
except:
    print(u'Missing data')

reps = {}
for i in range(len(rep_id)):
    reps[rep_id[i]] = rep_data[i]

store1 = firestore.client()
doc_ref1 = store1.collection(u'REPORTS_CLASSIFIED')
classrep_id = []
classrep_data = []
try:
    docs = doc_ref1.stream()
    for doc in docs:
        a = doc.to_dict()
        classrep_data.append(a)
        doc_id = doc.id
        classrep_id.append(doc_id)
except:
    print(u'Missing data')

#print(classrep_data)
loc_dict = {}
lone_dict = {}
disease_dict = {}
city_dict = {}
exist = ["City","Crime","Crime against women","Disaster","Diseases","Infrastructural Problems","Infrastructure","Loneiness","Location"]
for i in range(len(classrep_data)):
    var = classrep_data[i]
    if "Diseases" in list(var.keys()):
        disease_dict[classrep_id[i]] = var['Diseases']
    if "Location" in list(var.keys()):
        loc_dict[classrep_id[i]] = var['Location']
    if "City" in list(var.keys()):
        city_dict[classrep_id[i]] = var['City']
    if "Loneliness" in list(var.keys()):
        lone_dict[classrep_id[i]] = var['Loneliness']
    i = i+1

def get_key(val,my_dict): 
    for key, value in my_dict.items(): 
         if val == value:
             my_dict.pop(key) 
             return key 

#print(loc_dict)
'''
loc_unique = sorted(list(loc_dict.values()))
loc_show = {}
for i in range(len(loc_unique)):
    key = get_key(loc_unique[i],loc_dict)
    if key in list(reps.keys()):
        temp = reps[key]
        final = temp['report']
        loc_show[loc_unique[i]] = final

print(loc_show)
'''
lone_unique = sorted(list(lone_dict.values()))
print(lone_unique)
lone_show = []
for i in range(len(lone_unique)):
    key = get_key(lone_unique[i],lone_dict)
    print(key)
    if key in list(reps.keys()):
        temp = reps[key]
        final = temp['report']
        lone_show.append(final)

print(lone_show)

