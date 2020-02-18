import os
from datetime import date,timedelta
from firestore_add import check_prexist_report,add_feed_to_reports,get_reports,push_reports_classified
from nlp_ruler import NLP_E
import firestore_auth

consumer_key= 'QLatSzf4kxGh4R5GELqFSVUX4'
consumer_secret= 'm9B37uWF1INaFWBF0k6VSl0b6A4X9apzmTI0vLlNhBzQgqbR8u'
access_token= '897299439093559296-O0PON3M4fNaV3BcINHM0D8s7nomorQX'
access_token_secret= 'cYCyikf2CLL3rB5GKyp7pp4wAnC3lR4FakjPi0k2uGoTI'

db=firestore_auth.auth()


ip = input("Enter a string in any language you want")
a = NLP_E(ip,db)
print(a)