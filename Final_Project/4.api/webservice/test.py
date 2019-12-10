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
    garajes = 2
    countah = 0
    countcp = 0
    countms = 0

    param = {
    'estrato':[estrato], 
    'zona':[zona], 
    'log_area':[np.log(area)], 
    'num_banos':[banos], 
    'area':[area], 
    'num_garages':[garajes], 
    'Count_loc_AlojamientoHospedaje':[countah], 
    'Count_loc_CicloParqueadero':[countcp], 
    'Count_loc_Museos':[countms]}
    
    print (param)

    r = requests.post(url = URL2, json = param)
    print (r.json())

personal()

"""model_log = OLSResults.load("longley_results.pickle")

estrato = 4
zona = 'Chapinero'
area = 33.70
banos = 1
garajes = 2
countah = 0
countcp = 0
countms = 0


diccionario = {
    'estrato':[estrato], 
    'zona':[zona], 
    'log_area':[np.log(area)], 
    'num_banos':[banos], 
    'area':[area], 
    'num_garages':[garajes], 
    'Count_loc_AlojamientoHospedaje':[countah], 
    'Count_loc_CicloParqueadero':[countcp], 
    'Count_loc_Museos':[countms]}

arreglo = pd.DataFrame(diccionario)

print (model_log.predict(arreglo))
print (np.exp(model_log.predict(arreglo)))"""
