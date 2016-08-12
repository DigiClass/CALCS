import string
import re
import urllib

def allurls():
    lurls = open('cats.txt')
    fout = open('wikipgs.txt','w')
    for url in lurls:
        try: 
            hand = urllib.urlopen(url.rstrip())
        except:
            continue
        for line in hand:
            lst = re.findall('href="/wiki/([^:"]+)"', line.rstrip())
            if len(lst)>0:
                for u in lst:
                    if u != "Main_Page" and  re.match('^List_of_',u) == None : 
                        fout.write(u)
                        fout.write('\n')
#        fout.write('\n')
    fout.close()

allurls()