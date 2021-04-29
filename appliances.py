#  Copyright (c) 2021 by Marc Mueller-Stoffels (https://github.com/mmuellerstoffels/) is licensed under CC BY-SA 4.0.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/

import string
import random
import requests
import json
import pandas as pd
import threemaWorkManagementAPI
from dotenv import load_dotenv
import os
load_dotenv()

apiHandle = threemaWorkManagementAPI.ThreemaWorkManagementAPI(apiKey=os.environ.get('Threema_MngmtCockpit_Api_Key'))

def stringFlattener(inpString):
    """
    Replaces diacritics with internationally acceptable substitutes. Expects input strings with diacritics in
    ISO-8859-1.
    :param inpString: original string
    :return translation: string without diacritics
    """

    #Define the character dictionary
    charMap = {
                'À':'A', 'Á':'A', 'Â':'A', 'Ã':'A', 'Ä':'Ae', 'Å':'A', 'Æ':'Ae',
                'Ç':'C',
                'È':'E', 'É':'E', 'Ê': 'E', 'Ë': 'E',
                'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
                'Ð': 'Dh', 'Þ': 'Th',
                'Ñ': 'N',
                'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'Oe', 'Ø': 'Oe',
                'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'Ue',
                'Ý': 'Y',
                'ß': 'ss',
                'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'ae', 'å': 'a', 'æ': 'ae',
                'ç': 'c',
                'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
                'ð': 'dh', 'þ': 'th',
                'ñ': 'n',
                'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'oe', 'ø': 'oe',
                'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'ue',
                'ý': 'y', 'ÿ': 'y'}

    # Create a translation table
    translateTable = inpString.maketrans(charMap)
    # Convert the string and return
    translation = inpString.translate(translateTable)
    return translation




def passwordGenerator(length=10):
    """
    Generates a random password having the specified length
    Source: https://dev.to/spaceofmiah/generating-random-password-in-python-practical-guide-amd
    :param length: length of password to be generated. Defaults to 10 if nothing is specified.
    :returns randomPassword: Random string of characters of specified length
    """

    LETTERS = string.ascii_letters
    NUMBERS = string.digits

    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}'

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    randomPassword = random.choices(printable, k=length)
    randomPassword = ''.join(randomPassword)
    return randomPassword

def duplicateWarningDialogShell(duplicateLocation,
                           duplicateUserName,
                           existingFirstName,
                           existingLastName,
                           importFirstName,
                           importLastName):
    '''
    Creates a shell dialog to handle duplicate entries.

    :param duplicateLocation:
    :param duplicateUserName:
    :param existingFirstName:
    :param existingLastName:
    :param importFirstName:
    :param importLastName:
    :return:
    '''



    print("***********************************************")
    print("Username already exists in " + duplicateLocation)
    print("Username: " + duplicateUserName)
    print("Existing Name: " + existingFirstName + ' ' + existingLastName)
    print("Import Name: " + importFirstName + ' ' + importLastName)
    action = input("Options: Skip creation (s), Modify new (m)")

    return action

def getUsernameListAsDf():
    r = apiHandle.getListCredentials(pageSize='0')
    rson = json.loads(r.text)
    df = pd.json_normalize(rson['credentials'])
    return df['username']