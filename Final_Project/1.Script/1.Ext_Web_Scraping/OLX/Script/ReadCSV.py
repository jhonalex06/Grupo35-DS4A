import os
import pandas as pd
import sys
import re

rutaRelativa = os.path.dirname(os.path.realpath(__file__))
os.chdir(rutaRelativa)
rutaCSV = 'CSV_OLX'

def saveCSV(df):
    df.to_csv('OLX_Data.csv',sep=';',index=False)

def link2id(str):
    return str.rsplit("iid-")[1]

def word(sentence):
    post = re.findall(r'\b(?:APARTAMENTO|CASA|APTO)\b', sentence)
    post = str(post).replace('APTO', 'APARTAMENTO')
    post = str(post).replace('APTO', 'APARTAMENTO')
    post = re.sub(r"[^\w]", '', post)
    return post
    
df_OLX = pd.read_csv('CSV_OLX/OLX_Data_2019-11-13 12_43_03_165780.csv')

df_OLX = df_OLX.rename(columns={'price':'precio','surface':'area','streetaddress':'direccion','bedrooms':'num_habitaciones','bathrooms':'num_banos','antiquity':'edad','stratus':'estrato','parking':'num_garages', 'sellerType':'tipo_contrato'})

df_OLX['id'] = df_OLX.site_url.apply(link2id)
df_OLX = df_OLX.drop_duplicates(['id'], keep='last')
df_OLX = df_OLX.drop(['Unnamed: 0'], axis=1)
print(df_OLX.columns)

df_OLX['tipo_inmueble_1'] = df_OLX.site_url.apply(lambda row: word(str(row).upper()))
df_OLX['tipo_inmueble_2'] = df_OLX.title.apply(lambda row: word(str(row).upper()))
df_OLX['tipo_inmueble_3'] = df_OLX.description.apply(lambda row: word(str(row).upper()))
df_OLX['latitude'] = df_OLX.coordinates.apply(lambda row: row.split(',')[0])
df_OLX['longitude'] = df_OLX.coordinates.apply(lambda row: row.split(',')[1])

saveCSV(df_OLX)