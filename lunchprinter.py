try:
    from PIL import Image
except ImportError:
    import Image			# Imagick image viewer and stuff, also needed for screenshots

import urllib.request			# for reading URLs
import pytesseract      		# it is important to install tesseract 4.0 which is not trivial for Ubuntu < 18.04 as default 						would there be version 3. One also has to install libtesseract-dev from terminal and of 					course pytesseract via pip
import re				# regual expressions tool for python
import datetime				# for current week number and week day
import tabula				# to read pdfs, important to install tabula-py and not tabula via pip
import numpy as np			# for array operations
from termcolor import colored 		# for colored terminal output
from robobrowser import RoboBrowser 	# for automatic browsing of 9b website 

###################################################################################################

#tesseract location (of executable/command!); 
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' 

#set week in year
weeknumber = datetime.date.today().isocalendar()[1]
if not datetime.date.today().weekday() < 5:	# for weekend we want next weeks menu
	weeknumber +=1  
weeknumber = str(weeknumber)  # for string concatenation later on
#set year:
year = str(datetime.date.today().year)

###################################################################################################

def lunchprinter(NeunBE, Mensa, Tech, Flags):
	
	mensa_names = ['Menü Classic: \t', 'Vegetarisch: \t', 'Tagesteller: \t']
	tech_names = ['Tagesteller: \t', 'Vegetarisch: \t', 'Pasta: \t\t']
	neunbe_names = ['Tagesmenü: \t', 'Monatsburger: \t', 'Wochenburger: \t']
	days = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'] 

	outfile_today = open("today_out.txt","w")
	outfile_tomorrow = open("tomorrow_out.txt","w")
	outfile_week = open("week_out.txt","w")
	for i in range(len(flags)):		
		outfile_today.write(flags[i])
		outfile_tomorrow.write(flags[i])
		outfile_week.write(flags[i])

	weekday = datetime.date.today().weekday()
	day = days[weekday]
		
	if weekday >= 5:
		mensa = Mensa[0]
		tech = Tech[0]
		neunbe = NeunBE[0]
		outfile_today.write("nächster Montag:\n")
		outfile_today.write("\nMensa:\n")
		for i in range(0,len(mensa)):
			outfile_today.write("\n"+mensa_names[i]+"\n\n"+mensa[i]+"\n")
		outfile_today.write("\nTechCafe:\n")
		for i in range(0,len(tech)):
			outfile_today.write("\n"+tech_names[i]+"\n\n"+tech[i]+"\n")
		outfile_today.write("\n9b:\n")
		for i in range(0,len(neunbe)):
			outfile_today.write("\n"+neunbe_names[i]+"\n\n"+neunbe[i]+"\n")
			
	else:
		mensa = Mensa[weekday]
		tech = Tech[weekday]
		neunbe = NeunBE[weekday]	
	
		outfile_today.write(day+":\n")
		outfile_today.write("\nMensa:\n")
		for i in range(0,len(mensa)):
			outfile_today.write("\n"+mensa_names[i]+"\n\n"+mensa[i]+"\n")
		outfile_today.write("\nTechCafe:\n")
		for i in range(0,len(tech)):
			outfile_today.write("\n"+tech_names[i]+"\n\n"+tech[i]+"\n")
		outfile_today.write("\n9b:\n")
		for i in range(0,len(neunbe)):
			outfile_today.write("\n"+neunbe_names[i]+"\n\n"+neunbe[i]+"\n")
	
	outfile_today.close()		
	weekday = (datetime.date.today()+datetime.timedelta(days=1)).weekday()	
	day = days[weekday]
		
	if weekday >= 5:
		mensa = Mensa[0]
		tech = Tech[0]
		neunbe = NeunBE[0]
		outfile_tomorrow.write("nächster Montag:\n")
		outfile_tomorrow.write("\nMensa:\n")
		for i in range(0,len(mensa)):
			outfile_tomorrow.write("\n"+mensa_names[i]+"\n\n"+mensa[i]+"\n")
		outfile_tomorrow.write("\nTechCafe:\n")
		for i in range(0,len(tech)):
			outfile_tomorrow.write("\n"+tech_names[i]+"\n\n"+tech[i]+"\n")
		outfile_tomorrow.write("\n9b:\n")
		for i in range(0,len(neunbe)):
			outfile_tomorrow.write("\n"+neunbe_names[i]+"\n\n"+neunbe[i]+"\n")
		
	else:
		mensa = Mensa[weekday]
		tech = Tech[weekday]
		neunbe = NeunBE[weekday]	
		
		outfile_tomorrow.write(day+":\n")
		outfile_tomorrow.write("\nMensa:\n")
		for i in range(0,len(mensa)):
			outfile_tomorrow.write("\n"+mensa_names[i]+"\n\n"+mensa[i]+"\n")
		outfile_tomorrow.write("\nTechCafe:\n")
		for i in range(0,len(tech)):
			outfile_tomorrow.write("\n"+tech_names[i]+"\n\n"+tech[i]+"\n")
		outfile_tomorrow.write("\n9b:\n")
		for i in range(0,len(neunbe)):
			outfile_tomorrow.write("\n"+neunbe_names[i]+"\n\n"+neunbe[i]+"\n")
	outfile_tomorrow.close()
	
	mensa = Mensa
	tech = Tech
	neunbe = NeunBE
	for j in range(0,len(days)-2):
		outfile_week.write(days[j]+':\n')
		outfile_week.write("\nMensa:\n")
		for i in range(0,len(mensa[j])):
			outfile_week.write("\n"+mensa_names[i]+"\n\n"+mensa[j][i]+"\n")
		outfile_week.write("\nTechCafe:\n")
		for i in range(0,len(tech[j])):
			outfile_week.write("\n"+tech_names[i]+"\n\n"+tech[j][i]+"\n")
		outfile_week.write("\n9b:\n")
		for i in range(0,len(neunbe[j])):
			outfile_week.write("\n"+neunbe_names[i]+"\n\n"+neunbe[j][i]+"\n")
	outfile_week.close()	
	
		
