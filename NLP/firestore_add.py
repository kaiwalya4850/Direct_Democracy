import firestore_auth

db=firestore_auth.auth()
##########################use to create new entities#######################
def add_ent_to_nlp(entity_name,entity_array_data):
	doc_ref = db.collection(u'NLP').document(str(entity_name))
	dec_set=set(entity_array_data)
	
	dic={u'values':list(dec_set)}
	doc_ref.set(dic)

# infra = ["Urban residence","Power","Urban transport","Water","Sewerage","Railways","Roads","Bridges","Solid waste management","Water logging","Health centre","Hospitals","Electricity Problems","Tree falls","Illegal car parking","Sweage overflow","Foul smelling sweage","Dirty smelling sweage","Potholes on road","Damaged roads","Construction since large time","Diversion on roads since long time","Rickshaw strike","Taxi strike","Illegal dumping of waste","Stray aminals","Dog died","Bird died","Pregnant cattle","Illegal cattle herding","Cattle eats grass and plants","Traffic Jam due to cattle","Excessive growth of trees","Large trees","Blockage due to falling of tree"]
# add_ent_to_nlp("Infrastructure",infra)
####################use for feeback system#######################
def add_feed_to_nlp(entity_name,entity_array_data):
	doc_ref = db.collection(u'NLP').document(str(entity_name))
	doc = doc_ref.get()

	dic=doc.to_dict()
	dec_set=set(dic['values']+entity_array_data)
	dic['values']=list(dec_set)
	
	doc_ref.set(dic)


	
# add_feed_to_nlp("Infrastructure",['test'])