#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import read_csv

raw_data = pd.read_csv('India_Menu.csv')
raw_data.head()


# In[2]:


columns = list(raw_data.columns)
columns[1] = 'Item'
raw_data.columns = columns


# In[3]:


columns


# In[4]:


nutrients = list(raw_data.columns)[2:]
nutrients = dict(zip(range(len(nutrients)), nutrients))
nutrients


# In[5]:


stub, sep = 'Quantity', '_'
raw_data.columns = list(raw_data.columns)[:2] + [stub + sep + str(k) for k in nutrients.keys()]
raw_data.head()


# In[6]:


df = pd.wide_to_long(raw_data, stubnames="Quantity", i=["Category", "Item"],  j="Nutrient", sep="_", suffix=r"\w+")
df.reset_index(inplace=True)

df['Nutrient'] = df['Nutrient'].apply(lambda x: nutrients[x])
df['Unit'] = df['Nutrient'].apply(lambda x: x.split('(')[-1][:-1])
df['Nutrient'] = df['Nutrient'].apply(lambda x: x.split(' (')[0])

df.head()


# In[7]:


menus = pd.DataFrame(data=df['Category'].unique(), columns=['category'])
menus.reset_index(inplace=True)
menus.columns = ['id', 'menu']

menus.head()


# In[8]:


menus.to_csv('categories.csv', index=False)


# In[9]:


meals = df[['Item', 'Category']].drop_duplicates()
meals.reset_index(drop=True, inplace=True)
meals.reset_index(inplace=True)
meals.columns = ['id', 'meal', 'menu']

mapping = dict(menus[['menu', 'id']].values)
meals['menu'] = meals['menu'].apply(lambda x: mapping[x])

meals.head()


# In[10]:


meals.to_csv('meals.csv', index=False)


# In[11]:


units = df[['Unit']].drop_duplicates()
units.reset_index(drop=True, inplace=True)
units.reset_index(inplace=True)
units.columns = ['id', 'unit']

units.to_csv('units.csv', index=False)
units.head()


# In[12]:


nutrients = df[['Nutrient', 'Unit']].drop_duplicates()
nutrients.reset_index(drop=True, inplace=True)
nutrients.reset_index(inplace=True)
nutrients.columns = ['id', 'nutrient', 'unit']

mapping = dict(units[['unit', 'id']].values)
nutrients['unit'] = nutrients['unit'].apply(lambda x: mapping[x])

nutrients.head()


# In[13]:


nutrients.to_csv('nutrients.csv', index=False)


# In[14]:


nutrition = df[['Item', 'Nutrient', 'Quantity']]
nutrition.columns = ['meal', 'nutrient', 'quantity']

mapping = dict(meals[['meal', 'id']].values)
nutrition['meal'] = nutrition['meal'].apply(lambda x: mapping[x])

mapping = dict(nutrients[['nutrient', 'id']].values)
nutrition['nutrient'] = nutrition['nutrient'].apply(lambda x: mapping[x])

nutrition.head(25)


# In[15]:


nutrition.to_csv('nutrition.csv',index = False)


# In[ ]:




