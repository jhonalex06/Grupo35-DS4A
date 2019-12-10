import requests
import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLSResults


URL2 = 'http://127.0.0.1:8000/datos_compuestos/'

def personal():

    estrato = 4
    zona = 'Chapinero'
    area = 33.70
    banos = 1
    hab = 2
    garajes = 2
    countah = 0
    countcp = 0
    countms = 0
    piso_int = 1
    lat = 4.64470852
    long = -74.06352119
    tip_inmu = 'Apartamento'
    sc = 'chapinero central'
    loc = 'chapinero'

    param = {
    'estrato':[estrato], 
    'zona':[zona], 
    'log_area':[np.log(area)], 
    'num_banos':[banos],
    'numero_habitaciones':[hab], 
    'num_garages':[garajes], 
    'Count_loc_AlojamientoHospedaje':[countah], 
    'Count_loc_CicloParqueadero':[countcp], 
    'Count_loc_Museos':[countms],
    'piso_interior':[piso_int],
    'latitude':[lat],
    'longitude':[long],
    'tipo_inmueble':[tip_inmu],
    'sector_catastral':[sc],
    'Locnombre':[loc]}
    
    print (param)

    r = requests.post(url = URL2, json = param)
    print (r.json())

personal()
"""
model_log = OLSResults.load("algoritmo/modelo5.pickle")

estrato = 4
zona = 'Chapinero'
area = 33.70
banos = 1
hab = 2
garajes = 2
countah = 0
countcp = 0
countms = 0
piso_int = 1
lat = 4.64470852
long = -74.06352119
tip_inmu = 'Apartamento'
sc = 'chapinero central'
loc = 'chapinero'

param = {
'estrato':[estrato], 
'zona':[zona], 
'log_area':[np.log(area)], 
'num_banos':[banos],
'numero_habitaciones':[hab], 
'num_garages':[garajes], 
'Count_loc_AlojamientoHospedaje':[countah], 
'Count_loc_CicloParqueadero':[countcp], 
'Count_loc_Museos':[countms],
'piso_interior':[piso_int],
'latitude':[lat],
'longitude':[long],
'tipo_inmueble':[tip_inmu],
'sector_catastral':[sc],
'Locnombre':[loc]}

arreglo = pd.DataFrame(param)

print (model_log.predict(arreglo))
print (np.exp(model_log.predict(arreglo)))"""
