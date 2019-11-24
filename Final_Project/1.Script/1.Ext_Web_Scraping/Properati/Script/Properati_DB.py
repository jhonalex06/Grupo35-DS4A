from IPython.core.display import HTML
from bs4 import BeautifulSoup
from IPython.display import IFrame
import urllib # package required to interact with live webpage
import requests
import pandas as pd
import ast# will use to store the data from the webpage
import csv
import time
import json
import re
import sys
import time
import datetime
import os
# from shapely.geometry import point, polygon

n=0
rutaCarpeta = os.path.dirname(os.path.realpath(__file__))
os.chdir(rutaCarpeta)

df_p = pd.read_csv('Datos/co_properties.csv')

def saveCSV(df):
    df.to_csv('Properati_Data.csv',sep=',',index=False)

df_pBog = df_p[df_p['l3']=='Bogotá D.C']

df_pBog = df_pBog[df_pBog['operation_type']=='Venta']
df_pBog = df_pBog.rename(columns={'property_type':'tipo_inmueble','lat':'latitude','lon':'longitude','description':'descripcion','bedrooms':'num_habitaciones','bathrooms':'num_banos'})

# df_pBog= df_pBog.dropna(subset=['precio'], inplace=True)
df_pBog = df_pBog[(df_pBog['price']>0) & (df_pBog['tipo_inmueble'].isin(['Casa', 'Apartamento'])) ]

# print(df_pBog.columns)
# print(df_pBog.isna().sum())
df_pBog= df_pBog.dropna(how='all',subset=['surface_total','surface_covered'])
# print(df_pBog.shape)
df_pBog= df_pBog.dropna(how='all',subset=['latitude','longitude'])
# print(df_pBog.shape)

df_pBog['precio'] = df_pBog.apply(lambda row: row.price if row.currency == 'COP' else row.price*3271.05, axis=1)


df_pBog['num_habitaciones'] = df_pBog.apply(lambda row: row.rooms if row.num_habitaciones is None and row.rooms is not None else row.rooms, axis=1)
df_pBog['surface_covered'] = df_pBog.apply(lambda row: row.surface_total if pd.isnull(row.surface_covered) else row.surface_covered, axis=1)
df_pBog= df_pBog.dropna(how='all',subset=['num_habitaciones','num_banos'])
df_pBog= df_pBog.dropna(how='all',subset=['num_habitaciones'])
df_pBog= df_pBog.dropna(how='all',subset=['num_banos'])
# df_pBog['Ubicacion']= df_pBog["l4"] +" "+ df_pBog["l5"]+" "+ df_pBog["l6"]
df_pBog = df_pBog.drop(['ad_type','l1','l2','l3','operation_type','price_period','surface_total','rooms','currency','price','l4','l5','l6'], axis=1)
# print(df_pBog[['surface_total','surface_covered']][df_pBog.surface_covered.isnull()].head(10))
# print(df_pBog.head())
print(df_pBog.isna().sum())
# print(df_pBog.precio.head(5))

# sys.exit(0)
saveCSV(df_pBog)