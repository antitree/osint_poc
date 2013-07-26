## TweetCollect.py
## POC Used to collect tweets using the 1.1 Twitter API. 
## Besides just downloading the tweets, they are individually
## classified using the tweetagger module. 
##
## Example Usage:
## python tweetcollect.py list_of_twitter_ids.txt
##


import requests
import sqlite3
import json
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import logging
import tweettagger
import tweetscore
import sys

## Get your own motherfucker. https://dev.twitter.com
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

if CONSUMER_KEY == '':
    print("No consumer key - RTFM: Details in beginning of the script")
    quit()
 
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

## Fill this in with the tokens printed out on first run
## TODO Save this externally
OAUTH_TOKEN =  ''
OAUTH_TOKEN_SECRET = ''
 
OAUTH_TOKEN =  '220462504-hxNQIFvxDcN0NJuxfl59NbrnZ5UoAkXEKGO5XADY'
OAUTH_TOKEN_SECRET = 'BIM84g1tIvuEHbDWmekFs52F032DZdHdcddcpvoBo'

############
AUTH = ''
alert = [] 

SCORE = []
 
def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
 
    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]
    
    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url
    
    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)
 
    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]
 
    return token, secret
 
 
def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def get_alltweets(screenname, lastid="", auth=AUTH):
    """Iterate through ever last tweet the user has in their
    timeline. It will not get every tweet because the API
    is a dick, but you should get up to 3000+"""
    
    count = 200
    tweets = []
    maxcall="&max_id="
    if lastid:
        maxid = maxcall + str(lastid)
    else: maxid = ""
    
    while True:
        r = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&include_rts=1&count=%s%s" % (screenname, count, maxid, ), auth=AUTH, ).json()
        tweets += r
        store_tweets(r, screenname)
        
        try:
            lastid = r[len(r)-1]["id"]
            maxid = maxcall+str(lastid)
        except:
            print("ERROR: api call did not return anything while collecting for %s. Make sure account exists and is not protected." % screenname)
            print(r)
        if len(r) < 2:
            store_tweets(tweets, screenname)
            print("Stored tweets successfully")
            break
        
        print("Collected %s tweets..." % len(tweets))
        
def score_tweet(tweet):
    #Score tweets
    scoring = tweetscore.tweetscore()
    score = scoring.score(tweet)
    tweet['score'] = score
    SCORE.append(score)
    #if score > 0:
    #    alert.append(tweet)
        


def store_tweets(tweets, screenname):
    
    #con = sqlite3.connect('tweet.db')
    #cur = con.cursor()
    
    tag = tweettagger.Tweettagger()
    
    #define the schema to match the tweettagger class
    #schema = ' (' + ", ".join(["%s text" % x for x in tag.tweet.keys()]) + ')'
 
    
    #cur.execute('CREATE TABLE IF NOT EXISTS '+ screenname + schema)
    for tweet in tweets:
        tagger = tweettagger.Tweettagger()
        tagger.process_tweet(tweet) # classify the features from the API
        tagger.classify()           # classify other features outside of the API
        tagger.tweet['entities'] = ""   #HACK: doesn't need to be stored but has the URLs in them
        
        score_tweet(tagger.tweet)
        
        #Insert values into database
        #query='INSERT OR REPLACE INTO ' + screenname + ' VALUES(' + ("?,"*len(tagger.tweet.keys()))[:-1] +')'
        #try: 
        #    cur.execute(query, ([str(x) for x in tagger.tweet.values()]))
        #except sqlite3.ProgrammingError, e:
        #    #Unicode issues often caught for SQLITE. Hacked right now
        #    print("ERROR: %s on query %s " % (screenname, query))
        #    print("-"*100)
        #    print(tagger.tweet.values())
        #    print("-"*100)
        #    print("Unicode error %s " % e)
                     
    #cur.close()
    #con.commit()


if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print "Put this into the top of the python file"
        print
    else:
        AUTH = get_oauth()
        try:
            target = sys.argv[1]
        except:
            print("Please give me a target")
            quit()

        get_alltweets(target)
        result = sum(SCORE) / len(SCORE)
        findings_num = len([x for x in SCORE if x < 0])
        
        print("DOUCHEBAG SCORE FOR USER %s:" % target)
        print(result)
        print("NUMBER OF TOTAL DOUCHY POSTS FOUND:")
        print(findings_num)        
