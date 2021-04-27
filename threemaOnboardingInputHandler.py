#  Copyright (c) 2021 by Marc Mueller-Stoffels (https://github.com/mmuellerstoffels/) is licensed under CC BY-SA 4.0.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/

# The following code as well as that in 'threemaOnboardingMDMHandler.py' is used to bulk import users into Threema.Work
# and then adding some clear text information to their individual entries in the Threema.Work MDM. Along the way data is
# check for inconsistencies and errors.

# STEP 1: from an Excel file that at least has the columns 'FirstName' and 'LastName' generate usernames, check for
# duplicates, make sure usernames are unique and add username-password pairs to the dataframe. Then load and check that
# usernames have not already been used for another user in the Threema.Work system. If so either skip creating the user
# (because he or she seems to exist already) or make sure the username is modified to be unique. Final new
# username-password pairs are added to a version of the inputted Excel file and a written separately to a CSV file. The
# Excel file is useful for further handling users, e.g., if you also have their email addresses in there you can bulk
# email them their credentials. The CSV file is used to copy-paste the username-password pairs into the bulk user
# generation of Threema.Work.

# STEP 2: see threemOnboardingMDMHandler.py

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from appliances import stringFlattener, passwordGenerator, duplicateWarningDialogShell, getUsernameListAsDf

# Fire up the main view and hide it.
root = Tk()
root.withdraw()

# Load the file with the users that will be imported. This is an Excel file with at least the columns 'Firstname' and
# 'LastName'.
inputFileName = askopenfilename(message='Select the XLSX file with new users.', filetypes=[("XLSX Files", "*.xlsx")])
inptDF = pd.read_excel(inputFileName)

# Retrieve the current MDM file for checking new usernames against as duplicates ares not allowed.
# mdmFileName = askopenfilename(message='Select the CSV file containing the MDM infos.', filetypes=[('CSV Files', '*.csv')])
# mdmDf = pd.read_csv(mdmFileName)
# TODO clean up the code from file to Api call for MDM data
mdmDf = getUsernameListAsDf()

# Some setup and cleaning of the input dataframe needs to happen.
# Some Excel files may have empty rows for structure. These are trouble later so we drop them here.
inptDF.dropna(how='all', inplace=True)

# Add columns to the input dataframe for the generated username and password
inptDF["Username"] = ""
inptDF["Password"] = ""

# handle duplicates in input file
inptDF.drop_duplicates(subset=['FirstName', 'LastName'], keep='first', inplace=True, ignore_index=True)

for i in inptDF.index:
    # remove diacritics from users first and last names and fix some other things not nice in user names.
    nameFlattened = stringFlattener(inptDF.LastName[i])
    try: #handle empty first names
        fnameInit = stringFlattener(inptDF.FirstName[i])[:2]
    except:
        fnameInit = 'n'
    userName = fnameInit + nameFlattened
    userName = userName.lower().replace("-","").replace("'","").strip().replace(" ","")

    # Check if userName already exists in list of new users
    # Need a flag if an entry was skipped so we do not add it back to the final product
    skipped = False
    if inptDF["Username"].str.contains(userName).any():
        # Retrieve the duplicate info from the inptDF
        idx = inptDF["Username"].str.contains(userName).idxmax()

        # we'll be asking for user input. This input has to be a valid choice. Hence the flag.
        validAction = False
        while not validAction:
            #
            action = duplicateWarningDialogShell('Import Data', userName,
                                                 inptDF.FirstName[idx], inptDF.LastName[idx],
                                                 inptDF.FirstName[i], inptDF.LastName[i])

            if action == 's':
                inptDF.drop([i], inplace=True)
                print("User creation skipped")
                validAction = True
                skipped = True

            elif action == 'm':
                appendInt = 1
                userNameMod = userName
                while inptDF['Username'].str.contains(userNameMod).any():
                    userNameMod = userName + str(appendInt)
                userName = userNameMod
                print('Username modified to ' + userNameMod)
                validAction = True
            else:
                print('########### WARNING #############')
                print('Invalid action. Please try again.')

    # add username and password once certain it will be unique and no duplicate
    if not skipped:
        inptDF.loc[i, 'Username'] = userName
        inptDF.loc[i, 'Password'] = passwordGenerator()
        skipped = False # reset flag


for i in inptDF.index:
    userName = inptDF.loc[i, 'Username']  # convenience variable
    # check if username exists already in current MDM
    for j in mdmDf.index[1:]:
        if userName == mdmDf.username[j]:
            validAction = False
            while not validAction:
                # TODO clean this up - need to call MDM info by username or id (needs adjusting getUsername...)
                action = duplicateWarningDialogShell('MDM', userName,
                                            mdmDf.th_firstname[j], mdmDf.th_lastname[j],
                                            inptDF.FirstName[i], inptDF.LastName[i])

                if action == 's':
                    inptDF.drop([i], inplace=True)
                    print("User creation skipped")
                    validAction = True
                    #No further action here
                elif action == 'm':
                    appendInt = 1
                    userNameMod = userName
                    while mdmDf['license'].str.contains(userNameMod).any():
                        userNameMod = userName + str(appendInt)
                    userName = userNameMod
                    inptDF.loc[i, 'Username'] = userNameMod
                    print('Username modified to ' + userNameMod)
                    validAction = True
                else:
                    print('########### WARNING #############')
                    print('Invalid action. Please try again.')

# Save entire dataframe as Excel for external processing, e.g., for bulk email of access data
writer = pd.ExcelWriter('output/output.xlsx')
inptDF.to_excel(writer)
writer.save()

# TODO change the following to using the Threema API to write new users straight to the management center. While at it, the
# individual MDM entries can be updated too. (AFTER PULLING A BACKUP!)

# Save username-password pairs for import to Threema.Work user creation
inptDF.to_csv('output/output.csv', columns=["Username", "Password"], index=False, header=False)







