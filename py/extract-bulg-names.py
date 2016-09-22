# -*- coding: UTF-8 -*-
import collections
import csv
import json
import re
import string
import time
import urllib
import xml.etree.ElementTree as ET

def bulgnames():
    #extracts name, snippet and ID from extracted Bulgarian places in Pleiades
    with open('pleiades-bulgaria.json') as b:
        bg = json.load(b)
    bulg = []
    for pl in bg["features"]:
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
            bulg.append(plnm)
    with open('bulgarian-names.tsv', 'w') as o:
        dw = csv.DictWriter(o, sorted(bulg[0].keys()), delimiter='\t')
        dw.writeheader()
        dw.writerows(bulg)
    
bulgnames()