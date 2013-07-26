#!/usr/bin/python
# 9TAT4

import sys
sys.path.append("lib")
import src.rss as rss
import modules.gplus as gplus
import modules.reddit.reddit as reddit
#import modules.twitter.modtwitter as modtwitter
import modules.instagram.instagram as instagram
import modules.rssreader.rssreader as rssreader
import modules.twitpic.twitpic as twitpic
#import modules.gmail.mod_gmail as gmail
#import modules.irc.irclogparse as irclogparse
#import lib.threader as threader
#import twitter

def punkrokk():


 rsslist = []
 try:
    punkrokkreddit = reddit.classify(reddit.collect("punkrokk"))
    reddits = reddit.output(punkrokkreddit)
    rsslist += reddits
 except:
    print("ERROR downloading reddit")

 try:
    punkrokkinstagram = instagram.classify(instagram.collect("punkrokk"))
    instagrams = instagram.output(punkrokkinstagram)
    rsslist += instagrams
 except:
    print("ERROR downloading instagram")
    pass

 try:
    githubrss = "https://github.com/punkrokk.atom"
    punkrokkgithub = rssreader.classify(rssreader.collect(githubrss))
    githubs = rssreader.output(punkrokkgithub)
    rsslist += githubs
 except:
    print("Error downloading github feed")
   
 try: 
    twitterrss = "https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=punkrokk"
    punkrokktwitter = rssreader.classify(rssreader.collect(twitterrss))
    twitters = rssreader.output(punkrokktwitter)
    rsslist += twitters
 except:
    print("Error downloading twitter")

 try:
    punkrokktwitp = twitpic.classify(twitpic.collect("punkrokk"))
    twitpics = twitpic.output(punkrokktwitp)
    rsslist += twitpics
 except:
    print("Error downloading twitpic")

    feed = output(rsslist)
    feed.to_xml("./Punkrokk.xml")


def berticus():
    """threader.queueup(
	["110364378733146525545", "107091264429608883314"], 
	collect_gplus,
	classify_gplus,
	5
    """

    rsslist = []
    #""" 
    #Reddit1
    bertreddit = reddit.classify(reddit.collect("berticus"))
    reddits = reddit.output(bertreddit)
    #rsslist += reddits

    #Last.fm
    #http://www.last.fm/user/berticus
    bertlastfmrss = "http://ws.audioscrobbler.com/1.0/user/berticus/recenttracks.rss"
    bertlastfms = rssreader.classify(rssreader.collect(bertlastfmrss))
    
    lastfms = rssreader.output(bertlastfms)
    print(lastfms)
    rsslist += lastfms


    #insatagram
    bertinstagram = instagram.classify(instagram.collect("bertmb"))
    instagrams = instagram.output(bertinstagram)
    #rsslist += instagrams


    #github
    githubrss = "https://github.com/beardicus.atom"
    bertgithub = rssreader.classify(rssreader.collect(githubrss))
    githubs = rssreader.output(bertgithub)
    rsslist += githubs

    #twutter
    twitterrss = "https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=bertmb"
    bertmbtwitter = rssreader.classify(rssreader.collect(twitterrss))
    twitters = rssreader.output(bertmbtwitter)
    rsslist += twitters

    #twitpic
    bertmbtwitp = twitpic.classify(twitpic.collect("bertmb"))
    twitpics = twitpic.output(bertmbtwitp)
    #rsslist += twitpics
    
    #gmail
    #bertmbgmail = gmail.classify(gmail.collect("brian.boucheron@gmail.com"))
    #gmails = gmail.output(bertmbgmail)
    #rsslist += gmails

    #flickr
    flickrrss = "http://api.flickr.com/services/feeds/photos_public.gne?id=88138723@N00&lang=en-us&format=rss_200"
    bertmbflickr = rssreader.classify(rssreader.collect(flickrrss))
    flickrs = rssreader.output(bertmbflickr)
    #rsslist += flickrs

    #"""

    #IRC
    bertmbirc = irclogparse.classify(irclogparse.collect('irclogs/Freenode/#interlock.log'), "beardicus")
    ircs = irclogparse.output(bertmbirc)
    #rsslist += ircs
   

    feed = output(rsslist)
    feed.to_xml("./Berticus.xml")
    
	
    #berttwitter = modtwitter.classify(modtwitter.collect("bertmb"))

def output(rsslist):
    feed = rss.RSS("TEST", "Feed for a suer")
    for item in rsslist:
        feed.add_item(
	    title=item["title"],
	    description=item["description"],
	    link=item["link"],
	    pubDate=item["pubDate"],
	)
    return feed



if __name__ == '__main__':
    #berticus()
    punkrokk()

