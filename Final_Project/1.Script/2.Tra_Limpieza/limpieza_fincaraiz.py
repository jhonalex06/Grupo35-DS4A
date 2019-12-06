import pandas as pd
import numpy
from datetime import datetime

print("Proceso de estandarizacion inmuebles de finca raiz")
print("- Cargando data set .....")
df_origen = pd.read_csv('../../2.Export/1.Ext/variables_inmuebles_finca_raiz.zip',low_memory=False,
                       dtype={'Latitude': str})
n_rows_ori,n_columns_ori =df_origen.shape
print("- Cantidad de registros data set original: ",n_rows_ori)

print("- Eliminar duplicados")
train_1 = df_origen.drop_duplicates().reset_index(drop=True)
train_2 = train_1[['url_link','ModifyDate']].groupby('url_link').max().reset_index()
train_3 = pd.merge(train_2,train_1,how='left',left_on = ['url_link','ModifyDate'],right_on=['url_link','ModifyDate'])
train_1,train_2 = pd.DataFrame(),pd.DataFrame()

train_4 = train_3[['Latitude','Longitude','Price','Description','ClientId','Neighborhood','url_link']].groupby(['Latitude','Longitude','Price','Description','ClientId','Neighborhood']).max().reset_index()
train_5 = train_3.drop(['url_link'],axis='columns').drop_duplicates().reset_index(drop=True)
train   = pd.merge(train_5,train_4,how='left')
train_4,train_5 = pd.DataFrame(),pd.DataFrame()

n_rows,n_columns =train.shape
n_row_drop = n_rows_ori - n_rows
print("- Cantidad de registros ahora: ",n_rows," # duplicados: ",n_row_drop)

print("Eliminacion de campos nulos ....")
data_count_null = train.isnull().sum().reset_index(name='q_nan')

# Variable identificadas como no utiles
columns_to_drop = ['ClientId','ClientName','TransactionId',
                   'TransactionType','Category1Id','Category2Id',
                  'Category3Id','Location1','Location2','OutStanding',
                  'TopAdvert','Status','Surface','LivingArea',
                  'Capacity','ModifyDate','ProductLabel']

#identifica los campos que tengan el 90% de sus 
for columns in data_count_null[data_count_null['q_nan']==(n_rows)]['index']:
    columns_to_drop.append(columns)

train = train.drop(columns_to_drop,axis='columns')

extras_sector = []
extras_exteriores = []
extras_interiores = []
extras_apartamento = []
extras = []
for a in train['Extras']:
    if a==a:
        for b in a.split('|'):
            extras.append(b.split('$')[0])
            if(b.split('$')[0]=='del Sector'):
                for c in b.split('$')[1].split(','):
                    extras_sector.append(c.strip())
            if(b.split('$')[0]=='Interiores'):
                for c in b.split('$')[1].split(','):
                    extras_interiores.append(c.strip())
            if(b.split('$')[0]=='Exteriores'):
                for c in b.split('$')[1].split(','):
                    extras_sector.append(c.strip())
            if(b.split('$')[0]=='#Apartamento#'):
                for c in b.split('$')[1].split(','):
                    extras_apartamento.append(c.strip())
extras_sector.sort()
extras_sector = list(set(extras_sector))
extras_exteriores.sort()
extras_exteriores = list(set(extras_exteriores))
extras_interiores.sort()
extras_interiores = list(set(extras_interiores))
extras.sort()
extras = list(set(extras))
extras_apartamento.sort()
extras_apartamento = list(set(extras_apartamento))

homologacion_columns = {'Category1':'tipo_inueble',
                        'Location3':'zona',
                        'Location4':'barrio1', 
                        'Neighborhood':'sector_catastral', 
                        'Description':'descripcion', 
                        'Price':'precio',
                        'ContractType':'tipo_contrato',
                        'Area':'area', 
                        'Address':'direccion', 
                        'Rooms':'numero_habitaciones', 
                        'Baths':'num_banos',
                        'Ages':'edad',
                        'Condition':'condicion', 
                        'Floor': 'piso_ubicacion', 
                        'AdministrationPrice':'precio_administracion',
                        'Stratum':'estrato',
                        'Garages':'num_garages',
                        'Extras':'extras', 
                        'Latitude':'latitude',
                        'Longitude':'longitude',
                        'InteriorFloors':'piso_interior',
                        'url_link':'id_inmueble'}

train = train.rename(columns = homologacion_columns)

train.to_csv('../../2.Export/2.Final/limpieza_finca_raiz.zip', compression='gzip')
print("Fin limpieza finca raiz")