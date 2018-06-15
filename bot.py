import requests as req
from src.utils.constants import PAGE_URL, SHAPEFILES_FOLDER
from src.utils.file_manager import extract_zip_to_folder, delete_and_create_folder, download_file, generate_file_name
from src.utils._snippets import check_if_new_shapefile
from src.db.configs import TERMINAL_COMMAND, TABLE_NAME
from subprocess import call
from src.db.model import DB_Model
from src.utils.ipam_slack_notifier import SlackBOT

def routine():

    try:
        delete_and_create_folder()
        
        download_file(PAGE_URL)
        extract_zip_to_folder()

        if check_if_new_shapefile():
            db = DB_Model()

            if db.check_if_table_exists():
                db.drop_table()

            call(TERMINAL_COMMAND.format(SHAPEFILES_FOLDER,
                                            generate_file_name(), TABLE_NAME), shell=True)
            
            db.database_calculate_and_drop_table()
            
            SlackBOT().send_msg('[+] Risco fogo shapefile atualizado :+1: '+generate_file_name(), '#risco_fogo')
        else:

            SlackBOT().send_msg('[+] Nenhum shapefile novo.','#risco_fogo')

    except:

        SlackBOT().send_msg('[-] Ocorreu algum erro. :-1:', '#risco_fogo')

routine()

