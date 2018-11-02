try:
    from PIL import Image
except ImportError:
    import Image

import urllib.request
import pytesseract
import re
import datetime

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal

###################################################################################################

#tesseract location
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

##################################################################################################

urllib.request.urlretrieve("http://neunbe.at/pictures/44-111MENUE111--.jpg", "test.jpg")

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
urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/55?woy=45&year=2018","test2.pdf")

today = datetime.date.today()
thisweek = today.isocalendar()[1]
weekday = ("Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag")[today.weekday()]
#print(weekday)

###################################################################################################

document = open('test.pdf', 'rb')
#Create resource manager
rsrcmgr = PDFResourceManager()
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

textlist=[]
for page in PDFPage.get_pages(document):
	interpreter.process_page(page)
	layout = device.get_result()
	for element in layout:
		if isinstance(element, LTTextBoxHorizontal):
			#print(element.get_text())
			textlist.append(element.get_text())

#print(PDFPage.get_pages(document))
#print(layout)
#print(textlist)
