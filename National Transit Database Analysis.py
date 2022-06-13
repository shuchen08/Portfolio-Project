#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure

get_ipython().run_line_magic('matplotlib', 'inline')
## matplotlib.rcParams['figure.figsize'] = (12,8)


# ### Import necessary files

# In[2]:


df1 = pd.read_excel('2019 Revenue Vehicle Inventory.xlsx', index_col=None)


# In[69]:


df1 = pd.read_excel('2019 Revenue Vehicle Inventory.xlsx', index_col=None)
df2 = pd.read_excel('2019 Facility Inventory.xlsx', index_col=None)
df3 = pd.read_excel('2019 Transit Way Mileage.xlsx', index_col=None)
xls = pd.ExcelFile('Operating Expenses.xlsm')
df4 = pd.read_excel(xls, 'Operating Expenses by Function', index_col = None)


# In[146]:


df5 = pd.read_excel('2019 Transit Stations.xlsx', index_col=None)


# In[261]:


xls = pd.ExcelFile('Track and Roadway.xlsm')
df7 = pd.read_excel(xls, 'Track by Mode', index_col = None)


# In[10]:


pd.set_option("display.max_columns", None)


# ## How many stations do CTA and other transit agencies have?

# In[148]:


## Only need certain transit agencies
df_Stations=df5[df5['NTD ID'].isin([50066, 90154, 10003, 20008, 30019, 30030])]


# In[158]:


df_Stations.groupby(['Agency Name', 'Mode']).sum().sort_values(by = ['Agency Name', 'Total Stations'], ascending=False)


# In[285]:


stations = df_Stations[df_Stations['Mode'].isin(['MB', 'HR'])]

plt.figure(figsize = (16,16))
sns.barplot(data = stations, x='Agency Name', y='Total Stations', hue = 'Mode')
plt.title('Number of Stations (2019)', fontsize = 20)
plt.xlabel('Transit Agencies', fontsize = 16)
plt.ylabel('Total Stations', fontsize = 16)
plt.xticks(rotation= 'vertical')
plt.legend(title = 'Transit Mode', fontsize=15, title_fontsize = 15)
plt.tight_layout()


# HR(Heavy Rail). MB(Bus). The number of stations for rails outnumbered stations for buses for most transit agencies except LACMTA

# ## How many miles of track?

# In[264]:


df_track_miles=df7[df7['NTD ID'].isin([50066, 90154, 10003, 20008, 30019, 30030])]


# In[265]:


df_track_miles.groupby(['Agency', 'Mode']).sum()['Total Track Miles']


# In[280]:


sns.barplot(data=df_track_miles, x='Agency', y='Total Track Miles', hue='Mode')
plt.title('Track Miles by Transit Mode', fontsize=18)
plt.xticks(rotation= 'vertical')
plt.show()


# HR(Heavy Rail), LR(Light Rail), CR(Coummuter Rail), SR(Streetcar Rail). In terms of rails, NYCT has the most track miles in Heavy Rail while MBTA has the most track miles in Commuter Rail. CTA only uses Heavy Rail

# ## How many vehicles do each transit agencies have?

# In[4]:


df_Revenue_Vehicle_Inventory = df1[df1['NTD ID'].isin([50066, 90154, 10003, 20008, 30019, 30030])]


# In[182]:


df_Revenue_Vehicle_Inventory.head(5)


# In[214]:


cmap = plt.get_cmap("Paired")
colors = cmap(np.array([10,2,3,4,5,6,7,8,9,1]))
labels =df_Revenue_Vehicle_Inventory.groupby('Agency Name').sum().index

