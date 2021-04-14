#  Copyright (c) 2021 by Marc Mueller-Stoffels (https://github.com/mmuellerstoffels/) is licensed under CC BY-SA 4.0.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/

import pandas as pd
from appliances import stringFlattener, passwordGenerator, fileChooser, duplicateWarningDialogShell, mainView

# Fire up the main view
root = mainView()

# Load the file with the users that will be imported. This is an Excel file with at least the columns 'Firstname' and
# 'LastName'.
inputFileName = fileChooser(root, 'Select the XLSX file with new users.', [("XLSX Files", "*.xlsx")])
inptDF = pd.read_excel(inputFileName)
inptDF.dropna(how='all', inplace=True)

# Add columns to the input dataframe for the generated username and password
inptDF["Username"] = ""
inptDF["Password"] = ""

# Retrieve the current MDM file for checking new usernames against as duplicates ares not allowed.
mdmFileName = fileChooser(root, 'Select the CSV file containing the MDM infos.', [('CSV Files', '*.csv')])
mdmDf = pd.read_csv(mdmFileName)

# TODO handle duplicates in input file
print(inptDF.shape)
inptDF.drop_duplicates(subset=['FirstName', 'LastName'], keep='first', inplace=True, ignore_index=True)
print(inptDF.shape)

for i in inptDF.index:
    nameFlattened = stringFlattener(inptDF.LastName[i])
    try: #handle empty first names
        fnameInit = stringFlattener(inptDF.FirstName[i])[:2]
    except:
        fnameInit = 'n'
    userName = fnameInit + nameFlattened
    userName = userName.lower().replace("-","").replace("'","").strip().replace(" ","")

    # TODO Check if userName already exists in list of new users
    skipped = False
    if inptDF["Username"].str.contains(userName).any():
        # TODO Retrieve the duplicate info from the inptDF
        idx = inptDF["Username"].str.contains(userName).idxmax()

        validAction = False
        while not validAction:
            action = duplicateWarningDialogShell('Import Data', userName,
                                                 inptDF.FirstName[idx], inptDF.LastName[idx],
                                                 inptDF.FirstName[i], inptDF.LastName[i])

            if action == 's':
                inptDF.drop([i], inplace=True)
                print("User creation skipped")
                validAction = True
                skipped = True
                # No further action here
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

    # add username and password
    print(i)
    if not skipped:
        inptDF.loc[i, 'Username'] = userName
        inptDF.loc[i, 'Password'] = passwordGenerator()
        skipped = False


for i in inptDF.index:
    userName = inptDF.loc[i, 'Username']
    # check if username exists already in current MDM
    for j in mdmDf.index[1:]:
        if userName == mdmDf.license[j]:
            validAction = False
            while not validAction:
                action = duplicateWarningDialogShell('MDM', userName,
                                            mdmDf.th_firstname[j], mdmDf.th_lastname[j],
                                            inptDF.FirstName[i], inptDF.LastName[i])
                print('i: ' + str(i) + ', j: ' + str(j))
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





print(inptDF)

writer = pd.ExcelWriter('../../output/output.xlsx')
inptDF.to_excel(writer)
writer.save()

inptDF = inptDF.drop_duplicates('Username')
inptDF.to_csv('../../output/output.csv', columns=["Username", "Password"], index=False, header=False)







