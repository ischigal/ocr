from urllib.request import urlretrieve  # for reading URLs
from urllib.error import URLError
from PIL import Image
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

import pytesseract                      # apt install tesseract 4.0 (not trivial for Ubuntu < 18.04), also apt install libtesseract-dev and pytesseract via pip
import re                               # regular expressions tool for python
import datetime as dt                   # for current week number and week day
import tabula                           # to read pdfs, important to pip install tabula-py and not tabula
import numpy as np                      # for array operations

from robobrowser import RoboBrowser     # for automatic browsing of 9b website

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'       # tesseract location (of executable/command!);


def string_format_neunbe(regex, searched_string):
    return re.sub(" +", " ", re.search(regex, searched_string).group(1).replace("\n", " ").replace(" , ", ", ").strip())


def string_format_Mensen(data_frame, index_one, index_two, index_three):
    return re.sub(
        r'\s+',
        ' ',
        re.sub(
            r'\([ABCDEFGHLMNOPR/\s]*\)',  # this strips allergy signs
            "",
            re.sub(
                r'\([ABCDEFGHLMNOPR,\s]*\)',  # this strips allergy signs as well
                "",
                re.sub(
                    r'(€ ?\d+\,\d{1,2})',  # this strips prices
                    "",
                    data_frame[index_one]['data'][index_two][index_three]['text'].replace(
                        "\r",
                        " "))))).strip()


def get_weekly_menue_pdf_mensa_tech(location_id, week):
    current_week = dt.date.today().isocalendar()[1]
    current_year = dt.date.today().year
    user_message = f"Sorry, menue for location ID {location_id} currently not available\n"
    dev_info_flag = ""
    file_mensen = f"mensa_menu_week_{current_week + week}_location_{location_id}.pdf"

    try:
        urlretrieve(f"http://menu.mensen.at//index/menu-pdf/locid/{location_id}?woy={current_week}&year={current_year}", file_mensen)
    except URLError:
        dev_info_flag = f"ID {location_id} PDF not found"
        return [user_message, dev_info_flag]

    data_frame = tabula.read_pdf(file_mensen, pages="all", lattice=True, guess=True, multiple_tables=True, output_format="json")

    if len(data_frame) < 1:
        dev_info_flag = f"ID {location_id} PDF has 0 pages"
        return_list = [user_message, dev_info_flag]
    else:
        output_mensen = np.ndarray((5, 3), dtype=object)
        for iteration in range(5):
            try:  # two page menue
                if iteration != 4:
                    for index in range(3):
                        output_mensen[iteration][index] = string_format_Mensen(data_frame, 0, iteration + 2, index + 1)
                else:
                    for index in range(3):
                        output_mensen[iteration][index] = string_format_Mensen(data_frame, 2, 1, index + 1)
                dev_info_flag = f"ID {location_id} two page PDF"
            except BaseException:  # single page
                for index in range(3):
                    output_mensen[iteration][index] = string_format_Mensen(data_frame, 0, iteration + 2, index + 1)
                    dev_info_flag = f"ID {location_id} single page PDF"
        return_list = [output_mensen, dev_info_flag]
    return return_list


def get_menue_mensen(location_id, day):

    if day < 5:
        menue_flag = get_weekly_menue_pdf_mensa_tech(location_id, 0)  # stupid to call function for whole week every single time
        return_list = [menue_flag[0][day], menue_flag[1]]
    else:
        menue_flag = get_weekly_menue_pdf_mensa_tech(location_id, 1)
        return_list = [menue_flag[0][0], menue_flag[1]]
    return return_list


def get_menue_neunbe(day):
    current_week = dt.date.today().isocalendar()[1]
    current_year = dt.date.today().year

    user_message = "Sorry, no menue for 9b available at the moment\n"
    if day < 5:
        file_neunbe = f"neunbe_menu_week{current_week}.jpg"
        url_neunbe = 'http://neunbe.at/index.html'
        browser = RoboBrowser(history=True)
        try:
            browser.open(url_neunbe)
            url_content = str(browser.session.get(url_neunbe, stream=True).content)
            corr_url = re.search(f"\" src=\"../pictures/{current_year}-KW-.*?\">", url_content).group(0).split(".jpg\">")[0].split(" src=\"../")[1]

        except URLError:
            dev_info_flag = "9b menue page down, current menu not available"
            return [user_message, dev_info_flag]

        try:
            urlretrieve(f"http://neunbe.at/{corr_url}.jpg", file_neunbe)
        except URLError:
            dev_info_flag = "9b menue not found (probably not uploaded yet)"
            return [user_message, dev_info_flag]

        image_neunbe = Image.open(file_neunbe)
        image_dimensions = image_neunbe.size

        if image_dimensions == (935, 1324):
            used_image_area = (100, 100, 850, 1300)
        else:
            used_image_area = (0, 0, image_dimensions[0], image_dimensions[1])    # or use everything and deal with it
        imgage_ocr_input = image_neunbe.crop(used_image_area)
        # img.show()

        try:
            ocr = pytesseract.image_to_string(imgage_ocr_input, lang="deu", config='--psm 3')
        except AttributeError:
            dev_info_flag = "ocr did not work, might need to change page separation mode"
            return [user_message, dev_info_flag]

        try:
            monday_lunch = string_format_neunbe(r'Montag((?s).*)Dienstag', ocr)
            tuesday_lunch = string_format_neunbe(r'Dienstag((?s).*)Mittwoch', ocr)
            wednesday_lunch = string_format_neunbe(r'Mittwoch((?s).*)Donnerstag', ocr)
            thursday_lunch = string_format_neunbe(r'Donnerstag((?s).*)Freitag', ocr)
            friday_lunch = string_format_neunbe(r'Freitag((?s).*)Wochenburger', ocr)
            dev_info_flag = "psm 3 was used"

        except AttributeError:
            monday_lunch = tuesday_lunch = wednesday_lunch = thursday_lunch = friday_lunch = "unhandeld error, go bug Sebi about it"
            dev_info_flag = "ocr worked but regex didn't, might need to change keys"
        try:
            weekly_burger = string_format_neunbe(r'Wochenburger:((?s).*)V alle', ocr)
        except AttributeError:
            try:
                weekly_burger = string_format_neunbe(r'Wochenburger:((?s).*)V Burger', ocr)

            except AttributeError:
                weekly_burger = "unhandeld error, go bug Sebi about it"

        try:
            weekly_veggie = string_format_neunbe(r'Wochenangebot:((?s).*)\s\u20AC', ocr)
        except AttributeError:
            try:
                weekly_veggie = string_format_neunbe(r'Wochenangebot:((?s).*)Unsere', ocr)
            except AttributeError:
                try:
                    weekly_veggie = string_format_neunbe(r'Wochenangebot:((?s).*)', ocr)
                except AttributeError:
                    weekly_veggie = "unhandeld error, go bug Sebi about it"

        output_neunbe = np.array([[monday_lunch, tuesday_lunch, wednesday_lunch, thursday_lunch, friday_lunch][day], weekly_burger, weekly_veggie])
        return [output_neunbe, dev_info_flag]

    else:
        dev_info_flag = "Hoch die Hände, Wochenende"
        return [user_message, dev_info_flag]


