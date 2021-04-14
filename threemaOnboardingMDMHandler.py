import pandas as pd

mdmDF = pd.read_csv('input/threema-mdm-export-2021-04-14.csv')
userListDF = pd.read_excel('output/output.xlsx')

for i in mdmDF.index[1:]:
    if userListDF['Username'].str.fullmatch(mdmDF.license[i]).any():
        print(mdmDF.license[i])
        fname = userListDF.loc[userListDF['Username'] == mdmDF.license[i], 'FirstName'].values[0].strip()
        lname = userListDF.loc[userListDF['Username'] == mdmDF.license[i], 'LastName'].values[0].strip()
        mdmDF.th_nickname[i] = fname + ' ' + lname
        mdmDF.th_firstname[i] = fname
        mdmDF.th_lastname[i] = lname

print(mdmDF)
mdmDF.to_csv('output/mdmOutput.csv', index = False)