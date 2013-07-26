import sys
sys.path.append("../lib")
import pyRSS2Gen
import datetime


class RSS(object):
    """ RSS wrapper class that creates an RSS feed for you"""

    def __init__(self, title, description):
      self.rss = pyRSS2Gen.RSS2(
        title = title,
        link = 'http://www.antitree.com',
        description = description,
        lastBuildDate = datetime.datetime.now(),
	
	items = [])

    def add_item(self, title=None, link=None, description=None, author=None, categories=None, pubDate=datetime.datetime.now(), source=None):
        """Create an RSS item to add to the feed. Looking for title, link, description, author, 
        categories, pubdate, and source when possible. Returns an RSS2 item"""
        rssitem = pyRSS2Gen.RSSItem(title=title, link=link, description=description, author=author, categories=categories, pubDate=pubDate, source=source)
        self.rss.items.append(rssitem)
        

    def to_xml(self, path="./output.rss"):
        """ Save the results in an XML format in the supplied path. If no path supplied, the default
        location is ./output.rss"""
	if True:
        #try: 
         self.rss.write_xml(open(path, "w"))
        #except:
        #  print("Error saving to %s. Make sure the path exists and the XML is properly escaped" % path)

