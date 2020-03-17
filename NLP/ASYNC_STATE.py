import firestore_auth
from firestore_add import get_UCreports,add_feed_to_WEreports,del_UCreports,get_reports,push_reports_classified
from nlp_ruler import NLP_E
import time
db=firestore_auth.auth()
doc_ref = db.collection(u'Async').document(u'State')
def on_snapshot(doc_snapshot, changes, read_time):
	for doc in doc_snapshot:
		dic=doc.to_dict()
		if dic['val']=='1':
#################################get UnPRocessed IDS###############################################
			doc=get_UCreports(db)
#################################get UnPRocessed IDS###############################################
#################################Process tweets####################################################
			for ids in doc:
				report=get_reports(ids.id,db)
				d=NLP_E(report,db)
				
				print("Report: ",report)
				print("results")
				print(d)
				if len(d)==0:
					print("unclassified, add to human classifer")
					add_feed_to_WEreports(ids.id,db)
				if len(d)<=2:
					add_feed_to_WEreports(ids.id,db)
					print("weakly classified, add to human classifier")
					
				push_reports_classified(d,ids.id,db)
				del_UCreports(db,ids.id)
#################################Process tweets####################################################
			
		
		
		else:
			print('false')
		
# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)


while 1:
	time.sleep(10)
	print('program is running....')