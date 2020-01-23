# -*- coding: utf-8 -*-
try:
    from PIL import Image
except ImportError:
    import imagesize                    # Imagick image viewer and stuff, also needed for screenshots

import urllib.request                   # for reading URLs
import pytesseract                      # apt install tesseract 4.0 (not trivial for Ubuntu < 18.04), also apt install libtesseract-dev and pytesseract via pip
import re                               # regular expressions tool for python
import datetime                         # for current week number and week day
import tabula                           # to read pdfs, important to pip install tabula-py and not tabula
import numpy as np                      # for array operations
from robobrowser import RoboBrowser     # for automatic browsing of 9b website

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'       # tesseract location (of executable/command!);


def string_format_9b(string1, string2):
    return re.sub(" +", " ", re.search(string1, string2).group(1).replace("\n", " ").replace(" , ", ", ").strip())


def string_format_Mensen(DataFrame, IndexA, IndexB, IndexC):
    return re.sub('\s+', ' ', re.sub('\([ABCDEFGHLMNOPR/\s]*\)', "", re.sub('\([ABCDEFGHLMNOPR,\s]*\)', "", re.sub('(€ ?\d+\,\d{1,2})', "", DataFrame[IndexA]['data'][IndexB][IndexC]['text'].replace("\r", " "))))).strip()


def getMenue_Mensen_weekly(locid, week):
    currentWeek = datetime.date.today().isocalendar()[1]
    currentYear = datetime.date.today().year
    USER_MSG = "Sorry, menue for location ID "+str(locid)+" currently not available\n"
    file_Mensen = "mensa_menu_week_"+str(currentWeek+week)+"_location_"+str(locid)+".pdf"
    try:
        urllib.request.urlretrieve("http://menu.mensen.at//index/menu-pdf/locid/"+str(locid)+"?woy="+str(currentWeek+week)+"&year="+str(currentYear), file_Mensen)
    except:
        DEV_FLAG = "ID"+str(locid)+" PDF not found"
        return [USER_MSG, DEV_FLAG]
    df = tabula.read_pdf(file_Mensen, pages="all", lattice=True, guess=True, mulitple_tables=True, output_format="json")
    if len(df) < 1:
        DEV_FLAG = "ID"+str(locid)+" PDF has 0 pages"
        return [USER_MSG, DEV_FLAG]
    else:
        out_obj_Mensen = np.ndarray((5, 3), dtype=object)
        for iterator in range(0, 5):
            try:  # two page menue
                if iterator != 4:
                    for index in range(0, 3):
                        out_obj_Mensen[iterator][index] = string_format_Mensen(df, 0, iterator+2, index+1)
                else:
                    for index in range(0, 3):
                        out_obj_Mensen[iterator][index] = string_format_Mensen(df, 2, 1, index+1)
                DEV_FLAG = "ID"+str(locid)+" two page PDF"
            except:  # single page
                for index in range(0, 3):
                    out_obj_Mensen[iterator][index] = string_format_Mensen(df, 0, iterator+2, index+1)
                    DEV_FLAG = "ID"+str(locid)+" single page PDF"
        return [out_obj_Mensen, DEV_FLAG]


def getMenue_Mensen(locid, day):

    if day < 5:
        menue_flag = getMenue_Mensen_weekly(locid, 0)  # stupid to call function for whole week every single time
        return [menue_flag[0][day], menue_flag[1]]
    else:
        menue_flag = getMenue_Mensen_weekly(locid, 1)
        return [menue_flag[0][0], menue_flag[1]]  # show next monday


def getMenue_9b(day):
    currentWeek = datetime.date.today().isocalendar()[1]
    currentYear = datetime.date.today().year
    USR_MSG = "Sorry, no menue for 9b available at the moment\n"
    if day < 5:
        file_9b = "neunB_menu_week"+str(currentWeek)+".jpg"
        url_9b = 'http://neunbe.at/menue.html'
        browser = RoboBrowser(history=True)
        try:
            browser.open(url_9b)
            url_content = str(browser.session.get(url_9b, stream=True).content)
            corr_url = re.search("\" src=\"../pictures/mdw-.*?\">", url_content).group(0).split(".jpg\">")[0].split(" src=\"../")[1]
        except:  # TypeError or AttributeError:
            DEV_FLAG = "9b menue page down, current menu not available"
            return [USR_MSG, DEV_FLAG]

        try:
            urllib.request.urlretrieve("http://neunbe.at/"+corr_url+".jpg", file_9b)
        except:
            DEV_FLAG = "9b menue not found (probably not uploaded yet)"
            return [USR_MSG, DEV_FLAG]

        img = Image.open(file_9b)
        dims = img.size
        if dims == (1417, 1415):
            area = (600, 300, 1500, 1300)
        elif dims == (3000, 3000):
            area = (1200, 600, 2700, 2700)
        elif dims == (935, 934):
            area = (275, 118, 825, 800)
        else:
            area = (580, 310, 1300, 1300)  # TODO automatically find this area

        img = img.crop(area)
        #img.show()

        try:
            try:
                ocr = pytesseract.image_to_string(img, lang="deu", config='--psm 6')
                Mo = string_format_9b('Montag((?s).*)Dienstag', ocr)
                Di = string_format_9b('Dienstag((?s).*)Mittwoch', ocr)
                Mi = string_format_9b('Mittwoch((?s).*)Donnerstag', ocr)
                Do = string_format_9b('Donnerstag((?s).*)Freitag', ocr)
                Fr = string_format_9b('Freitag((?s).*)Monatsburger', ocr)
                DEV_FLAG = "psm 6 was used"
            except AttributeError:
                ocr = pytesseract.image_to_string(img, lang="deu", config='--psm 3')
                Mo = string_format_9b('Montag((?s).*)Dienstag', ocr)
                Di = string_format_9b('Dienstag((?s).*)Mittwoch', ocr)
                Mi = string_format_9b('Mittwoch((?s).*)Donnerstag', ocr)
                Do = string_format_9b('Donnerstag((?s).*)Freitag', ocr)
                Fr = string_format_9b('Freitag((?s).*)Monatsburger', ocr)
                DEV_FLAG = "psm 3 was used"
        except AttributeError:
            DEV_FLAG = "9b menue is template only"
            return [USR_MSG, DEV_FLAG]
        MBurger = string_format_9b('Monatsburger:((?s).*)\s\u20AC((?s).*)Wochenburger', ocr)

        try:
            WBurger = string_format_9b('Wochenburger:((?s).*)\s\u20AC((?s).*)V', ocr)
        except AttributeError:
            try:
                WBurger = string_format_9b('Wochenburger:((?s).*)Valle', ocr)
            except AttributeError:
                WBurger = string_format_9b('Wochenburger:((?s).*)V alle', ocr)
        try:
            WVeg = string_format_9b('Wochenangebot:((?s).*)\s\u20AC', ocr)
        except AttributeError:
            try:
                WVeg = string_format_9b('Wochenangebot:((?s).*)Unsere', ocr)
            except:
                WVeg = "unhandeld error, go bug Sebi about it"

        out_obj_9b = np.array([[Mo, Di, Mi, Do, Fr][day], MBurger, WBurger, WVeg])
        return [out_obj_9b, DEV_FLAG]

    else:
        DEV_FLAG = "Hoch die Hände, Wochenende"
        return [USR_MSG, DEV_FLAG]


