# -*- coding: UTF-8 -*-
import collections
import csv
import json
import re
import string
import time
import urllib
import xml.etree.ElementTree as ET

def locnames():
    #extracts name, snippet and ID from extracted modern country places in Pleiades
    with open('pleiades-loc.json') as l:
        ln = json.load(l)
    loc = []
    for pl in ln["features"]:
        if re.match('^Aggregation of',pl["properties"]["Name"])==None and \
        re.match('^Withdrawn:',pl["properties"]["Name"])==None and \
        pl["geometry"] != None :
            plnm = dict()
            plnm["name"] = pl["properties"]["Name"].encode('utf8')
            plnm["snippet"] =  pl["properties"]["snippet"].encode('utf8')
            htdesc = pl["properties"]["description"].encode('utf8')
            xdesc = ET.fromstring('<div>'+htdesc+'</div>')
            pid = xdesc.find("./ul/li[1]/span")
            pleid = pid.text
            plnm["id"] = pleid
            plnm["url"] = 'http://pleiades.stoa.org/places/'+pleid
            loc.append(plnm)
    with open('location-names.tsv', 'w') as o:
        dw = csv.DictWriter(o, sorted(loc[0].keys()), delimiter='\t')
        dw.writeheader()
        dw.writerows(loc)
    
locnames()