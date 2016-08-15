# -*- coding: UTF-8 -*-
import string
import re
import json

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
