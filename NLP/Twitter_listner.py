import os
import tweepy as tw
import pandas as pd
from datetime import date,timedelta
from firestore_add import check_prexist_report,add_feed_to_reports,get_reports,push_reports_classified,add_feed_to_ucreports
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
today = date.today()- timedelta(days=3)
date_since = str(today)
unprocessed_ids=[]
tweets = tw.Cursor(api.search,q=search_words,since=date_since).items(100)
print(tweets)
#################################Twitter query####################################################
#################################firestore check and feed####################################################
for tweet in tweets:
	
	str_final=tweet.text.replace('@ForTPeople', '')
	print(tweet.text)
	flag=check_prexist_report(str(tweet.user.screen_name),str(str_final),db)
	if flag==0:
		id=add_feed_to_reports(str(tweet.user.screen_name),str(str_final),str(tweet.user.location),db)
		add_feed_to_ucreports(str(tweet.user.screen_name),id,str(str_final),str(tweet.user.location),db)
		unprocessed_ids.append(id)
#################################firestore check and feed####################################################


#################################Process tweets####################################################
for ids in unprocessed_ids:
	report=get_reports(ids,db)
	d=NLP_E(report,db)
	
	print("Report: ",report)
	print("results")
	print(d)
	if len(d)==0:
		print("unclassified, add to human classifer")
	if len(d)<=2:
		print("weakly classified, add to human classifier")
		
	push_reports_classified(d,ids,db)
#################################Process tweets####################################################