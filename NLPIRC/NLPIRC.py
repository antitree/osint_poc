#
# NLPIRC.py
# Description: Script that takes in an text file and extracts the
#  entities as well as performs freq distribution
# Based on code from https://gist.github.com/gavinmh/4735528

from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk, FreqDist
import sys

#import operator 
 
def extract_entities(text):
    entities = []
    
    for sentence in sent_tokenize(text):
        words = word_tokenize(sentence)
        chunks = ne_chunk(pos_tag(words))

        
        entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])
    return entities

def check_freq(text, entities=None):
    words = word_tokenize(text)
    fdist = FreqDist([w for w in words if len(w) > 3]) #check words 3 characters or longer
    #if Entities:
    return fdist
 
 
if __name__ == '__main__':
    try:
        file = sys.argv[1]
        f = open(file, 'r')
        text = ''.join(f.readlines())
    except:
        print("No file found or error. Using default demo instead...")
        #Demo text instead
        text = """
    Skytalks is a track at Defcon presented by 303 for the Defcon community. 
    Its purpose: for people to show the cutting edge in technology and research 
    -- the kind you can't or don't want to do at home. This is classic, old-school 
    Defcon: no cameras, no recording. No pre-con content takedowns. No sobriety. 
    No bullshit. Our track runs the 3 main days of Defcon: Friday, Saturday, and 
    Sunday.... 9am to 7pm Friday and Saturday, and 9am to close on Sunday. We bring 
    three days of the very best, and we invite you to be a part of it.Deviant Ollam
     | DaKahuna | theprez98 | SketchCow | Indigosax | Lizzie Borden | Anch | Aphelia
     | 0nlychick | Hacktress09 | Databeast | Pyr0 | Teabag | Legion303 | everyone at
     DC949 | The Defcon Goons | and most importantly, The Dark Tangent, for letting
      us do this for all these years.
    """
    entities = extract_entities(text)
    fdist = check_freq(text)
    print("List of entities from the text:")
    print(entities)
    print("Top 50 words used")
    print(fdist.keys()[:50])