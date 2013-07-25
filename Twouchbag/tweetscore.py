#!/usr/bin/python
## TweetScore.py
## POC used to score a bunch of tweets based on actionability
## Reads in a YAML config file and returns useful results 
##
##
## Example Usage:
## python tweetscore.py username
##

import sqlite3
import yaml
#import tweettagger




class tweetscore(object):
    def __init__(self, scoreconfig="scoring.yaml"):
        with open(scoreconfig, 'r') as f:
            self.config = yaml.load(f)
            
        self.retweet = self.config["retweet"]
        self.url = self.config["url"]
        self.phrases = self.config["phrases"]
        self.days = self.config["days"]
        self.baddomains = self.config["baddomains"]
        self.times = self.config["times"]
        self.caplocks = self.config["caplocks"]
        self.douche = self.config["douche"]
        #nlp
        #other
        #other
        
        
    
    def score(self, t):
        score = 0
        #tag = tweettagger.Tweettagger()
        #tag.process_tweet(t)
        #tag.classify()
        
        #tweet = tag.tweet
        tweet = t
        
        #does it contain a URL
        if tweet['urls']:
            score += self.url
            
            #does it contain a url on the blacklist
            for url in tweet['urls']:
                for d in self.baddomains:
                    if d["dom"] in url: 
                        score += d["score"]
        
        
        #look for keywords    
        for phrase in self.phrases:
            if phrase["phrase"] in tweet["text"]:
                score += phrase["score"]
                
        #Look for douche keywords
        douchescores = [w["score"] for w in self.douche if w["phrase"] in tweet["text"]]
        score += sum(douchescores)
                
        #How many CAP locks are used
        upperletters = [l for l in tweet["text"] if l.isupper()]
        if len(upperletters) > 10:
            score += self.caplocks            
            
        #is it a retweet
        if tweet['retweeted']:
            print("Retweeted")
            score += self.retweet
        return score    
        
        
        
        