def auth():
	import firebase_admin
	from firebase_admin import credentials
	from firebase_admin import firestore

	# Use a service account
	cred = credentials.Certificate('ftposs-efae4cd96151.json')
	firebase_admin.initialize_app(cred)

	db = firestore.client()
	return db