#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
#from mechanize import ParseResponse, urlopen, urljoin
import mechanize
from time import *
from bs4 import BeautifulSoup
br = mechanize.Browser()
br.set_handle_robots(False)	  # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox')]
wochentag = ["Montag", "Dienstag","Mittwoch","Donnerstag", "Freitag", "Samstag", "Sonntag"]


lt = localtime()
print "Es ist", wochentag[lt.tm_wday], "der", str(lt.tm_mday)+"."+str(lt.tm_mon)+". um "+str(lt.tm_hour)+":%02i"%lt.tm_min+" Uhr."
address = "http://www.wetteronline.de/wetter/karlsruhe"
#ant = br.open("http://localhost/Daily/daily.php?testy=marco")
#print ant.read()
#input()
	

response = br.open(address)
seite = response.read()
#print seite	 # the text of the page
sunrise = re.findall('sunrisetime.{10}', seite)
sunset = re.findall('sunsettime.{10}', seite)
for i in range(len(sunrise)):
	sunrise[i] = sunrise[i].split("'")[1]
	sunset[i] = sunset[i].split("'")[1]
print "Heute: Sonnenaufgang", sunrise[0], "Uhr, Sonnenuntergang:", sunset[0], "Uhr."
print "Morgen: Sonnenaufgang", sunrise[1], "Uhr, Sonnenuntergang:", sunset[1], "Uhr."
print "Übermorgen: Sonnenaufgang", sunrise[2], "Uhr, Sonnenuntergang:", sunset[2], "Uhr."
print "Überübermorgen: Sonnenaufgang", sunrise[3], "Uhr, Sonnenuntergang:", sunset[3], "Uhr."
for line in seite.splitlines():					#Findet Aktuelle Temperatur
	x = re.findall('temperature tooltip gt.{,3}">.{2}', line)
	y = re.findall('weather tooltip">.{1,}<', line)
	if x: print "Es sind aktuell:",x[0].split(">")[1], "Grad, es ist", re.findall('weather tooltip">[^<]+',line)[0].split(">")[1]+"."
seite = seite.replace("\n", "") # einzeilig machen
print "Aktueller Wetterbericht:\n",re.findall("Wetterbericht.{,500}</p>",seite)[0].split("\t")[1]



response = br.open("http://www.fcbayern.de/de/spiele/spielplan/bundesliga/")
seite = response.read()
print "----------------------\n\n Ab jetzt Infos zu Bayern:"
seite = seite.replace("\n", "") # einzeilig machen
mannschaften = re.findall('.{600}>- : -<.{300}', seite)
print "Als nächstes in der Bundesliga am", re.findall('matchday">[^<]+', mannschaften[0])[0].split(">")[1], "um",re.findall('time">[^<]+', mannschaften[0])[0].split(">")[1], "Uhr:"
mannschaften = re.findall('alt="[^"]+', mannschaften[0])
print mannschaften[0].split('"')[1], "gegen", mannschaften[1].split('"')[1]

response = br.open("http://www.fcbayern.de/de/spiele/spielplan/champions-league/")
seite = response.read()
seite = seite.replace("\n", "") # einzeilig machen
mannschaften = re.findall('.{600}>- : -<.{300}', seite)
print "Als nächstes in der Champions League am", re.findall('matchday">[^<]+', mannschaften[0])[0].split(">")[1], "um",re.findall('time">[^<]+', mannschaften[0])[0].split(">")[1], "Uhr:"
mannschaften = re.findall('alt="[^"]+', mannschaften[0])
print mannschaften[0].split('"')[1], "gegen", mannschaften[1].split('"')[1]

response = br.open("http://www.fcbayern.de/de/spiele/spielplan/dfb-pokal/")
seite = response.read()
seite = seite.replace("\n", "") # einzeilig machen
mannschaften = re.findall('.{600}>- : -<.{300}', seite)
print "Als nächstes im DFB-Pokal im", re.findall('matchday">[^<]+', mannschaften[0])[0].split(">")[1], "um",re.findall('time">[^<]+', mannschaften[0])[0].split(">")[1], "Uhr:"
mannschaften = re.findall('alt="[^"]+', mannschaften[0])
print mannschaften[0].split('"')[1], "gegen", mannschaften[1].split('"')[1]


print "TODO: Motivations-Spruch des Tages, Mensa-Essen, Rezept des Tages"
response = br.open("http://chefkoch.de")
seite = response.read()
seite = seite.replace("\n", "") # einzeilig machen
receipt = re.findall('<a href="/rezept-des-tages.php">.{800}', seite)
#print receipt
receipt = re.findall('title="[^"]+',receipt[0])[1].split('"')[1]
print "CHEFKOCH Rezept des Tages:",receipt


print "Mensa-Essen"
response = br.open("http://www.studentenwerk-karlsruhe.de/de/essen/")
seite = response.read()
seite = seite.replace("\n", "") # einzeilig machen
seite = seite.split('<div id="canteen_place_2"')[0] # nur Mensa am Adenauerring!
price = re.findall('.{200}class="bgp price_1">[^&]+', seite)
for i in price:
	#print i
	j = i.split('price_1">')[1].replace(",", "")
	try:
		j = int(j)
		if int(j)>100:
			i = i.replace("<b>","!")
			i = i.replace("</b>","!")
			print "Essen:", i.split("!")[1], "Preis:", j/100.
	except: print ""
print "TODO: welche Linie?"

print "Oxford:"
response = br.open("http://www.oxford-studentenfutter.de/essenpub.html")
seite = response.read()
seite = seite.replace("\n", "") # einzeilig machen
#akttag = "<em>"++"</em>"
if lt.tm_wday < 5:
	wasgibts = re.findall(wochentag[lt.tm_wday]+'.{450}', seite)[0]
else:
	wasgibts = re.findall(wochentag[0]+'.{450}', seite)[0]
preise = re.findall("\d.\d\d", wasgibts)
essen = re.findall("<em>[^â]+", wasgibts)
for i in range(len(essen)):
	print str(essen[i].split(">")[1])+":", preise[i], "Euro"



print "Top-Schlagzeilen, SPIEGEL ONLINE:"
response = br.open("http://www.spiegel.de/schlagzeilen/tops/index.html")
seite = response.read().decode('iso-8859-1').replace("\n","")# einzeilig machen
seite = seite.replace(u'\xa0', u' ') # replaced with space
headline = re.findall('class="headline-intro">([^<]+)', seite)
headline2 = re.findall('class="headline">([^<]+)', seite)
#g = open("headline.txt", 'w')
#for i in range(len(headline)):
	#g.write(("{"+headline[i]+"}{"+headline2[i]+"}\n").encode('utf-8'))
#g.close()
response = br.open("http://www.studentenwerk-karlsruhe.de/de/essen/?view=ok&STYLE=popup_plain&c=adenauerring&p=1")
soup = BeautifulSoup(response.read().split('</style>')[2].decode('utf-8'))
print "BeautifulSoup-Test"
for i in soup.find_all('h1'):
	print i.string
for i in soup.find_all("span", "bg"):
	print i.b.string
for i in soup.table.find_all("span", "bgp price_1"):
	print i
print "Programm beendet."
