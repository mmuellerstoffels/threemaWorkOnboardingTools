import pandas as pd
from appliances import stringFlattener, passwordGenerator


inptDF = pd.read_excel('/Users/marc/PycharmProjects/pythonProject/ThreemaOnboarding/input/Kopie von Threema Bedarfe mit E-Mail-Adressen_.xlsx')

inptDF["Username"] = ""
inptDF["Password"] = ""


for i in inptDF.index:
    nameFlattened = stringFlattener(inptDF.Nachname[i])
    try: #handle empty first names
        fnameInit = stringFlattener(inptDF.Vorname[i][:2])
    except:
        fnameInit = 'n'
    userName = fnameInit + nameFlattened
    userName = userName.lower()
    inptDF["Username"][i] = userName
    inptDF["Password"][i] = passwordGenerator()



writer = pd.ExcelWriter('../../output/output.xlsx')
inptDF.to_excel(writer)
writer.save()

inptDF = inptDF.drop_duplicates('Username')
inptDF.to_csv('../../output/output.csv', columns=["Username", "Password"], index=False, header=False)







