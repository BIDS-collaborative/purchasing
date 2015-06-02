import pandas as pd
import numpy as np



"""
Data cleaning
The original dataset does not contain the proper department names, so
need to get the organizational numbers and names from the departmentV3 dataset,
create a dictionary from
the data and use it to assign department names to the original dataset with
the network connections
"""
data = pd.read_csv('/Users/dariushbozorgmehri/Documents/My Work/Berkeley Classes Spring 2015/BIDS/data/modified_data_4_15/departmentDataV3_ALL_DATA_CLEAN.csv', low_memory=False)


"""
Rename the columns
"""
data = data.rename(columns={'Org.Level.4': 'org_level_4', 'Org.Level.4.Number': 'org_level_4_number','Org.Level.5': 'org_level_5', 'Org.Level.5.Number': 'org_level_5_number'})


"""
create data frame with org level 4 data only
"""
data4Number = data[["org_level_4","org_level_4_number"]]
#drop duplicates from the dataset
data4Number = data4Number.drop_duplicates()
data4Number = data4Number[["org_level_4_number", "org_level_4"]]
#need to reindex after drop dup or cannot create a dictionary
data4Number.index = range(1,len(data4Number) + 1)


"""
do same as above for org leve 5 data
"""
data5Number = data[["org_level_5","org_level_5_number"]]
data5Number = data5Number.drop_duplicates()
data5Number = data5Number[["org_level_5_number", "org_level_5"]]
data5Number.index = range(1,len(data5Number) + 1)


"""
Create a dictionary for org elevel 4
"""
i=1
for i in range(1,len(data4Number)):
    #while i < 3:
    data4Dic.update({data4Number.org_level_4_number[i]:data4Number.org_level_4[i]}) 
    

"""
create dic for org level 5 data
"""
i=1
for i in range(1,len(data5Number)):
    #while i < 3:
    data5Dic.update({data5Number.org_level_5_number[i]:data5Number.org_level_5[i]})


"""
Create dataframe from cleaned dataset (dataset cleaned by Chris Holdgraf
"""
dataOrig = pd.read_csv('/Users/dariushbozorgmehri/Documents/My Work/Berkeley Classes Spring 2015/BIDS/data/UCB_dept_merge.csv', low_memory=False)


"""
The original department name contains the 5 digit code of the department
and unspecific (general) department name. Split the orginal departname into
department number and the unspecified dept name
"""
dataOrig['department_number'] = dataOrig["department_name"].apply(lambda x: x[:5])
dataOrig['department_name_stripped'] = dataOrig["department_name"].apply(lambda x: x[6:])


"""
Use the dicitonaries to create a new department name in the dataOrig
dataframe using the more accurate data
from the above created dicitonaries, all of the most accurate department names
are in the department_name_update variable
"""
i=0
for i in range(1,len(dataOrig)):
    if  dataOrig.department_number[i] in data4Dic:
        #print "in there"
        dataOrig.department_name_update[i] = data4Dic[dataOrig.department_number[i]]
    elif dataOrig.department_number[i] in data5Dic:
        dataOrig.department_name_update[i] = data5Dic[dataOrig.department_number[i]]
    else:
        dataOrig.department_name_update[i] = dataOrig.department_name_stripped[i]



