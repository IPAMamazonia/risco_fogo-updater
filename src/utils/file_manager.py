import os
import zipfile
import shutil
import re
import tarfile
import requests
from constants import SHAPEFILES_FOLDER, TGZ_FILE_LOCATION

def remove_folder_and_shapeFiles():

    shutil.rmtree(SHAPEFILES_FOLDER)


def delete_and_create_folder():

    if os.path.exists(SHAPEFILES_FOLDER):
        remove_folder_and_shapeFiles()
    os.makedirs(SHAPEFILES_FOLDER)
        
def extract_zip_to_folder():
    
    tar = tarfile.open(mode="r:gz", fileobj=file(TGZ_FILE_LOCATION))
    tar.extractall(SHAPEFILES_FOLDER)  
    tar.close()


def download_file(url):
   
    r = requests.get(url, stream=True)

    print 'Downloading file...'
    with open(TGZ_FILE_LOCATION, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: 
                f.write(chunk)
     


def generate_file_name():
    regexp = re.compile(r'prev2d_(.*?)\.shp')
    for file_names in os.listdir(SHAPEFILES_FOLDER):
        if regexp.search(file_names):
            return file_names
