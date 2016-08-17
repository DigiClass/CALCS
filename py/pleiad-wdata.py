# -*- coding: UTF-8 -*-
import json
import re
import string
import time
import urllib
import xml.etree.ElementTree as ET

def getwdata():
    with open('wpevid.json') as p:
        wp = json.load(p)
    for wpurl in wp:
        time.sleep(1)
        try:
            wpage1 = urllib.urlopen(wpurl["WikipediaURL"]).read()
            wpage2 = re.sub('&.*?;','',wpage1)
            xpage = ET.fromstring(wpage2)
            wdata = xpage.find(".//li[@id='t-wikibase']/a").attrib['href']
            wpurl["WikidataURI"] = wdata
        except:
            print "Error: "+wpurl["WikipediaURL"]
            continue
    json.dump(wp,open('pl-wp-wd.json','w'),indent=4)

# http://www.wikidata.org/wiki/Special:EntityData/
# + Q00000000.json

def getnames():
    with open('pl-wp-wd0.json') as r:
        raw = json.load(r)
    for wd in raw:
        try:
            wdat1 = wd['WikidataURI'].split('/wiki/',1)[1]
            wdat2 = 'http://www.wikidata.org/wiki/Special:EntityData/'+wdat1+'.json'
            print wdat1
            print wdat2
        except:
            print "Error: "+wd['WikipediaURL']+" has no Wikidata URI"
            continue
        try:
            wdjson = urllib.urlopen(wdat2)
            wdj = json.load(wdjson)
        except:
            print wdat2+": Cannot load json"
            continue
        try:
            arn = wdj['entities'][wdat1]['labels']['ar']['value']
            print wd['WikidataURI']
            print arn
        except:
            print "Error: "+wd['WikipediaURL']
            continue
    #json.dump(raw,(open('pl-w-names.json','w'),indent=4)


#getwdata()
getnames()