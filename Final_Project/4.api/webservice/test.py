import requests
from statsmodels.regression.linear_model import OLSResults

URL2 = 'http://127.0.0.1:8000/datos_compuestos/'

def personal():
    param = {'Comentarios': 'jhon'}
    r = requests.post(url = URL2, json = param)
    print (r.json())

#personal()

new_results = OLSResults.load("longley_results.pickle")