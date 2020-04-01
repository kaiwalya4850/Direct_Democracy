import google.cloud
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, session
import firestore_auth

appf = Flask(__name__)
appf.secret_key = 'any random string'

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
#print(len(n))
# Just in case query method fails and it did! #
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


a = entity_cal(n)
#print(a)
#print(values)
# Part to generate reports #
def checkKey(dict, key):      
    if key in dict.keys(): 
        #print("Present, value is", dict[key]) 
        val = "yes"
    else:
        val = "no"
    return val


# Gets all the data with certain entity #
# Pass all data as dict and a black list to store #
# send to next function for flask readable format #
location_reports = []	
infra_reports = []	
ts_reports = []
loneliness_reports = []
diseases_reports = []
date_reports = []

def report_gen(key_name,entity_reports_list):
    for i in range(len(n)):
        k = n[i]
        c = checkKey(k,key_name)
        if c is "yes":
            entity_reports_list.append(k)
        else:
            pass
report_gen("Location",location_reports)		
report_gen("Infrastructure",infra_reports)
report_gen("Loneliness",loneliness_reports)
report_gen("TS",ts_reports)
report_gen("Diseases",diseases_reports)
report_gen("DATE",date_reports)



# To get reports ready to be shown on Flask Website #
# Pass above list with filtered reports #
# Gives you a list named final_reports #
location_final_reports = []
infra_final_reports = []
ts_final_reports = []
loneliness_final_reports = []
diseases_final_reports = []
date_final_reports = []
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
        fin = ""

report_for_flask(location_reports,location_final_reports)
report_for_flask(infra_reports,infra_final_reports)
report_for_flask(ts_reports,ts_final_reports)
report_for_flask(loneliness_reports,loneliness_final_reports)
report_for_flask(diseases_reports,diseases_final_reports)
report_for_flask(date_reports,date_final_reports)






# Lets start with Flask #
@appf.route("/")
# Home Page, display only count in numbers #
def home():
    return render_template("index.html",len= len(date_final_reports), date_final_reports =date_final_reports)

@appf.route("/reports")
def report_show():
    return render_template("report_show.html")

if __name__ == "__main__":
	appf.run()
