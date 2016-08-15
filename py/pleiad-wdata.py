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
        time.sleep(2)
        wpage1 = urllib.urlopen(wpurl["WikipediaURL"]).read()
        wpage2 = re.sub('&.*?;','',wpage1)
        xpage = ET.fromstring(wpage2)
        wdata = xpage.find(".//li[@id='t-wikibase']/a").attrib['href']
        print wdata

def wpasevid():
    #with open('dianium.json') as p:
    with open('../../../../Desktop/calcs/pleiades-places.json') as p:
        pleiad = json.load(p)
    allrefs = []
    for pl in pleiad["@graph"]:
        if pl['@type'] == 'Place':
            thisplace = pl['id']
            thistitle = pl['title']
            for ref in pl['references']:
                if ref['type'] == 'seeFurther' and re.match('https?://[a-z\-]{2,14}.wikipedia.org/.*',ref['uri']):
                    thisref = dict()
                    thisref['Title'] = thistitle
                    thisref['PleiadesURI'] = thisplace
                    thisref['WikipediaURL'] = ref['uri']
                    allrefs.append(thisref)
    json.dump(allrefs, open('wpevid.json','w'), indent=4)




getwdata()
