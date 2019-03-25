try:
    from PIL import Image#, ImageDraw
except ImportError:
    import Image#, ImageDraw		# Imagick image viewer and stuff, also needed for screenshots

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
if not datetime.date.today().weekday() < 5:	# for weekend we want next weeks menu
	weeknumber +=1  
weeknumber = str(weeknumber)  # for string concatenation later on
#set year:
year = str(datetime.date.today().year)

###################################################################################################
# stolen shit inserted here
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw

PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"

def text_image(text_path, font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'L'
    # parse the file into lines
    with open(text_path) as text_file:  # can throw FileNotFoundError
        lines = tuple(l.rstrip() for l in text_file.readlines())

    # choose a font (you can see more detail in my library on github)
    large_font = 80  # get better resolution with larger size
    font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = PIL.ImageOps.invert(image).getbbox()
    c_box = np.asarray(c_box) + np.array([-10,-10,10,10]) 
    image = image.crop(c_box)
    return image

#######################################################################################################
def lunchprinter(NeunBE, Mensa, Tech, Flags):
	
	mensa_names = ['_Menü Classic:_ \t', '_Vegetarisch:_ \t', '_Tagesteller:_ \t']
	tech_names = ['_Tagesteller:_ \t', '_Vegetarisch:_ \t', '_Pasta:_ \t\t']
	neunbe_names = ['_Tagesmenü:_ \t', '_Monatsburger:_ \t', '_Wochenburger:_ \t']
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
	weekday = (datetime.date.today()+datetime.timedelta(days=1)).weekday()	
	day = days[weekday]
		
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

	#image_d = text_image('today_out.txt')
	#image_d.save('today_out.png')
	#image_t = text_image('tomorrow_out.txt')
	#image_t.save('tomorrow_out.png')
	#image_w = text_image('week_out.txt')
	#image_w.save('week_out.png')
		
########## 9b - the people who can't name files in a coherent way ###############################
flags=[]

neunB_menu_file = "neunB_menu_week"+weeknumber+".jpg"

url_9b = 'http://neunbe.at/menue.html'
browser = RoboBrowser(history=True)
try:
	browser.open(url_9b)
	request = browser.session.get(url_9b, stream=True)
	corr_url = re.search("2019\" src=\"../pictures/((?s).*\">)", str(request.content))[0].split("<br>")[0].split("/")[2].split(".jpg\">")[0]
except TypeError:
	flags.append("9b Menue page down")
	neunB_menu_file = "neunB_menu_week8.jpg"    # use a template menu from week 8/2019 so the rest at least works
	flags.append("9b Menǘ nicht verfügbar, eingetragenes Menü vermutlich falsch")

try: 
	urllib.request.urlretrieve("http://neunbe.at/pictures/"+corr_url+".jpg", neunB_menu_file)	

# should specify on which exception except should act (for all excepts in the script)
except:
	neunB_menu_file = "neunB_menu_week8.jpg"    # use a template menu from week 8/2019 so the rest at least works
	flags.append("9b Menǘ nicht verfügbar, eingetragenes Menü vermutlich falsch")

img = Image.open(neunB_menu_file)
area = (570,320,1300,1300)
img = img.crop(area)
#img.show()

# language option needs installation of file in usr/share/tessseract/4.00/tessdata
# --psm 6 is page separation mode option of tesseract, 6 uses image es single block of text, 3 is automatic/default
# psm 3 is better when there are empty lines in the day column before the actual day e.g. \nMontag 
out = pytesseract.image_to_string(img, lang="deu", config='--psm 6')
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

#TODO do not print MBurger and WBurger 5 times?!

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
