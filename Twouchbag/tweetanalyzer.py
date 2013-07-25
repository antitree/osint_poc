#!/usr/bin/python
#Tweet Analyzer

import tweettagger
import sqlite3
import sys

DB = 'tweet.db'

def dbget(screenname):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM ' + screenname)
    totaltweets = cur.fetchone()
    rows = [x for x in cur.execute('SELECT * FROM ' + screenname + ' where urls is not "[]"' )]
    return rows

def filter(tweets):
    #filter out useless information
    ftweets = tweets
    return ftweets

def score(tweets):
    scoredtweets = []
    for tweet in tweets:
        score = 0
        if tweet[6] is not "[]":
            score += 90
        
        print(score)
        
        
    return scoredtweets
    
def getdomainblacklist():
    f = open("blacklistdomains.txt", 'r')
    blacklist = [x for x in f.readlines()]
    return blacklist

def main():
    screenname = sys.argv[1]
    
    tweets = dbget(screenname)
    tweets = filter(tweets)
    scoredtweets = score(tweets)
    
if __name__ == "__main__":
    main()
    