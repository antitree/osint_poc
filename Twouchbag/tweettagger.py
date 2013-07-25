## TweetTagger.py
## Twitter object class that classifies each tweet
## based on its features. Used for machine learning
## and stats later.  
##
## Example Usage
##
## import TweetTagger
## tagger = tweettagger.TweetTager()
## tagger.process_tweet(dict_of_twitter_API_response)
## tagger.classify()
## print(tagger.tweet['text']

import re
import requests
#import futures  
import urlparse
import time
import unicodedata


class Tweettagger(object):
    '''Twitter class that takes a tweet and returns
    metadata properties such as key words, links, images
    retweets, etc'''
    
    def __init__(self):
        self.tweet = {
         'id': None,
         'text': None,
         'geo': None,
         'retweet_count': None,
         'retweeted': None,
         'coordinates': None,
         'entities': None,
         'place': None,
         'created_at': None,
         'entities': None,
         'urls': None,
         'domains': None,
         'hashtags': None,
         'keywords': None,
         'deleted': None,
         'category': None,
         'words': None,
         'sentences': None,
         'actionable': None,
         'score': None,
          
          }
        
        self.anon = False  # whether we care about attribution
        
    
    def __longify(self, url):
      """Take a shortened URL and longify without making 
      a direct request to the site"""
      ##TODO: These calls should be queued in a thread. 
      try:
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 301:
            lurl = r.headers['location']
            return lurl
        else: return url
      except:
        return url
    
    def process_tweet(self, tweet):
        '''Takes in a dict from the official twitter 1.1 api and creates a tweet object'''
        for key in tweet.keys():
            if key in self.tweet.keys():
                if isinstance(tweet[key], unicode):
                    value = unicodedata.normalize('NFKD', tweet[key]).encode('ascii','ignore')
                else: value = tweet[key]
                #self.tweet[key] = str(tweet[key])
                self.tweet[key] = value
        
        #Formatting fixes
        self.tweet['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
      
    
    def classify(self):
        """Wrapper function that will do all of the classifying 
        possible""" 
        ##Classifying is a misnomer - I think this is actually analyzing?
        ##TODO: Decide if it shoudl be here or in analytics
        self.classifylinks()
        if self.tweet['urls']:
            self.classifydomain()
        #self.classifycategory()
        #self.classifyactionable()
        #self.classifytext()
    
    def classifylinks(self):
        '''returns the links and domains of a tweet as 
        a list'''
        #   l = re.findall(r'(https?://[^\s]+)', self.tweet) #get all the urls
        l = [url['expanded_url'] for url in self.tweet['entities']['urls']] 
        self.tweet['urls'] = [self.__longify(url) for url in l]
    
    def classifydomain(self):
        """Set the domains that are used in the tweet. Does not return a value"""
        self.tweet['domains'] = [urlparse.urlparse(u).hostname for u in self.tweet['urls']]
        
    def classifycategory(self):
        #Todo use scoring engine to help categorize content
        #TODO: Decide if this should be here or in analytics portion
        self.tweet['category'] = None
        
    def classifyactionable(self):
        """Automatically classify whether a tweet is actionable based on
        something that I haven't written yet..."""
        ##TODO decide if this should be here or in the analytics portion
        self.actionable = 0
    
    
    def classifytext(self):
        '''return a list of keywords automatically extracted 
        from the text'''
        import nltk    #import as necessary
        
        self.tweet['sentences'] = nltk.tokenize.sent_tokenize(self.tweet['text'])
        
        self.tweet['words'] = nltk.tokenize.word_tokenize(self.tweet['text'])
        #This is really just an example. Trained chunkers would be better
        #TODO: Make sure NLTK content has been downloaded
        #postag = nltk.chunk.ne_chunk(nltk.tag.pos_tag(self.words))
    
