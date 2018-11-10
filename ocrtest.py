try:
    from PIL import Image
except ImportError:
    import Image

import urllib.request
import pytesseract
import re
import datetime
import tabula
import pprint
import numpy as np

###################################################################################################

#tesseract location
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

#weeknumber hardcoded for now TODO: be able to look at any week the user wants, only possible for Mensa & Tech though, 9b uploads their menu on sunday

weeknumber = str(datetime.date.today().isocalendar()[1])  #needed as string for concatenation

###################################################################################################

#general TODO: print mondays lunch on weekends
# also TODO: print weekplan without alphabetical ordering
# TODO as always clean up code

def lunchprinter(NeunBE, Mensa, Tech, wholeweek=False, tomorrow=False):
	
	if wholeweek == True:
		mensa = Mensa
		tech = Tech
		neunbe = NeunBE
		print('TODO - Wochenplan anzeigen')

	else:	

		if tomorrow == False:
			weekday = datetime.date.today().weekday()
		
		else:
			weekday = (datetime.date.today()+datetime.timedelta(days=1)).weekday()	
		
		day = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'][weekday]
		
		if weekday >= 5:
			print("Hoch die Hände Wochenende!")
		else:
			mensa = Mensa[weekday]
			tech = Tech[weekday]
			neunbe = NeunBE[weekday]	
			print('TODO - Tagesmenü anzeigen')
			
########## 9b - the people who can't name files in a coherent way ###############################
neunB_menu_file = "neunB_menu"+weeknumber+".jpg"

urllib.request.urlretrieve("http://neunbe.at/pictures/"+weeknumber+"-111MENUE111--.jpg", neunb_menu_file) #9be FAILS a lot but seems to keep this name going for at least two consecutive weeks.

img = (Image.open(neunB_week_file))
area = (380,240,795,500)   #these change from week to week unfortunatley, so they have to be adjusted manually every week
img_crop = img.crop(area)
#img_crop.show()

area2 = (350,520,825,850)  #these change from week to week unfortunatley, so they have to be adjusted manually every week
img_crop2 = img.crop(area2)
#img_crop2.show()

#language option needs installation of file in usr/share/tessseract/4.00/tessdata

out = (pytesseract.image_to_string(img_crop, lang='deu', config='--psm 6'))

Mon = re.sub(" +", " ", re.search('Montag((?s).*)Dienstag', out).group(1).replace("\n"," ").strip())
Die = re.sub(" +", " ", re.search('Dienstag((?s).*)Mittwoch', out).group(1).replace("\n"," ").strip())
Mit = re.sub(" +", " ", re.search('Mittwoch((?s).*)Donnerstag', out).group(1).replace("\n"," ").strip())
Don = re.sub(" +", " ", re.search('Donnerstag((?s).*)Freitag', out).group(1).replace("\n"," ").strip())
Fre = re.sub(" +", " ", re.search('Freitag((?s).*)', out).group(1).replace("\n"," ").strip())

out2 = (pytesseract.image_to_string(img_crop2, lang='deu',config='--psm 6'))

MBurger = re.sub(" +", " ", re.search('Monatsburger:((?s).*)Wochenburger', out2).group(1).replace("\n", " ").strip())
WBurger = re.sub(" +", " ", re.search('Wochenburger:((?s).*)Wochencurry', out2).group(1).replace("\n", " ").strip())
WCurry = re.sub(" +", " ", re.search('Wochencurry;((?s).*)', out2).group(1).replace("\n", " ").strip())  # stupid 9b can't write for shit  ; != :

daylist = [Mon,Die,Mit,Don,Fre]
NeunB = np.ndarray((5,4),dtype=object)

for ind in range(0,5):
	NeunB[ind][0] = daylist[ind]
	NeunB[ind][1] = MBurger
	NeunB[ind][2] = WBurger
	NeunB[ind][3] = WCurry

######### MENSA = locid 42    ##############################################################
mensa_file = "mensa_menu_week"+weeknumber+".pdf"
urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/42?woy="+weeknumber+"&year=2018",mensa_file)

# Read pdf into DataFrame
df = tabula.read_pdf(mensa_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

Men = np.ndarray((5,3),dtype=object)

for jnd in range(0,5):
	if jnd != 4:
		for i in range(0,3):
			Men[jnd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", df[0]['data'][jnd+2][i+1]['text'].replace("\r", ", "))
	else:
		for i in range(0,3):
			Men[jnd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", df[2]['data'][1][i+1]['text'].replace("\r", ", "))

######################### TECH = locid 55 ####################################################
tech_file = "tech_menu_week"+weeknumber+".pdf"
urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/55?woy="+weeknumber+"&year=2018",tech_file)

df2 = tabula.read_pdf(tech_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

Tec = np.ndarray((5,3),dtype=object)

for knd in range(0,5):
	for i in range(0,3):
		Tec[knd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", re.sub(' *\((.*?)\)', "", df2[0]['data'][knd+2][i+1]['text'].replace("\r", ", ")))

###################################################################################################

lunchprinter(NeunB,Men,Tec,wholeweek=False,tomorrow=False) #wholeweek and tomorrow are optional and False by default 	
