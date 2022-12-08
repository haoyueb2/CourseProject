"""
This module is used to help execute db command.
"""

import os
import pathlib

from dotenv import load_dotenv


def get_username_and_password():
    """
    get the dotenv username and password
    :return: username, password
    """
    load_dotenv(pathlib.Path('/Users/wuyuqun/Desktop/cs242/') /
                'fa21-cs242-assignment2/goodreads' / 'goodreads' / '.env')

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    return username, password


def load_file_to_db(fname):
    """
    This function insert the json files into mongodb database.
    It would take the filename, and call mongodb's function to insert.
    :param fname: json files
    """
    with open(fname, 'r') as file:
        contents = file.read()
        if 'ISBN' in contents:
            col = 'book'
        elif 'author_id' in contents:
            col = 'author'
        else:
            file.close()
            raise RuntimeError('file is not book or author!')

    username, password = get_username_and_password()
    db_command = 'mongoimport --db admin --collection ' + col + \
                 ' --file ' + fname + ' --jsonArray' + \
                 ' --authenticationDatabase admin' + \
                 ' -u ' + username + ' -p ' + password
    os.system(db_command)


def extract_db_to_json():
    """
    This function would extract data in db as book.json
    and author.json json by calling functions of mongodb
    """
    username, password = get_username_and_password()
    cmd1 = 'mongoexport -c book -d admin -o book.json --pretty --jsonArray ' \
           + ' --authenticationDatabase admin' + ' -u ' + username + ' -p ' + password
    os.system(cmd1)

    cmd2 = 'mongoexport -c author -d admin -o author.json --pretty --jsonArray' \
           + ' --authenticationDatabase admin' + ' -u ' + username + ' -p ' + password
    os.system(cmd2)
