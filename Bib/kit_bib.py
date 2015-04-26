#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys
import re
#from mechanize import ParseResponse, urlopen, urljoin
from os import system
from time import *
import mechanize

# hier wird direkt die Webseite geladen, die per AJAX angefordert wird.
# Es ist daher möglich, dass sich diese Seite oft ändert
# Die AJAX-Datei enthält die letzten 1000 Einträge. Das entspricht bei der KIT-Bib rund 83 Stunden (halbe Woche), bei der Physik-Bib rund knapp 10 Tagen.
# Python kann gut 10 Millionen Array-Felder handlen, das entspricht damit mindestens 8 Jahren.
# Alternativ: nur die letzten 1000 Einträge abfragen
# Die Daten sollen per GNU-Plot dargestellt werden

def lastxrows(a, b, x):
    f = open(a, 'r')
    g = open(b, 'w')
    lines = f.readlines()
    lines = lines[-x:]
    for i in lines:
        g.write(i)
    f.close()
    g.close()
br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders =    	 [('User-agent', 'Firefox')]
bib = ["LSG", "LST","LSW","LSM", "LSN", "LBS", "LAF", "FBP", "BIB-N"]
#zum einfacheren berechnen, muss evtl. oft angepasst werden:
maxseat= [164, 192, 176, 56, 186, 72, 94, 86, 37]
maxseat_kitbib = maxseat[0]+maxseat[1]+maxseat[2]+maxseat[3]+maxseat[4]+maxseat[5]
f = open("kitbib.txt",'r')
s = f.read()
f.close()
f = open("kitbib.txt",'a')
frei = []
nfrei = []
for i in range(6):
    address = "http://services.bibliothek.kit.edu/leitsystem/getdata.php?&location[0]="+bib[i]+"&values[0]=seatestimate&after[0]=-10050000seconds&after[1]&before[0]=now&before[1]=now&limit[0]=-1111&limit[1]=1"
    response = br.open(address)
    seite = response.read()
    x=0
    for i in seite.split('},{"timestamp'):
        values = re.findall(r'\b\d+\b', i)
        try: frei[x] += int(values[8])
        except: frei.append(int(values[8]))
        try: nfrei[x] += int(values[7])
        except: nfrei.append(int(values[7]))
        x = x+1
x=0
for i in reversed(seite.split('},{"timestamp')):
    values = re.findall(r'\b\d+\b', i)
    datetime = str(values[2]+"-"+values[1]+"-"+values[0]+" "+values[3]+":"+values[4])
    if not datetime in s:
        f.write(datetime+"  "+str(frei[x])+" "+str(nfrei[x])+" "+str(frei[x]/(nfrei[x]+frei[x]))+"\n")
    x = x+1;
f.close()

f = []
s = []
f.append(open("laf.txt","r"))
f.append(open("fbp.txt","r"))
f.append(open("bibn.txt","r"))
s.append(f[0].read())
s.append(f[1].read())
s.append(f[2].read())
f[0].close()
f[1].close()
f[2].close()
f = []
f.append(open("laf.txt","a"))
f.append(open("fbp.txt","a"))
f.append(open("bibn.txt","a"))

frei = []
nfrei = []

for i in range(6,9):
    address = "http://services.bibliothek.kit.edu/leitsystem/getdata.php?&location[0]="+bib[i]+"&values[0]=seatestimate&after[0]=-10050000seconds&after[1]&before[0]=now&before[1]=now&limit[0]=-1111&limit[1]=1"
    response = br.open(address)
    seite = response.read()
    x=0
    for j in reversed(seite.split('},{"timestamp')):
        values = re.findall(r'\b\d+\b', j)
        datetime = str(values[2]+"-"+values[1]+"-"+values[0]+" "+values[3]+":"+values[4])
        if not datetime in s[i-6]:
            f[i-6].write(datetime+"  "+values[8]+" "+values[7]+" "+str(int(values[8])/(float(values[7])+int(values[8])))+"\n")
        x = x+1

f[0].close()
f[1].close()
f[2].close()
lastxrows("kitbib.txt", "kitbib_7.txt", 2020)
lastxrows("kitbib_7.txt", "kitbib_24.txt", 300)
lastxrows("kitbib_24.txt", "kitbib_3.txt", 40)

lastxrows("laf.txt", "laf_7.txt", 2020)
lastxrows("laf_7.txt", "laf_24.txt", 300)
lastxrows("laf_24.txt", "laf_3.txt", 40)
lastxrows("fbp.txt", "fbp_7.txt", 2020)
lastxrows("fbp_7.txt", "fbp_24.txt", 300)
lastxrows("fbp_24.txt", "fbp_3.txt", 40)
lastxrows("bibn.txt", "bibn_7.txt", 2020)
lastxrows("bibn_7.txt", "bibn_24.txt", 300)
lastxrows("bibn_24.txt", "bibn_3.txt", 40)
lt = localtime()
print "Programmdurchlauf beendet:",str(lt.tm_mday)+"."+str(lt.tm_mon)+",",str(lt.tm_hour)+":"+str(lt.tm_min)+" Uhr."
system('kitbib.plt')