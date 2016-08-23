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


def getnames():
    with open('pl-wp-wd.json') as r:
        raw = json.load(r)
    wdout = []
    for wd in raw:
        try:
            wdat1 = wd['WikidataURI'].split('/wiki/',1)[1]
            wdat2 = 'http://www.wikidata.org/wiki/Special:EntityData/'+wdat1+'.json'
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
            boo = False
            if 'ar' in wdj['entities'][wdat1]['labels']:
                arn = wdj['entities'][wdat1]['labels']['ar']
                arstr = arn['value']
                wd['Arabic'] = arstr
                boo = True
            if 'tr' in wdj['entities'][wdat1]['labels']:
                trn = wdj['entities'][wdat1]['labels']['tr']
                trstr = trn['value']
                wd['Turkish'] = trstr
                boo = True
            if boo:
                wdout.append(wd)
            else:
                print wdat1+" has no Arabic or Turkish names"
        except:
            print "Error: "+wdat1
            continue
    jsutf = json.dumps(wdout,ensure_ascii=False).encode('utf8')
    with open('pl-w-names.json','w') as jsout:
        jsout.write(jsutf)


#getwdata()
getnames()