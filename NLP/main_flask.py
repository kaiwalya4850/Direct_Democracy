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
drafts = d[0]
pending = d[1]
draft_name = list(drafts.keys())
draft_link = list(drafts.items())
pending_name = list(pending.keys())
pending_link = list(pending.items())
number_of_bills = int(len(draft_name))+int(len(pending_name))


# Getting vote_ID  #
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

# Pass vote_id from above #
# Gets: Total number of votes(index 0), how many yes(index 1) and no(index 2) #
def get_vote_stats(vote_id_list):
    queryx = []
    qid = []
    count_dict = {}
    yes_dict = {}
    no_dict = {}
    for i in range(len(vote_id_list)):
        try:
            query = doc_ref2.document(vote_id_list[i]).collection('Votes').stream()
            for doc in query:
                a = doc.to_dict()
                queryx.append(a)
                doc_id = doc.id
                qid.append(doc_id)
        except:
            print(u'Missing data')
        count_dict[vote_id_list[i]] = len(qid)
        for j in range(len(qid)):
            p = list(queryx[j].items())
            y_or_n = p[0][1]
            if y_or_n == "Yes":
                yes_dict[vote_id_list[i]] = qid
            else:
                no_dict[vote_id_list[i]] = qid           
            j = j+1
        queryx = []
        qid = []
        i = i+1    
    return count_dict,yes_dict,no_dict
    
vote_display = get_vote_stats(vote_id)
vote_count = vote_display[0]
vote_count_names = list(vote_count.keys())
vote_count_count = list(vote_count.items())
yes_count = vote_display[1]
yes_count_bill = list(yes_count.keys())
yes_count_voters = list(yes_count.items())
no_count = vote_display[2]
no_count_bill = list(no_count.keys())
no_count_voters = list(no_count.items())

# Starting Macro Analysis stuff #
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
#print(non)       

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
    return render_template("votes.html",len=len(draft_name),dname = draft_name,dlink = draft_link,len1 = len(pending_name), \
                           pname = pending_name,plink = pending_link, number = number_of_bills, len2 = len(vote_count_names), \
                            vc_name = vote_count_names, vc_count = vote_count_count, len3 = len(yes_count_bill), yes_nm = yes_count_bill, \
                            yes_voter = yes_count_voters, len4 = len(no_count_bill),no_nm = no_count_bill, no_voter = no_count_voters)

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

@appf.route("/macro_add", methods=["POST", "GET"])
def macro_adder():
    if request.method == "POST":
        city_dat = request.form["city_data"]
        crime_dat = request.form["crime_data"]
        cow_dat = request.form["cow_data"]
        disaster_dat = request.form["disaster_data"]
        diseases_dat = request.form["disease_data"]
        infra_dat = request.form["infra_data"]
        lonely_dat = request.form["lonely_data"]
        doc_dat = request.form["doc_data"]
        return redirect(url_for("user1", city = city_dat,crime = crime_dat, cow = cow_dat, disaster = disaster_dat, disease = diseases_dat , \
                                 infra = infra_dat, lone = lonely_dat, docx = doc_dat))  
    else:
        return render_template("macro_analysis.html") 


@appf.route("/<city> /<crime> /<cow> /<disaster> /<disease> /<infra> /<lone> /<docx>")
def user1(city, crime, cow, disaster, disease, infra, lone, docx):
    to_put = {}
    #existing_entity = ["City","Crime","Crime against women","Disaster","Diseases","Infrastructural Problems","Infrastructure","Loneiness"]
    print(city, crime, cow, disaster, disease, infra, lone)
    if city=="NA":
        print("na")
    else:
        to_put[u"City"] = city 

    if crime=="NA":
        print("na")
    else:
        to_put[u"Crime"] = crime

    if cow=="NA":
        print("na")
    else:
        to_put[u"Crime against women"] = cow
    
    if disaster=="NA":
        print("na")
    else:
        to_put[u"Disaster"] = disaster

    if disease=="NA":
        print("na")
    else:
        to_put[u"Diseases"] = disease

    if infra=="NA":
        print("na")
    else:
        to_put[u"Infrastructure"] = infra
        
    if lone=="NA":
        print("na")
    else:
        to_put[u"Loneliness"] = lone

    print(to_put)
    docx = str(docx)
    my_data = store.collection('REPORTS_CLASSIFIED').document(docx).set(to_put)
    return render_template("macro_analysis.html") 

if __name__ == "__main__":
	appf.run()
