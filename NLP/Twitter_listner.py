import os
import tweepy as tw
import pandas as pd
from datetime import date,timedelta
from firestore_add import check_prexist_report,add_feed_to_reports,get_reports
from nlp_ruler import NLP_E
import firestore_auth
###################Auth#####################################
consumer_key= 'QLatSzf4kxGh4R5GELqFSVUX4'
consumer_secret= 'm9B37uWF1INaFWBF0k6VSl0b6A4X9apzmTI0vLlNhBzQgqbR8u'
access_token= '897299439093559296-O0PON3M4fNaV3BcINHM0D8s7nomorQX'
access_token_secret= 'cYCyikf2CLL3rB5GKyp7pp4wAnC3lR4FakjPi0k2uGoTI'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
###################Auth#####################################
db=firestore_auth.auth()

#################################Twitter query####################################################
search_words = "@ForTPeople"+"-filter:retweets"
today = date.today()- timedelta(days=1)
date_since = str(today)
unprocessed_ids=[]
tweets = tw.Cursor(api.search,q=search_words,since=date_since).items(10)
print(tweets)
#################################Twitter query####################################################
#################################firestore check and feed####################################################
for tweet in tweets:
	print(tweet.text)
	flag=check_prexist_report(str(tweet.user.screen_name),str(tweet.text),db)
	if flag==0:
		id=add_feed_to_reports(str(tweet.user.screen_name),str(tweet.text),db)
	unprocessed_ids.append(id)
#################################firestore check and feed####################################################


#################################Process tweets####################################################
for ids in unprocessed_ids:
	report=get_reports(ids,db)
	d=NLP_E(report,db)
	
	print("Report: ",report)
	print("results")
	print(d)
#################################Process tweets####################################################