def dayPrinter(date):
    menue9b = getMenue_9b(date)
    menueMensa = getMenue_Mensen(42, date)
    menueTech = getMenue_Mensen(55, date)
    return [menue9b, menueMensa, menueTech]


def miniLoop(place, place_name, outFile):
    if len(place) == 3:
        for i in range(0, len(place)):
            outFile.write(place_name[i]+"\n  "+place[i]+"\n")
    elif len(place) == 4:
        for i in range(0, len(place)):
            outFile.write(place_name[i]+"\n  "+place[i]+"\n")
    else:
        outFile.write("\n_"+place+"_\n")


def writeLoop(outFile, mensa, tech, neunb, mensa_names, tech_names, neunb_names):
    outFile.write("\n *Mensa:* \n")
    miniLoop(mensa, mensa_names, outFile)
    outFile.write("\n *TechCafe:* \n")
    miniLoop(tech, tech_names, outFile)
    outFile.write("\n *9b:* \n")
    miniLoop(neunb, neunb_names, outFile)


def outFileWriter(outFile, flagFile, date, menue):

    mensa_names = ['_Vegetarisch:_ \t', '_Menü Classic:_ \t', '_Tagesteller:_ \t']
    tech_names = ['_Tagesteller:_ \t', '_Vegetarisch:_ \t', '_Pasta:_ \t\t']
    neunb_names = ['_Tagesmenü:_ \t', '_Monatsburger:_ \t', '_Wochenburger:_ \t', '_Vegetarisches Wochenangebot:_ \t']
    days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

    if date == "week":

        for i in range(0, 5):
            outFile.write("\n*"+days[i]+":* \n")
            mensa = menue[i][1][0]
            tech = menue[i][2][0]
            neunb = menue[i][0][0]
            writeLoop(outFile, mensa, tech, neunb, mensa_names, tech_names, neunb_names)

        for j in range(0, 3):
            flagFile.write(menue[0][j][1]+"\n")  # should be the same flags for every day so only do once

    else:
        mensa = menue[1][0]
        tech = menue[2][0]
        neunb = menue[0][0]

        for i in range(0, 3):
            flagFile.write(menue[i][1]+"\n")

        if date >= 5:
            outFile.write("*nächster Montag:* \n")
            writeLoop(outFile, mensa, tech, neunb, mensa_names, tech_names, neunb_names)

        else:
            outFile.write("*"+days[date]+":* \n")
            writeLoop(outFile, mensa, tech, neunb, mensa_names, tech_names, neunb_names)


def lunchPrinter():

    outfile_today = open("today_out.txt", "w")
    outfile_tomorrow = open("tomorrow_out.txt", "w")
    outfile_week = open("week_out.txt", "w")
    outfile_dev_flags_today = open("dev_flags_today_out.txt", "w")
    outfile_dev_flags_tomorrow = open("dev_flags_tomorrow_out.txt", "w")
    outfile_dev_flags_week = open("dev_flags_week_out.txt", "w")

    today = datetime.date.today().weekday()

    menueToday = dayPrinter(today)
    menueTomorrow = dayPrinter(today+1)
    menueWeek = []
    for day in range(0, 5):
        menueWeek.append(dayPrinter(day))

    outFileWriter(outfile_today, outfile_dev_flags_today, today, menueToday)
    outFileWriter(outfile_tomorrow, outfile_dev_flags_tomorrow, today+1, menueTomorrow)
    outFileWriter(outfile_week, outfile_dev_flags_week, "week", menueWeek)

    outfile_today.close()
    outfile_tomorrow.close()
    outfile_week.close()
    outfile_dev_flags_today.close()
    outfile_dev_flags_tomorrow.close()
    outfile_dev_flags_week.close()


lunchPrinter()
