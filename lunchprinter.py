try:
    from PIL import Image
except ImportError:
    import Image		# Imagick image viewer and stuff, also needed for screenshots

import urllib.request		# for reading URLs
import pytesseract      	# it is important to install tesseract 4.0 which is not trivial for Ubuntu < 18.04 as default would there 					be version 3. One also hast to install libtesseract-dev from terminal and of course pytesseract via pip
import re			# regual expressions tool for python
import datetime			# for current week number and week day
import tabula			# to read pdfs, important to install tabula-py and not tabula via pip
import numpy as np		# for array operations

###################################################################################################

#tesseract location (of executable/command!); 
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

#set week in year
if datetime.date.today().weekday() < 5:
	weeknumber = str(datetime.date.today().isocalendar()[1])  #needed as string for concatenation
else:
	weeknumber = str(datetime.date.today().isocalendar()[1]+1)

###################################################################################################

def lunchprinter(NeunBE, Mensa, Tech, wholeweek=False, tomorrow=False):
	
	mensa_names = ['Menü Classic: \t', 'Vegetarisch: \t', 'Tagesteller: \t']
	tech_names = ['Tagesteller: \t', 'Vegetarisch: \t', 'Pasta: \t\t']
	neunbe_names = ['Tagesmenü: \t', 'Monatsburger: \t', 'Wochenburger: \t', 'Wochenaktion: \t']
	days = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'] 

	if wholeweek == True:
		mensa = Mensa
		tech = Tech
		neunbe = NeunBE

		for j in range(0,len(days)-2):
			print('--------------------------- '+days[j]+' ---------------------------', "\n")
			print("------------ Mensa ------------", "\n")
			for i in range(0,len(mensa[j])):
				print(mensa_names[i],mensa[j][i],"\n")
			print("------------ Tech ------------", "\n")
			for i in range(0,len(tech[j])):
				print(tech_names[i],tech[j][i],"\n")
			print("------------ 9b ------------", "\n")
			for i in range(0,len(neunbe[j])):
				print(neunbe_names[i],neunbe[j][i],"\n")
	else:	

		if tomorrow == False:
			weekday = datetime.date.today().weekday()
		
		else:
			weekday = (datetime.date.today()+datetime.timedelta(days=1)).weekday()	
		
		day = days[weekday]
		
		if weekday >= 5:
			mensa = Mensa[0]
			tech = Tech[0]
			neunbe = NeunBE[0]

			print("--------------------------- nächster Montag ---------------------------")
			print("------------ Mensa ------------", "\n")
			for i in range(0,len(mensa)):
				print(mensa_names[i],mensa[i],"\n")
			print("------------ Tech ------------", "\n")
			for i in range(0,len(tech)):
				print(tech_names[i],tech[i],"\n")
			print("------------ 9b ------------", "\n")
			for i in range(0,len(neunbe)):
				print(neunbe_names[i],neunbe[i],"\n")
			
		else:
			mensa = Mensa[weekday]
			tech = Tech[weekday]
			neunbe = NeunBE[weekday]	
			
			print("--------------------------- "+day+" ---------------------------", "\n")
			print("------------ Mensa ------------", "\n")
			for i in range(0,len(mensa)):
				print(mensa_names[i],mensa[i],"\n")
			print("------------ Tech ------------", "\n")
			for i in range(0,len(tech)):
				print(tech_names[i],tech[i],"\n")
			print("------------ 9b ------------", "\n")
			for i in range(0,len(neunbe)):
				print(neunbe_names[i],neunbe[i],"\n")
			
########## 9b - the people who can't name files in a coherent way ###############################
neunB_menu_file = "neunB_menu_week"+weeknumber+".jpg"

try: 
	urllib.request.urlretrieve("http://neunbe.at/pictures/KW"+weeknumber+".jpg", neunB_menu_file) 
	# often name changes so check before relying on information generated from this