########## 9b - the people who can't name files in a coherent way ###############################
flags=[]

neunB_menu_file = "neunB_menu_week"+weeknumber+".jpg"

url_9b = 'http://neunbe.at/menue.html'
browser = RoboBrowser(history=True)
browser.open(url_9b)
request = browser.session.get(url_9b, stream=True)
corr_url = re.search("2019\" src=\"../pictures/((?s).*\">)", str(request.content))[0].split("<br>")[0].split("/")[2].split(".jpg\">")[0]

try: 
	urllib.request.urlretrieve("http://neunbe.at/pictures/"+corr_url+".jpg", neunB_menu_file)	

# should specify on which exception except should act (for all excepts in the script)
except:
	neunB_menu_file = "neunB_menu_week8.jpg"    # use a template menu from week 8/2019 so the rest at least works
	flags.append("9b Menǘ nicht verfügbar, eingetragenes Menü vermutlich falsch")

img = Image.open(neunB_menu_file)
area = (550,300,1300,1200)
img = img.crop(area)
#img.show()

# language option needs installation of file in usr/share/tessseract/4.00/tessdata
# --psm 6 is page separation mode option of tesseract, 6 uses image es single block of text, 3 is automatic/default
# psm 3 is better when there are empty lines in the day column before the actual day e.g. \nMontag 
out = pytesseract.image_to_string(img, lang="deu", config='--psm 3')
#print(out)

Mon = re.sub(" +", " ", re.search('Montag((?s).*)Dienstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Die = re.sub(" +", " ", re.search('Dienstag((?s).*)Mittwoch', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Mit = re.sub(" +", " ", re.search('Mittwoch((?s).*)Donnerstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Don = re.sub(" +", " ", re.search('Donnerstag((?s).*)Freitag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
Fre = re.sub(" +", " ", re.search('Freitag((?s).*)Monatsburger', out).group(1).replace("\n"," ").replace(" , ",", ").strip())

# TODO: add price to output?

MBurger = re.sub(" +", " ", re.search('Monatsburger:((?s).*)\s\u20AC((?s).*)Wochenburger', out).group(1).replace("\n", " ").replace(" , ",", ").strip())
WBurger = re.sub(" +", " ", re.search('Wochenburger:((?s).*)\s\u20AC', out).group(1).replace("\n", " ").replace(" , ",", ").strip())

daylist = [Mon,Die,Mit,Don,Fre]
NeunB = np.ndarray((5,3),dtype=object)

for ind in range(len(daylist)):		#add daily menu and specials which are available every day
	NeunB[ind][0] = daylist[ind] 
	NeunB[ind][1] = MBurger
	NeunB[ind][2] = WBurger

######### MENSA = locid 42    ##############################################################
mensa_file = "mensa_menu_week"+weeknumber+".pdf"
try:
	urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/42?woy="+weeknumber+"&year="+year,mensa_file)
except:
	mensa_file = "mensa_menu_week48.pdf"	
	flags.append("Mensa Menü nicht verfügbar, eingetragenes Menü vermutlich falsch")

# Read pdf into json style DataFrame
df = tabula.read_pdf(mensa_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

Men = np.ndarray((5,3),dtype=object)

for jnd in range(0,5):
	try:
	#only if menu pdf has 2 pages:
		if jnd != 4:
			for i in range(0,3):
				Men[jnd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", df[0]['data'][jnd+2][i+1]['text'].replace("\r", " "))
		else:
			for i in range(0,3):
				Men[jnd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", df[2]['data'][1][i+1]['text'].replace("\r", ", "))
	
	except:
	#single page:
		for i in range(0,3):
			Men[jnd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", df[0]['data'][jnd+2][i+1]['text'].replace("\r", " "))

######################### TECH = locid 55 ####################################################
tech_file = "tech_menu_week"+weeknumber+".pdf"
try:
	urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/55?woy="+weeknumber+"&year="+year,tech_file)
except: 
	tech_file = "tech_menu_week48.pdf"	
	flags.append("TechCafe Menü nicht verfügbar, eingetragenes Menü vermutlich falsch")

# similar as for mensa
df2 = tabula.read_pdf(tech_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

Tec = np.ndarray((5,3),dtype=object)

for knd in range(0,5):
	for i in range(0,3):
		Tec[knd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", re.sub(' *\((.*?)\)', "", df2[0]['data'][knd+2][i+1]['text'].replace("\r", " ")))
# here additional regex search for things in brackets as these are usually(!) just allergy informations

###################################################################################################

lunchprinter(NeunB,Men,Tec,flags)

#TODO delete files after reading?!
