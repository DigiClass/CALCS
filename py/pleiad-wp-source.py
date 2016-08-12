# -*- coding: UTF-8 -*-
import string
import re
#import socket
#import time
#import urllib
import json

def wpasevid():
    with open('dianium.json') as p:
    #with open('../../../../Desktop/calcs/pleiades-places.json') as p:
        pleiad = json.load(p)
    #wp = open('wpevid.json','w')
    allrefs = []
    for pl in pleiad:
        if pl['@type'] == 'Place':
            thisplace = pl['id']
            thistitle = pl['title']
            for ref in pl['references']:
                if ref['type'] == 'seeFurther' and re.match('https?://[a-z\-]{2,14}.wikipedia.org/.*',ref['uri']):
                    thisref = dict()
                    thisref['Title'] = thistitle
                    thisref['Pleiades'] = thisplace
                    thisref['Wikipedia'] = ref['uri']
                    allrefs.append(thisref)
    for mapping in allrefs:
        print '('+mapping['Title']+') '+mapping['Pleiades']+': '+mapping['Wikipedia']



def jsonname():
    input = ''' [
    { "id" : "001", "x" : "2", "name" : "Chuck" },
    { "id" : "009", "x" : "7", "name" : "Brent" },
    { "id" : "123", "x" : "81", "name" : "Bubba Hotep" }
    ]'''
    info = json.loads(input)
    print 'User count:', len(info)
    for item in info:
        print 'Name', item['name'] 
        print 'Id', item['id'] 
        print 'Attribute', item['x']

def geoapi():
    serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
    while True:
        address = raw_input('Enter location: ')
        if len(address) < 1 : break
        url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
        print 'Retrieving', url
        uh = urllib.urlopen(url)
        data = uh.read()
        print 'Retrieved',len(data),'characters'
        try: js = json.loads(str(data))
        except: js = None
        if 'status' not in js or js['status'] != 'OK':
            print '==== Failure To Retrieve ===='
            print data
            continue
        print json.dumps(js, indent=4)
        lat = js["results"][0]["geometry"]["location"]["lat"] 
        lng = js["results"][0]["geometry"]["location"]["lng"] 
        print 'lat',lat,'lng',lng
        location = js['results'][0]['formatted_address']
        print location

wpasevid()