fig, ax = plt.subplots(figsize = (12,8))
wedges, texts, autotexts = ax.pie(
           x=df_Revenue_Vehicle_Inventory.groupby('Agency Name').sum()['Total Fleet Vehicles'],
           startangle = -30,
           autopct = '%1.1f%%',
           wedgeprops={'width':0.5,'edgecolor': 'white','linewidth': 2},
           colors=colors,
           pctdistance = 1.2
          )

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=1)
kw = dict(arrowprops=dict(arrowstyle="-", color = "0.2"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

plt.title('Percentage Vehicles Owned by Agencies', fontsize=16)
plt.tight_layout()


# NYCT owns the most vehicles whereas CTA falls in 4th place

# In[5]:


df_Revenue_Vehicle_Inventory.groupby(['Agency Name', 'Modes']).sum()['Total Fleet Vehicles']


# In[7]:


VehicleByMode=df_Revenue_Vehicle_Inventory[df_Revenue_Vehicle_Inventory['Modes'].isin(['HR/DO', 'MB/DO'])]

plt.figure(figsize = (16,16))
sns.barplot(data=VehicleByMode, x='Agency Name', y='Total Fleet Vehicles', hue='Modes')
plt.title('Number of Vehicles by Mode', fontsize = 20)
plt.xlabel('Transit Agencies', fontsize = 16)
plt.ylabel('Total Vehicles', fontsize = 16)
plt.xticks(rotation= 'vertical')
plt.legend(title = 'Transit Mode', fontsize=15, title_fontsize = 15)
plt.tight_layout()


# Let's breakdown to HR and MB. NYCT owns the most Heavy Rail while CTA owns the most buses

# ## How old are the tracks?

# In[8]:


df_Track_Age = pd.read_excel('Track Age.xlsx', index_col=None)
df_Track_Age.head(5)


# In[13]:


matplotlib.rcParams['figure.figsize'] = (12,8)
sns.lineplot(data=df_Track_Age, x = 'Years', y = 'Total Track Mileage', hue='Agency')
plt.title('Age of the Tracks')


# SEPTA has more old tracks while NYCT has more newer tracks.

# ## Who has the oldest station and who has the newest?

# In[14]:


df_Station_Age = pd.read_excel('Station Age.xlsx', index_col=None)


# In[15]:


df_Station_Age.head(5)


# In[16]:


matplotlib.rcParams['figure.figsize'] = (12,8)
sns.lineplot(data=df_Station_Age, x = 'Years', y = 'Total stations', hue='Agency')
plt.title('Age of the Stations')


# Most of NYCT stations are old. Same as MBTA. NYCT also has the most new stations compared to other agencies. 

# ## Who has the oldest vehicles and who has the newest vehicles?

# In[18]:


df_Vehicle_Age = pd.read_excel('Vehicles Age.xlsx', index_col=None)


# In[22]:


df_Vehicle_Age.sort_values('Agency').head()


# In[260]:


sns.boxplot(data=df_Vehicle_Age, x='Agency', y ='Average Age Of Fleet (In Years)')
plt.xticks(rotation= 'vertical')
plt.title('Ages of Vehicles')


# SEPTA has an average of older vehicles. NYCT has an average of new vehicles

# ## What are the maintenance costs for CTA and other transit agencies?

# In[80]:


df_Operating_Expenses = df4[df4['NTD ID'].isin([50066, 90154, 10003, 20008, 30019, 30030])]


# In[278]:


cost = df_Operating_Expenses[df_Operating_Expenses['Mode'].isin(['MB', 'HR'])]

plt.figure(figsize = (16,16))
sns.barplot(data = cost, x='Agency', y='Vehicle Maintenance', hue = 'Mode')
plt.title('Vehicle Maintenance Costs of Transit Agencies (2019)', fontsize = 20)
plt.xlabel('Transit Agencies', fontsize = 16)
plt.ylabel('Maintenance Cost ($)', fontsize = 16)
plt.xticks(rotation= 'vertical')
plt.legend(title = 'Transit Mode', fontsize=15, title_fontsize = 15)
plt.tight_layout()


# NYCT has the most maintenance cost for both heavy rail and bus. CTA's maintenance costs are relatively high compared to LACMTA, MBTA and SEPTA

# ## Who has the most Fare Revenues?

# In[313]:


xls = pd.ExcelFile('Metrics.xlsm')
df8 = pd.read_excel(xls, 'Metrics', index_col = None)


# In[342]:


df_metrics = df8[df8['NTD ID'].isin([50066, 90154, 10003, 20008, 30019, 30030])]


# In[343]:


df_metrics= df_metrics[df_metrics['Mode'].isin(['HR', 'MB'])]


# In[344]:


df_metrics


# In[367]:


sns.clustermap(df_metrics.groupby(['Agency','Mode']).sum()['Fare Revenues Earned'].unstack(level=-1), cmap='coolwarm')


# NYCT has the most fare revenue

# ## What do the transit agencies spend the money on?

# In[52]:


df_Capital_Expenses = pd.read_excel('Capital Expense.xlsx', index_col=None)


# In[71]:


df_Capital_Expenses.head(5)


# In[75]:


df_Capital_Expenses.groupby(['Agency','Type'])['Expense'].sum().unstack().plot(kind='bar', stacked=True, 
                                                                               color=['black', 'red', 'green', 'blue', 'cyan', 'grey','chartreuse', 'goldenrod', 'violet'])
plt.title('Capital Expenses', fontsize=18)
plt.ylabel('Total Expenses ($)')


# CTA has the least capital expenses compared to other transit agencies. NYCT has the most capital expenses, and spent mostly on stations and guideway. The agencies spent their money mostly on passenger vehicles and guideway except WMATA spent fairly on it.