except:
	neunB_menu_file = "neunB_menu_week46.jpg"    # use a template menu from week 46 so the rest at least works

img = Image.open(neunB_menu_file)
area = (380,200,825,500)   #these change from week to week unfortunatley, so they have to be adjusted manually every week
img_crop = img.crop(area)
#img_crop.show()	# shows the image from which text is extracted, has to show monday to friday with menu but nothing else

area2 = (350,520,825,850)  #these change from week to week unfortunatley, so they have to be adjusted manually every week
img_crop2 = img.crop(area2)
#img_crop2.show() 	# shows the image from which text is extracted, has to show specials but not the menu or other stuff

       
out = pytesseract.image_to_string(img_crop, lang="deu", config='--psm 6')
# language option needs installation of file in usr/share/tessseract/4.00/tessdata
# --psm 6 is argument/option for tesseract to sort tables differently (not always needed, but seems to do nothing bad if not needed)

Mon = re.sub(" +", " ", re.search('Montag((?s).*)Dienstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Die = re.sub(" +", " ", re.search('Dienstag((?s).*)Mittwoch', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Mit = re.sub(" +", " ", re.search('Mittwoch((?s).*)Donnerstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Don = re.sub(" +", " ", re.search('Donnerstag((?s).*)Freitag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Fre = re.sub(" +", " ", re.search('Freitag((?s).*)', out).group(1).replace("\n"," ").replace(" , ",", ").strip())

out2 = pytesseract.image_to_string(img_crop2, lang='deu',config='--psm 6')

MBurger = re.sub(" +", " ", re.search('Monatsburger:((?s).*)Wochenburger', out2).group(1).replace("\n", " ").replace(" , ",", ").strip())
WBurger = re.sub(" +", " ", re.search('Wochenburger:((?s).*)Wochenaktion', out2).group(1).replace("\n", " ").replace(" , ",", ").strip())
WAktion  = re.sub(" +", " ", re.search('Wochenaktion:((?s).*)', out2).group(1).replace("\n", " ").replace(" , ",", ").strip())  
#WAktion often changes actual name --> check if strings need to be adjusted for consistency

daylist = [Mon,Die,Mit,Don,Fre]
NeunB = np.ndarray((5,4),dtype=object)

for ind in range(0,5):		#add daily menu and specials which are available every day
	NeunB[ind][0] = daylist[ind] 
	NeunB[ind][1] = MBurger
	NeunB[ind][2] = WBurger
	NeunB[ind][3] = WAktion

######### MENSA = locid 42    ##############################################################
mensa_file = "mensa_menu_week"+weeknumber+".pdf"
urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/42?woy="+weeknumber+"&year=2018",mensa_file)

# Read pdf into json style DataFrame
df = tabula.read_pdf(mensa_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

Men = np.ndarray((5,3),dtype=object)

for jnd in range(0,5):
	if jnd != 4:
		for i in range(0,3):
			Men[jnd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", df[0]['data'][jnd+2][i+1]['text'].replace("\r", " "))
	else:
		for i in range(0,3):
			Men[jnd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", df[2]['data'][1][i+1]['text'].replace("\r", ", "))
#regex used to remove prices and for formatting of the strings

######################### TECH = locid 55 ####################################################
tech_file = "tech_menu_week"+weeknumber+".pdf"
urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/55?woy="+weeknumber+"&year=2018",tech_file)

# similar as for mensa
df2 = tabula.read_pdf(tech_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

Tec = np.ndarray((5,3),dtype=object)

for knd in range(0,5):
	for i in range(0,3):
		Tec[knd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", re.sub(' *\((.*?)\)', "", df2[0]['data'][knd+2][i+1]['text'].replace("\r", " ")))
# here additional regex search for things in brackets as these are usually(!) just allergy informations

###################################################################################################

lunchprinter(NeunB,Men,Tec,wholeweek = False, tomorrow = False) #wholeweek and tomorrow are optional and False by default 	
