# threemaWorkOnboardingTools
Set of tools to batch onboard users to Threema.Work and updating the Threema.Work MDM entries for new users with their clear first/last name and 'firstname lastname' as their nickname. 

Workflow:
1) You need an Excel file with Columns for FirstName and LastName (at least) for people that are to be onboarded. Better to also get their email addresses in there if you can. 
2) You need to export the current global and individual values out of the Threema.Work MDM as a CSV file. KEEP A BACKUP COPY.
3) Run 'threemaWorkOnboardingInputHandler.py': this will create output.xlsx (for further processing) and output.csv. 
4) Use the username-password pairs in output.csv to bulk create new users in the Threema.Work Management-Cockpit.
5) Export the new Threema.Work MDM data as CSV.  KEEP A BACKUP COPY.
6) Run 'threemaWorkOnboardingMDMHandler.py': this will add the additional information (clear names) from output.xlsx to the MDM File. 
7) Import the new 'outputMDM.csv' as the new Threema.Work MDM data. CAUTION: this overrides all existing data in the Management-Cockpit.
8) Let your new users know the username-password combination to get going with Threema.Work. 

# License
CC BY-SA 4.0.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/
