import firestore_auth
import time

##########################use to create new entities#######################
def add_ent_to_nlp(entity_name,entity_array_data,db):
	doc_ref = db.collection(u'NLP').document(str(entity_name))
	dec_set=set(entity_array_data)
	
	dic={u'values':list(dec_set)}
	doc_ref.set(dic)

# infra = ["Urban residence","Power","Urban transport","Water","Sewerage","Railways","Roads","Bridges","Solid waste management","Water logging","Health centre","Hospitals","Electricity Problems","Tree falls","Illegal car parking","Sweage overflow","Foul smelling sweage","Dirty smelling sweage","Potholes on road","Damaged roads","Construction since large time","Diversion on roads since long time","Rickshaw strike","Taxi strike","Illegal dumping of waste","Stray aminals","Dog died","Bird died","Pregnant cattle","Illegal cattle herding","Cattle eats grass and plants","Traffic Jam due to cattle","Excessive growth of trees","Large trees","Blockage due to falling of tree"]
# add_ent_to_nlp("Infrastructure",infra)
####################use for feeback system#######################
def add_feed_to_nlp(entity_name,entity_array_data,db):
	doc_ref = db.collection(u'NLP').document(str(entity_name))
	doc = doc_ref.get()

	dic=doc.to_dict()
	dec_set=set(dic['values']+entity_array_data)
	dic['values']=list(dec_set)
	
	doc_ref.set(dic)


	
# add_feed_to_nlp("Infrastructure",['test'])


def add_feed_to_reports(UID,report,loc,db):
	doc_ref = db.collection(u'REPORTS').document()
	
	dic={u'UID':str(UID),u'report':str(report),u'DATA_LOC':str(loc),u'TS':str(int(time.time()))}
	doc_ref.set(dic)
	return (doc_ref.id)
	
def check_prexist_report(UID,report,db):
	flag=0
	report_ref = db.collection(u'REPORTS')
	query = report_ref.where(u'UID', u'==', str(UID)).where(u'report', u'==', str(report))
	docs = query.stream()
	for doc in docs:
		flag=flag+1
	return flag
def get_reports(id,db):
	doc_ref = db.collection(u'REPORTS').document(str(id))
	doc = doc_ref.get()

	dic=doc.to_dict()
	report=dic['report']
	return report
	
def push_reports_classified(dic,id,db):
	doc_ref = db.collection(u'REPORTS_CLASSIFIED').document(str(id))
	dic['TS']=str(int(time.time()))
	doc_ref.set(dic)
