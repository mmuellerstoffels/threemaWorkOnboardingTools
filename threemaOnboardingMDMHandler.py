#  Copyright (c) 2021 by Marc Mueller-Stoffels (https://github.com/mmuellerstoffels/) is licensed under CC BY-SA 4.0.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/

# STEP 2: Add users clear names to the MDM
# This file relies on you to have downloaded the MDM export CSV file AFTER adding a bunch of username-password
# pairs to the Threema.Work database. It the runs a comparison against the Excel (generated as output.xlsx in
# STEP 1) containing those usernames and the clear text names and adds the clear text to the individual fields for the
# Threema.Work MDM file.

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Get a view to launch and then hide
root = Tk()
root.withdraw()

# Select and load the MDM file that needs appending with clear text names for users
mdmFile = askopenfilename(message='Select the CSV file containing the MDM infos.', filetypes=[('CSV Files', '*.csv')])
mdmDF = pd.read_csv(mdmFile)

# Select and load the Excel with the needed information
userListFile = askopenfilename(message='Select the XLSX file with new users.', filetypes=[("XLSX Files", "*.xlsx")])
userListDF = pd.read_excel(userListFile)

# If usersnames are full match add the first, last and nickname info to the MDM dataframe
for i in mdmDF.index[1:]:
    if userListDF['Username'].str.fullmatch(mdmDF.license[i]).any():
        fname = userListDF.loc[userListDF['Username'] == mdmDF.license[i], 'FirstName'].values[0].strip()
        lname = userListDF.loc[userListDF['Username'] == mdmDF.license[i], 'LastName'].values[0].strip()
        mdmDF.th_nickname[i] = fname + ' ' + lname
        mdmDF.th_firstname[i] = fname
        mdmDF.th_lastname[i] = lname

# Save the fresh MDM file
mdmDF.to_csv('output/mdmOutput.csv', index = False)