def day_printer(date):
    menue_neunbe = get_menue_neunbe(date)
    menue_mensa = get_menue_mensen(42, date)
    menue_tech = get_menue_mensen(55, date)
    return [menue_neunbe, menue_mensa, menue_tech]


def mini_loop(place, place_name, out_file):
    if len(place) == 3:
        for iter_name, iter_place in zip(place_name, place):
            out_file.write(iter_name + "\n  " + iter_place + "\n")
    else:
        out_file.write("\n_" + place + "_\n")


def write_loop(out_file, mensa, tech, neunbe, mensa_names, tech_names, neunbe_names):
    out_file.write("\n *Mensa:* \n")
    mini_loop(mensa, mensa_names, out_file)
    out_file.write("\n *TechCafe:* \n")
    mini_loop(tech, tech_names, out_file)
    out_file.write("\n *9b:* \n")
    mini_loop(neunbe, neunbe_names, out_file)


def out_file_writer(out_file, flag_file, date, menue):

    mensa_names = ['_Vegetarisch:_ \t', '_Menü Classic:_ \t', '_Tagesteller:_ \t']
    tech_names = ['_Tagesteller:_ \t', '_Vegetarisch:_ \t', '_Pasta:_ \t\t']
    neunbe_names = ['_Tagesmenü:_ \t', '_Wochenburger:_ \t', '_Vegetarisches Wochenangebot:_ \t']
    days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

    if date == "week":

        for i in range(0, 5):
            out_file.write("\n*" + days[i] + ":* \n")
            mensa = menue[i][1][0]
            tech = menue[i][2][0]
            neunbe = menue[i][0][0]
            write_loop(out_file, mensa, tech, neunbe, mensa_names, tech_names, neunbe_names)

        for j in range(0, 3):
            flag_file.write(menue[0][j][1] + "\n")  # should be the same flags for every day so only do once

    else:

        neunbe = menue[0][0]
        mensa = menue[1][0]
        tech = menue[2][0]

        for i in range(0, 3):
            flag_file.write(menue[i][1] + "\n")

        if date >= 5:
            out_file.write("*nächster Montag:* \n")
            write_loop(out_file, mensa, tech, neunbe, mensa_names, tech_names, neunbe_names)

        else:
            out_file.write("*" + days[date] + ":* \n")
            write_loop(out_file, mensa, tech, neunbe, mensa_names, tech_names, neunbe_names)


def lunch_printer():

    outfile_today = open("today_out.txt", "w")
    outfile_tomorrow = open("tomorrow_out.txt", "w")
    outfile_week = open("week_out.txt", "w")
    outfile_dev_flags_today = open("dev_flags_today_out.txt", "w")
    outfile_dev_flags_tomorrow = open("dev_flags_tomorrow_out.txt", "w")
    outfile_dev_flags_week = open("dev_flags_week_out.txt", "w")

    today = dt.date.today().weekday()

    menue_today = day_printer(today)
    menue_tomorrow = day_printer(today + 1)
    menue_week = []
    for day in range(0, 5):
        menue_week.append(day_printer(day))

    out_file_writer(outfile_today, outfile_dev_flags_today, today, menue_today)
    out_file_writer(outfile_tomorrow, outfile_dev_flags_tomorrow, today + 1, menue_tomorrow)
    out_file_writer(outfile_week, outfile_dev_flags_week, "week", menue_week)

    outfile_today.close()
    outfile_tomorrow.close()
    outfile_week.close()
    outfile_dev_flags_today.close()
    outfile_dev_flags_tomorrow.close()
    outfile_dev_flags_week.close()


lunch_printer()
