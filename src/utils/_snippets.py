import datetime
import re
import os
from constants import SHAPEFILES_FOLDER
from file_manager import generate_file_name


def check_if_new_shapefile():


    file_name = generate_file_name()
    
    file_date_string = re.search('(\d{3,})', file_name).group(1)

    year = int(file_date_string[:4])
    month = int(file_date_string[4:6])
    day = int(file_date_string[6:])

    dt = datetime.date(year, month, day)

    if dt == datetime.datetime.today().date():

        return True
    else:

        return False
