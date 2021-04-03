import pandas as pd

mdmDF = pd.read_csv('input/threema-mdm-export-2021-03-31.csv')
userListDF = pd.read_excel('input/output_Personalrat_20210331.xlsx')

for i in mdmDF.index[1:]:
    if userListDF['Username'].str.contains(mdmDF.license[i]).any():
        fname = userListDF.loc[userListDF['Username'] ==  mdmDF.license[i], 'Vorname'].values[0].strip()
        lname = userListDF.loc[userListDF['Username'] ==  mdmDF.license[i], 'Nachname'].values[0].strip()
        mdmDF.th_nickname[i] = fname + ' ' + lname
        mdmDF.th_firstname[i] = fname
        mdmDF.th_lastname[i] = lname

mdmDF.to_csv('output/mdmOutput.csv', index = False)