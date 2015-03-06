
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# In[5]:

full_data_path = '../../data/raw/UCB.csv'
data_path = '/Users/choldgraf/Google Drive/Projects/BIDS/Sourcing/data/UCB_cleaned.csv'
dept_path = '/Users/choldgraf/Google Drive/Projects/BIDS/Sourcing/data/BerkeleyPO_Department.csv'


# In[16]:

output_path = '../../data/cleaned/UCB_cleaned.csv'
merged_path = '../../data/cleaned/UCB_dept_merge.csv'


# In[7]:

full_data = pd.read_csv(full_data_path)


# In[8]:

# Subset of columns
keep_columns = ['PO ID',
                'PO #',
                'Creation Date',
                'Supplier Name',
                'Item Type',
                'Product Description',
                'Manufacturer',
                'Quantity',
                'Unit Price',
                'Department',
                'Buyer: First Name',
                'Buyer: Last Name',
                'PO Closed Date']
data = full_data[keep_columns]


# In[9]:

# Replace problematic characters in column names
def convert_strings_to_specials(s):
    s = s.replace(' ', '_')
    s = s.replace(':', '_')
    s = s.replace('#', 'num')
    s = s.lower()
    return s
data.columns = [convert_strings_to_specials(col) for col in data.columns]


# In[10]:

# Remove rows with some percentage null values
null_perc_cutoff = .5
ix_null = data.isnull().sum(1) < np.round(null_perc_cutoff * data.shape[1])
data = data.loc[ix_null]


# In[13]:

# Turn column values into correct dtype
convert_int = ['po_id', 'quantity']
convert_float = ['unit_price']
convert_date = ['po_closed_date', 'creation_date']

data[convert_int] = data[convert_int].astype(np.int64)
data[convert_float] = data[convert_float].replace(',', '', regex=True).astype(float)


# In[14]:

# Convert dates (this may take some time)
data[convert_date] = data[convert_date].apply(pd.to_datetime)


# In[17]:

data.to_csv(output_path, index=False)


# ## Merge with department

# In[18]:

# Department ID
dept = pd.read_csv(dept_path)
dept['Spend'] = dept['Spend'].replace(',', '', regex=True).astype(float)
dept = dept.sort('Spend', ascending=False)


# In[19]:

# Clean up the department data
dept['Spend'] = dept.Spend.replace(',', '', regex=True).astype(float)
rename_dict = {col: ''.join([c for c in col if c.isalnum()]) for col in dept.columns}
dept = dept.rename(columns=rename_dict)
dept = dept.dropna(axis=0, subset=['PONumber'])
dept = dept[dept.PONumber != 'Null']


# In[27]:

merged = pd.merge(data, dept, left_on='po_num', right_on='PONumber', how='inner')


# In[28]:

merged = merged.drop('PONumber', axis=1).rename(columns={'DepartmentName': 'department_name', 'Spend': 'spend'})


# In[30]:

merged.to_csv(merged_path, index=False)


# In[ ]:



