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
#print(n)    # Actual data in a list


# Just in case query method fails and it did! #
# To get count of all entities and their values #
# RETURNS A LIST #
def entity_cal_list(lst):
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
a = entity_cal_list(n)
#print(a)
#print(values)

# Get count to pass in homepage #
def checkKey_to_get_just_count(dict, key):      
    if key in dict.keys(): 
        key_count = dict[key] 
    return key_count

# Entity count calculator RETURNING A DICTIONARY #
# Pass data list and desired dictionary name #
def entity_cal_dict(lst,dicti):
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
    for i in range(len(entity_list)):
        k = entity_list[i]
        count = z.count(k)
        dicti[k] = count
        i = i+1
entity_dict ={}
entity_cal_dict(n,entity_dict)

location_count = checkKey_to_get_just_count(entity_dict,"Location")
infra_count = checkKey_to_get_just_count(entity_dict,"Infrastructure")
ts_count = checkKey_to_get_just_count(entity_dict,"TS")
loneliness_count = checkKey_to_get_just_count(entity_dict,"Loneliness")
diseases_count = checkKey_to_get_just_count(entity_dict,"Diseases")
date_count =  checkKey_to_get_just_count(entity_dict,"DATE")
cardinal_count = checkKey_to_get_just_count(entity_dict,"CARDINAL")
# Getting values in a list "values" #
values = []
for i in range(len(n)):
	k = list(n[i].values())
	k.pop(-1) #since every last element is a timestamp
	values.append(k)



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
cardinal_reports =[]

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
report_gen("CARDINAL",cardinal_reports)


# To get reports ready to be shown on Flask Website #
# Pass above list with filtered reports #
# Gives you a list named final_reports #
location_final_reports = []
infra_final_reports = []
ts_final_reports = []
loneliness_final_reports = []
diseases_final_reports = []
date_final_reports = []
cardinal_final_reports = []
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
report_for_flask(cardinal_reports,cardinal_final_reports)

# Votes and e-gov stuff #
# Getting Data #
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

# Getting stuff #
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



# Lets start with Flask #
@appf.route("/")
# Home Page, display only count in numbers #
def home():
    return render_template("index_new.html",content= location_count,content1= infra_count, content2 = ts_count, \
	                      content3 = loneliness_count, content4 = diseases_count, content5 = date_count, content6 = cardinal_count )

@appf.route("/reports")
def report_show():
    return render_template("report_show_new.html",len= len(location_final_reports), location_final_reports =location_final_reports, \
	                    len1= len(infra_final_reports), infra_final_reports =infra_final_reports, \
						len2= len(loneliness_final_reports), loneliness_final_reports =loneliness_final_reports, \
						len3= len(diseases_final_reports), diseases_final_reports =diseases_final_reports, \
						len4= len(date_final_reports), date_final_reports =date_final_reports, \
                        len5= len(cardinal_final_reports), cardinal_final_reports = cardinal_final_reports)

@appf.route("/votes")
def votes_page():
    return render_template("votes.html")

@appf.route("/ent_add", methods=["POST", "GET"])
def entity_adder():
    if request.method == "POST":
        entity_name = request.form["entnm"]
        entity_add = request.form["entadd"]
        return redirect(url_for("user", ent=entity_name,entn=entity_add))  
    else:
        return render_template("ent_add_new.html") 


@appf.route("/<ent> /<entn>")
def user(ent,entn):
    existing_entity = ["City","Crime","Crime against women","Disaster","Diseases","Infrastructural Problems","Infrastructure","Loneiness"]
    print(ent,entn)
    if ent in existing_entity:
        print("yes")
        my_data = store.collection('NLP').document(ent)
        my_data.update({u'values': firestore.ArrayUnion([entn])})
        return render_template("ent_add_new.html")
    else:
        print("Wrong name")
        return f"<h2>Wrong name. Entity name must only be from {existing_entity}</h2>"

    '''
    try:
        if ent in existing_entity:
            my_data = store.collection('NLP').document(ent)
            my_data.update({u'values': firestore.ArrayUnion([entn])})
    except NameError:
        print("Invalid names, the names must be from:", existing_entity)
    '''
    

if __name__ == "__main__":
	appf.run()
