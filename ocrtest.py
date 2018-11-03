try:
    from PIL import Image
except ImportError:
    import Image

import urllib.request
import pytesseract
import re
import datetime
import numpy as np
import pandas
import tabula
import pprint


###################################################################################################

#tesseract location
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

##################################################################################################

#urllib.request.urlretrieve("http://neunbe.at/pictures/44-111MENUE111--.jpg", "test.jpg") #9be FAIL

img = (Image.open('test.jpg'))
area = (350,220,800,500)
img_crop = img.crop(area)
#img_crop.show()

area2 = (320,500,850,775)
img_crop2 = img.crop(area2)
#img_crop2.show()

#language option needs installation of file in usr/share/tessseract/4.00/tessdata
#print(type(pytesseract.image_to_string(img_crop, lang='deu')))
out = (pytesseract.image_to_string(img_crop, lang='deu'))
#print(out)

Mon = re.search('Montag((?s).*)Dienstag',out).group(1)
Die = re.search('Dienstag((?s).*)Mittwoch',out).group(1)
Mit = re.search('Mittwoch((?s).*)Donnerstag',out).group(1)
Don = re.search('Donnerstag((?s).*)Freitag',out).group(1)
Fre = re.search('Freitag((?s).*)',out).group(1)

Mon = re.sub(" +"," ",Mon.replace("\n"," ").strip())
Die = re.sub(" +"," ",Die.replace("\n"," ").strip())
Mit = re.sub(" +"," ",Mit.replace("\n"," ").strip())
Don = re.sub(" +"," ",Don.replace("\n"," ").strip())
Fre = re.sub(" +"," ",Fre.replace("\n"," ").strip())

#print(Mon)
#print(Die)
#print(Mit)
#print(Don)
#print(Fre)

out2 = (pytesseract.image_to_string(img_crop2, lang='deu'))
#print(out2)

MBurger = re.search('Monatsburger:((?s).*)Wochenburger',out2).group(1)
WBurger = re.search('Wochenburger:((?s).*)Oktober',out2).group(1)
MAktion = re.search('Aktion:((?s).*)',out2).group(1)
MBurger = re.sub(" +"," ",MBurger.replace("\n"," ").strip())
WBurger = re.sub(" +"," ",WBurger.replace("\n"," ").strip())
MAktion = re.sub(" +"," ",MAktion.replace("\n"," ").strip())

#print(MBurger)
#print(WBurger)
#print(MAktion)

###################################################################################################
#Mensa/Tech
#menu.mensen.at//index/menu-pdf/locid/42?woy=45&year=2018
urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/42?woy=45&year=2018","test.pdf")


today = datetime.date.today()
thisweek = today.isocalendar()[1]
weekday = ("Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag")[today.weekday()]
#print(weekday)

###################################################################################################
# Read pdf into DataFrame
df = tabula.read_pdf("test.pdf", pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

#pprint.pprint(df[0]['data'][2][1]['text']) # [2 = montag] [1= Menü Classic]
#pprint.pprint(df[2]['data'][1][1]['text']) # 1 = friday 1= menu classic

men_mon_men = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][2][1]['text'].replace("\r",", "))) 
men_mon_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][2][2]['text'].replace("\r",", "))) 
men_mon_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][2][3]['text'].replace("\r",", ")))

men_die_men = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][3][1]['text'].replace("\r",", "))) 
men_die_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][3][2]['text'].replace("\r",", "))) 
men_die_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][3][3]['text'].replace("\r",", ")))

men_mit_men = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][4][1]['text'].replace("\r",", "))) 
men_mit_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][4][2]['text'].replace("\r",", "))) 
men_mit_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][4][3]['text'].replace("\r",", ")))

men_don_men = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][5][1]['text'].replace("\r",", "))) 
men_don_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][5][2]['text'].replace("\r",", "))) 
men_don_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[0]['data'][5][3]['text'].replace("\r",", ")))

men_fre_men = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[2]['data'][1][1]['text'].replace("\r",", "))) 
men_fre_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[2]['data'][1][2]['text'].replace("\r",", "))) 
men_fre_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df[2]['data'][1][3]['text'].replace("\r",", ")))

Men={'Mon':{'Menü Classic': men_mon_men,'Vegetarisch': men_mon_veg,'Tagesteller': men_mon_tag},'Die':{'Menü Classic': men_die_men,'Vegetarisch': men_die_veg,'Tagesteller': men_die_tag},'Mit':{'Menü Classic': men_mit_men,'Vegetarisch': men_mit_veg,'Tagesteller': men_mit_tag},'Don':{'Menü Classic': men_don_men,'Vegetarisch': men_don_veg,'Tagesteller': men_don_tag},'Fre':{'Menü Classic': men_fre_men,'Vegetarisch': men_fre_veg,'Tagesteller': men_fre_tag}}

pprint.pprint(Men)
######################### TECH ####################################################

urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/55?woy=45&year=2018","test2.pdf")

df2 = tabula.read_pdf("test2.pdf", pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")
#pprint.pprint(df2[0]['data'][2][1]['text'])

tec_mon_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][2][1]['text'].replace("\r",", "))) 
tec_mon_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][2][2]['text'].replace("\r",", "))) 
tec_mon_pas = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][2][3]['text'].replace("\r",", ")))

tec_die_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][3][1]['text'].replace("\r",", "))) 
tec_die_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][3][2]['text'].replace("\r",", "))) 
tec_die_pas = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][3][3]['text'].replace("\r",", ")))

tec_mit_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][4][1]['text'].replace("\r",", "))) 
tec_mit_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][4][2]['text'].replace("\r",", "))) 
tec_mit_pas = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][4][3]['text'].replace("\r",", ")))

tec_don_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][5][1]['text'].replace("\r",", "))) 
tec_don_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][5][2]['text'].replace("\r",", "))) 
tec_don_pas = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][5][3]['text'].replace("\r",", ")))

tec_fre_tag = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][6][1]['text'].replace("\r",", "))) 
tec_fre_veg = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][6][2]['text'].replace("\r",", "))) 
tec_fre_pas = re.sub('(€ ?\d+\,\d{1,2})',"", re.sub(' *\((.*?)\)',"",df2[0]['data'][6][3]['text'].replace("\r",", ")))

Tec={'Mon':{'Tagesteller': tec_mon_tag,'Vegetarisch': tec_mon_veg,'Pasta': tec_mon_pas},'Die':{'Tagesteller': tec_die_tag,'Vegetarisch': tec_die_veg,'Pasta': tec_die_pas},'Mit':{'Tagesteller': tec_mit_tag,'Vegetarisch': tec_mit_veg,'Pasta': tec_mit_pas},'Don':{'Tagesteller': tec_don_tag,'Vegetarisch': tec_don_veg,'Pasta': tec_don_pas},'Fre':{'Tagesteller': tec_fre_tag,'Vegetarisch': tec_fre_veg,'Pasta': tec_fre_pas}}

pprint.pprint(Tec)
