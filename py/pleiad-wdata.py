# -*- coding: UTF-8 -*-
import collections
import csv
import json
import re
import string
import time
import urllib
import xml.etree.ElementTree as ET

def getwdata():
    # fetches Wikidata URI for each Wikipedia page in dictionary
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
    # fetches Arabic and Turkish names from Wikidata
    # only outputs entries if at least one name to add
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

def slimwdnames():
    # removes duplicate Wikidata entries from results
    # removes Turkish names that are identical to Pleiades *or* Wikipedia labels
    with open('pl-w-names.json') as r:
        rdat = json.load(r) 
    cldat = []
    for pl in rdat:
        try:
            wduri = pl["WikidataURI"]
            if not cldat:
                allwds = []
            else:
                allwds = cldat[0]["WikidataURI"]
            if wduri in allwds:
                print "Dropping repeated "+pl["WikidataURI"].split('/wiki/',1)[1]
                continue
            else:
                if "Turkish" in pl.keys():
                    if pl["Turkish"] == pl["Title"] or pl["Turkish"] == pl['WikipediaURL'].split('/wiki/',1)[1]:
                        print "Removing duplicate "+pl["Turkish"]+" from "+pl["WikidataURI"].split('/wiki/',1)[1]
                        del pl["Turkish"]
                cldat.append(pl)
        except:
            print "Error: "+pl["WikidataURI"].split('/wiki/',1)[1]
            continue
    cdutf = json.dumps(cldat,ensure_ascii=False).encode('utf8')
    with open('cleanednames.json','w') as cdout:
        cdout.write(cdutf)


def rendertsv():
    # renders a row of TSV for each Arabic or Turkish name (in CALCS/Pleiades format)
    # as per https://docs.google.com/spreadsheets/d/1KBa5OqOL5cxIfR1i_Mr2oex8KiLkX0QegR4HYImN7NE
    with open('cleanednames.json') as atn:
        atnames = json.load(atn) 
    tsvrows = []
    # columns needed = label	Pleiades place	Name	Transliteration	Language	source citation	source link	source citation 2	source link 2	source citation 3	source link 3	date attested	author	details
    for place in atnames:
        if "Arabic" in place.keys():
            arrow = collections.OrderedDict()
            arrow["label"] = place["Title"].encode('utf8')
            arrow["Pleiades place"] = place["PleiadesID"]
            arrow["Name"] = place["Arabic"].encode('utf8')
            arrow["Transliteration"] = ""
            arrow["Language"] = "ar"
            arrow["source citation"] = "Wikidata: "+place["WikidataURI"].split('/wiki/',1)[1]
            arrow["source link"] = place["WikidataURI"]
            arrow["source citation 2"] = ""
            arrow["source link 2"] = ""
            arrow["source citation 3"] = ""
            arrow["source link 3"] = ""
            arrow["date attested"] = "modern"
            arrow["author"] = "gbodard,vvitale"
            arrow["details"] = ""
            tsvrows.append(arrow)
        if "Turkish" in place.keys():
            trrow = collections.OrderedDict()
            trrow["label"] = place["Title"].encode('utf8')
            trrow["Pleiades place"] = place["PleiadesID"]
            trrow["Name"] = place["Turkish"].encode('utf8')
            trrow["Transliteration"] = ""
            trrow["Language"] = "tr"
            trrow["source citation"] = "Wikidata: "+place["WikidataURI"].split('/wiki/',1)[1]
            trrow["source link"] = place["WikidataURI"]
            trrow["source citation 2"] = ""
            trrow["source link 2"] = ""
            trrow["source citation 3"] = ""
            trrow["source link 3"] = ""
            trrow["date attested"] = "modern"
            trrow["author"] = "gbodard,vvitale"
            trrow["details"] = ""
            tsvrows.append(trrow)
    # save as TSV
    with open('pleiad-wdata-clean.tsv', 'w') as o:
        dw = csv.DictWriter(o, sorted(tsvrows[0].keys()), delimiter='\t')
        dw.writeheader()
        dw.writerows(tsvrows)



#getwdata()
#getnames()
#slimwdnames()
rendertsv()
