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
from robobrowser import RoboBrowser 	# for automatic browsing of 9b website 

###################################################################################################

#tesseract location (of executable/command!); 
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' 

#set week in year
weeknumber = datetime.date.today().isocalendar()[1]
if not datetime.date.today().weekday() < 5:		# for weekend we want next weeks menu
	weeknumber +=1  
weeknumber = str(weeknumber)  				# for string concatenation later on
#set year:
year = str(datetime.date.today().year)

###################################################################################################
#TODO WIP menue getter functions for correct week
#idea: function that takes location, weeknumber and day which can be called multiple times

def getMenue(place,week=0,day=0):   #default values for week (0 = current week) and day (0= Monday?!)
	
	currentWeek = datetime.date.today().isocalendar()[1]
	currentYear = datetime.date.today().year
	if not (week == 0 or week ==1):
		raise Exception("Menu can only be retrieved for current week (0) or next week (1)")
	else:
		if place == "Mensa":
			pass #TODO temp
	
		elif place == "Tech":
			pass #TODO temp
			
		elif place == "9b":
			if week != 0:
				raise Exception("9b menu not available for the coming week")	
			elif day < 5:
				file_9b = "neunB_menu_week"+str(currentWeek+week)+".jpg"
				url_9b = 'http://neunbe.at/menue.html'
				browser = RoboBrowser(history=True)
				try:
					browser.open(url_9b)
					request = browser.session.get(url_9b, stream=True)
					corr_url = re.search("2019\" src=\"../pictures/((?s).*\">)", str(request.content))[0].split("<br>")[0].split("/")[2].split(".jpg\">")[0]

				except TypeError:
					raise Exception("9b menue page down, current menu not available")
					return ("Sorry, no menue for 9b available at the moment") 
				try: 
					urllib.request.urlretrieve("http://neunbe.at/pictures/"+corr_url+".jpg", file_9b)	
				except:  #should specify on which error except should be
					raise Exception("9b menue not found (probably not uploaded yet)")
					return ("Sorry, no menue for 9b available at the moment") 
				
				area = (580,310,1300,1300)  # TODO automatically find this area
				img = Image.open(file_9b).crop(area)
				try:
					ocr = pytesseract.image_to_string(img, lang="deu", config='--psm 6')
					Mo = re.sub(" +", " ", re.search('Montag((?s).*)Dienstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Di = re.sub(" +", " ", re.search('Dienstag((?s).*)Mittwoch', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Mi = re.sub(" +", " ", re.search('Mittwoch((?s).*)Donnerstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Do = re.sub(" +", " ", re.search('Donnerstag((?s).*)Freitag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Fr = re.sub(" +", " ", re.search('Freitag((?s).*)Monatsburger', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
				except AttributeError:
					ocr = pytesseract.image_to_string(img, lang="deu", config='--psm 3')
					Mo = re.sub(" +", " ", re.search('Montag((?s).*)Dienstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Di = re.sub(" +", " ", re.search('Dienstag((?s).*)Mittwoch', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Mi = re.sub(" +", " ", re.search('Mittwoch((?s).*)Donnerstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Do = re.sub(" +", " ", re.search('Donnerstag((?s).*)Freitag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
					Fr = re.sub(" +", " ", re.search('Freitag((?s).*)Monatsburger', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
				
				MBurger = re.sub(" +", " ", re.search('Monatsburger:((?s).*)\s\u20AC((?s).*)Wochenburger', out).group(1).replace("\n", " ").replace(" , ",", ").strip())
				try:
					WBurger = re.sub(" +", " ", re.search('Wochenburger:((?s).*)\s\u20AC', out).group(1).replace("\n", " ").replace(" , ",", ").strip())
				except AttributeError:
					WBurger = re.sub(" +", " ", re.search('Wochenburger:((?s).*)Valle', out).group(1).replace("\n", " ").replace(" , ",", ").strip())
				out_obj_9b = [[Mo,Di,Mi,Do,Fr][day],MBurger,WBurger]
				return out_obj_9b
			elif day>=5:
				raise Exception("9b menu not available for the coming week")
				return ("Sorry, no menue for 9b avalaible at the moment")
	
		else:
			raise Exception("First argument has to be 'Mensa', 'Tech' or '9b'")

# TODO Look up how to catch Exception (probably try except blocks)
# for testing:
#print(getMenue("9b",0,0))
###################################################################################################
def lunchPrinter(NeunBE, Mensa, Tech, Flags, DevFlags):
	
	mensa_names = ['_Menü Classic:_ \t', '_Vegetarisch:_ \t', '_Tagesteller:_ \t']
	tech_names = ['_Tagesteller:_ \t', '_Vegetarisch:_ \t', '_Pasta:_ \t\t']
	neunbe_names = ['_Tagesmenü:_ \t', '_Monatsburger:_ \t', '_Wochenburger:_ \t']
	days = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'] 

	outfile_today = open("today_out.txt","w")
	outfile_tomorrow = open("tomorrow_out.txt","w")
	outfile_week = open("week_out.txt","w")
	outfile_dev_flags = open("dev_flags_out.txt","w")

	for i in range(len(Flags)):		
		outfile_today.write(Flags[i])
		outfile_tomorrow.write(Flags[i])
		outfile_week.write(Flags[i])

	for j in range(len(DevFlags)):
		outfile_dev_flags.write(DevFlags[j])

	weekday = datetime.date.today().weekday()
	day = days[weekday]
		
	if weekday >= 5:
		mensa = Mensa[0]
		tech = Tech[0]
		neunbe = NeunBE[0]
		outfile_today.write("*nächster Montag:* \n")
		outfile_today.write("\n *Mensa:* \n")
		for i in range(0,len(mensa)):
			outfile_today.write(mensa_names[i]+"\n  "+mensa[i]+"\n")
		outfile_today.write("\n *TechCafe:* \n")
		for i in range(0,len(tech)):
			outfile_today.write(tech_names[i]+"\n  "+tech[i]+"\n")
		outfile_today.write("\n *9b:* \n")
		for i in range(0,len(neunbe)):
			outfile_today.write(neunbe_names[i]+"\n  "+neunbe[i]+"\n")
			
	else:
		mensa = Mensa[weekday]
		tech = Tech[weekday]
		neunbe = NeunBE[weekday]	
	
		outfile_today.write("*"+day+":* \n")
		outfile_today.write("\n *Mensa:* \n")
		for i in range(0,len(mensa)):
			outfile_today.write(mensa_names[i]+"\n  "+mensa[i]+"\n")
		outfile_today.write("\n *TechCafe:* \n")
		for i in range(0,len(tech)):
			outfile_today.write(tech_names[i]+"\n  "+tech[i]+"\n")
		outfile_today.write("\n *9b:* \n")
		for i in range(0,len(neunbe)):
			outfile_today.write(neunbe_names[i]+"\n  "+neunbe[i]+"\n")
	
	outfile_today.close()		
	weekday = (datetime.date.today()+datetime.timedelta(days=1)).weekday()	# go from today to tomorrow
	day = days[weekday]
	
	# TODO this doesn't actually give any information about the real menue next week, need to actually load future menu ^^
	if weekday >= 5:
		mensa = Mensa[0]
		tech = Tech[0]
		neunbe = NeunBE[0]
		outfile_tomorrow.write("*nächster Montag:* \n")
		outfile_tomorrow.write("\n *Mensa:* \n")
		for i in range(0,len(mensa)):
			outfile_tomorrow.write(mensa_names[i]+"\n  "+mensa[i]+"\n")
		outfile_tomorrow.write("\n *TechCafe:* \n")
		for i in range(0,len(tech)):
			outfile_tomorrow.write(tech_names[i]+"\n  "+tech[i]+"\n")
		outfile_tomorrow.write("\n *9b:* \n")
		for i in range(0,len(neunbe)):
			outfile_tomorrow.write(neunbe_names[i]+"\n  "+neunbe[i]+"\n")
		
	else:
		mensa = Mensa[weekday]
		tech = Tech[weekday]
		neunbe = NeunBE[weekday]	
		
		outfile_tomorrow.write("*"+day+":* \n")
		outfile_tomorrow.write("\n *Mensa:* \n")
		for i in range(0,len(mensa)):
			outfile_tomorrow.write(mensa_names[i]+"\n  "+mensa[i]+"\n")
		outfile_tomorrow.write("\n *TechCafe:* \n")
		for i in range(0,len(tech)):
			outfile_tomorrow.write(tech_names[i]+"\n  "+tech[i]+"\n")
		outfile_tomorrow.write("\n *9b:* \n")
		for i in range(0,len(neunbe)):
			outfile_tomorrow.write(neunbe_names[i]+"\n  "+neunbe[i]+"\n")
	outfile_tomorrow.close()
	
	# whole week:
	mensa = Mensa
	tech = Tech
	neunbe = NeunBE
	for j in range(0,len(days)-2):
		outfile_week.write("*"+days[j]+':* \n')
		outfile_week.write("\n *Mensa:* \n")
		for i in range(0,len(mensa[j])):
			outfile_week.write(mensa_names[i]+"\n  "+mensa[j][i]+"\n")
		outfile_week.write("\n *TechCafe:* \n")
		for i in range(0,len(tech[j])):
			outfile_week.write(tech_names[i]+"\n  "+tech[j][i]+"\n")
		outfile_week.write("\n *9b:* \n")
		for i in range(0,len(neunbe[j])):
			outfile_week.write(neunbe_names[i]+"\n  "+neunbe[j][i]+"\n")
	outfile_week.close()	

		
########## 9b - the people who can't name files in a coherent way ###############################
flags=[]
dev_flags=[]

neunB_menu_file = "neunB_menu_week"+weeknumber+".jpg"

url_9b = 'http://neunbe.at/menue.html'
browser = RoboBrowser(history=True)
try:
	browser.open(url_9b)
	request = browser.session.get(url_9b, stream=True)
	corr_url = re.search("2019\" src=\"../pictures/((?s).*\">)", str(request.content))[0].split("<br>")[0].split("/")[2].split(".jpg\">")[0]

except TypeError:
	dev_flags.append("9b menue page down\n")
	neunB_menu_file = "neunB_menu_DEFAULT.jpg"    # use a template menu from week 8/2019 so the rest at least works
	flags.append("*9b Menü nicht verfügbar, eingetragenes Menü vermutlich falsch* \n")

try: 
	urllib.request.urlretrieve("http://neunbe.at/pictures/"+corr_url+".jpg", neunB_menu_file)	

# should specify on which exception except should act (for all excepts in the script)
except:
	dev_flags.append("9b menue probably not uploaded yet\n")
	neunB_menu_file = "neunB_menu_DEFAULT.jpg"    # use a template menu from week 8/2019 so the rest at least works
	flags.append("*9b Menü nicht verfügbar, eingetragenes Menü vermutlich falsch*\n")

img = Image.open(neunB_menu_file)
area = (580,310,1300,1300)
img = img.crop(area)
#img.show()

# notes on pytesseract:
# language option needs installation of training files in usr/share/tessseract/4.00/tessdata
# --psm is page separation mode option of tesseract, 6 uses image es single block of text, 3 is automatic/default
# psm 3 is better when there are empty lines in the day column before the actual day e.g. \nMontag 
# psm 6 recovers text better (both grammar and orthography) but does not work all the time, so try this first

# have to put all Mon/Die/Mit/Don/Fre in the try block as they can give AttributeErrors in addition to out
try:
	out = pytesseract.image_to_string(img, lang="deu", config='--psm 6')
	Mon = re.sub(" +", " ", re.search('Montag((?s).*)Dienstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Die = re.sub(" +", " ", re.search('Dienstag((?s).*)Mittwoch', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Mit = re.sub(" +", " ", re.search('Mittwoch((?s).*)Donnerstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Don = re.sub(" +", " ", re.search('Donnerstag((?s).*)Freitag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Fre = re.sub(" +", " ", re.search('Freitag((?s).*)Monatsburger', out).group(1).replace("\n"," ").replace(" , ",", ").strip())

except AttributeError:
	dev_flags.append("--psm 3 was used\n")
	out = pytesseract.image_to_string(img, lang="deu", config='--psm 3')
	Mon = re.sub(" +", " ", re.search('Montag((?s).*)Dienstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Die = re.sub(" +", " ", re.search('Dienstag((?s).*)Mittwoch', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Mit = re.sub(" +", " ", re.search('Mittwoch((?s).*)Donnerstag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Don = re.sub(" +", " ", re.search('Donnerstag((?s).*)Freitag', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
	Fre = re.sub(" +", " ", re.search('Freitag((?s).*)Monatsburger', out).group(1).replace("\n"," ").replace(" , ",", ").strip())
#print(out)

# TODO: add price to output? consistently remove (or add) allergy information?

MBurger = re.sub(" +", " ", re.search('Monatsburger:((?s).*)\s\u20AC((?s).*)Wochenburger', out).group(1).replace("\n", " ").replace(" , ",", ").strip())

# try block for the case that the price is not read by pytesseract or ommited by the menue creator
try:
	WBurger = re.sub(" +", " ", re.search('Wochenburger:((?s).*)\s\u20AC', out).group(1).replace("\n", " ").replace(" , ",", ").strip())

except AttributeError:
	WBurger = re.sub(" +", " ", re.search('Wochenburger:((?s).*)Valle', out).group(1).replace("\n", " ").replace(" , ",", ").strip())

daylist = [Mon,Die,Mit,Don,Fre]
NeunB = np.ndarray((5,3),dtype=object)

for ind in range(len(daylist)):		#add daily menu and specials which are available every day
	NeunB[ind][0] = daylist[ind] 
	NeunB[ind][1] = MBurger
	NeunB[ind][2] = WBurger

#TODO do not print MBurger and WBurger 5 times?!

######### MENSA = locid 42    ##############################################################
mensa_file = "mensa_menu_week"+weeknumber+".pdf"
try:
	urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/42?woy="+weeknumber+"&year="+year,mensa_file)
except:
	mensa_file = "mensa_menu_DEFAULT.pdf"	
	flags.append("*Mensa Menü nicht verfügbar, eingetragenes Menü vermutlich falsch* \n")

# Read pdf into json style DataFrame
df = tabula.read_pdf(mensa_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

#for the case of empty pdf of the menue
if len(df) < 1:
	mensa_file = "mensa_menu_DEFAULT.pdf"
	df = tabula.read_pdf(mensa_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")	
	flags.append("*Mensa Menü nicht verfügbar, eingetragenes Menü vermutlich falsch* \n")

Men = np.ndarray((5,3),dtype=object)

# try blocks for different pdf lengths. usually menue has two pages but single page and three page is covered as well. three page is special as it probably was a one time thing with additional strange formatting
try:
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
except:
	for jnd in range(0,5):
		# triple page shenanigans:
		if jnd == 0 or jnd == 1:
			for i in range(0,3):
				Men[jnd][i] = re.sub("!!(.*)!!","",re.sub('(€ ?\d+\,\d{1,2})', "", df[0]['data'][jnd+2][i+1]['text'].replace("\r", " ")))
				
		elif jnd == 2 or jnd == 3:			
			for i in range(0,3):
				Men[jnd][i] = re.sub("!!(.*)!!","",re.sub('(€ ?\d+\,\d{1,2})', "", df[2]['data'][jnd-1][i+1]['text'].replace("\r", ", ")))
		else:
			for i in range(0,3):
				Men[jnd][i] = re.sub("!!(.*)!!","",re.sub('(€ ?\d+\,\d{1,2})', "", df[4]['data'][1][i+1]['text'].replace("\r", ", ")))

######################### TECH = locid 55 ####################################################
tech_file = "tech_menu_week"+weeknumber+".pdf"
try:
	urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/55?woy="+weeknumber+"&year="+year,tech_file)
except: 
	tech_file = "tech_menu_DEFAULT.pdf"	
	flags.append("*TechCafe Menü nicht verfügbar, eingetragenes Menü vermutlich falsch* \n")

# similar as for mensa
df2 = tabula.read_pdf(tech_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")

#for the case of empty pdf of the menue
if len(df2) < 1:
	tech_file = "tech_menu_DEFAULT.pdf"
	df2 = tabula.read_pdf(tech_file, pages="all", lattice=True, guess=True, mulitple_tables=True ,output_format="json")	
	flags.append("*TechCafe Menü nicht verfügbar, eingetragenes Menü vermutlich falsch* \n")

Tec = np.ndarray((5,3),dtype=object)

# only works for single page menues, but no multi page menues have been observed over the past months.
for knd in range(0,5):
	for i in range(0,3):
		Tec[knd][i] = re.sub('(€ ?\d+\,\d{1,2})', "", re.sub(' *\((.*?)\)', "", df2[0]['data'][knd+2][i+1]['text'].replace("\r", " ")))
# here additional regex search for things in brackets as these are usually(!) just allergy informations

###################################################################################################

lunchPrinter(NeunB,Men,Tec,flags,dev_flags)

#TODO should write three functions which generate the menue and then a printer function which is more simple 
