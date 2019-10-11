#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import os

# currentPath = os.getcwd()
currentPath = os.path.dirname(os.path.abspath('__file__'))
folderFiles = 'Dataset'
# pathFiles = os.path.join(currentPath,folderFiles)
weather = 'weather.csv'
uber2014 = 'uber_trips_2014.csv'
uber2015 = 'uber_trips_2015.csv'
greenTrips = 'green_trips.csv'
mtaTrips = 'mtaTrips.csv'
yellowTrips = 'yellow_trips.csv'

fileDatesAll = os.path.join(currentPath,folderFiles,'Fechas_en_Todos_DF.csv')
listFiles = [weather,uber2014,uber2015,greenTrips,mtaTrips,yellowTrips]


# In[36]:


def dateFunction(file):
    dfPandas = pd.read_csv(os.path.join(currentPath,folderFiles,file))
    if file == 'weather.csv':
        dfPandas['date'] = pd.to_datetime(dfPandas['date']).dt.strftime('%Y-%m-%d')
        dates = (dfPandas.date.unique()).tolist()
        return dates
    elif 'uber' in file:
        dfPandas['pickup_datetime'] = pd.to_datetime(dfPandas['pickup_datetime']).dt.strftime('%Y-%m-%d')
        dates = (dfPandas.pickup_datetime.unique()).tolist()
        return dates
    else:
        dfPandas['pickup_datetime'] = pd.to_datetime(dfPandas['pickup_datetime']).dt.strftime('%Y-%m-%d')
        dfPandas['dropoff_datetime'] = pd.to_datetime(dfPandas['dropoff_datetime']).dt.strftime('%Y-%m-%d')
        datesPU = (dfPandas.pickup_datetime.unique()).tolist()
        datesDO = (dfPandas.dropoff_datetime.unique()).tolist()
        for dateDO in datesDO:
            if dateDO in datesPU:
                datesPU.append(dateDO)
        # datesPU.sort()
        return datesPU


# In[ ]:


datesWeather = dateFunction(weather)
datesuber = dateFunction(uber2014)+ dateFunction(uber2015)
datesgreenTrips = dateFunction(greenTrips)
datesyellowTrips = dateFunction(yellowTrips)


# In[41]:


datesinAll = set(datesWeather) & set(datesuber) & set(datesgreenTrips) & set(datesyellowTrips)


# In[53]:


with open (fileDatesAll,'w') as f:
    for i in datesinAll:
        f.write('{}\n'.format(i))


# In[ ]:




