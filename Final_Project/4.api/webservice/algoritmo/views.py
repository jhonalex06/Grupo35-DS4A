import math
import re
import string
import numpy as np

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from statsmodels.regression.linear_model import OLSResults

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def clean_special_chars(line):
    filter_chars = string.punctuation.replace("|", '').replace('@', '').replace('#', '') + '¿' + '¡'
    chars = re.escape(filter_chars)
    return re.sub(r'[' + chars + ']', '', line)

def clean_url(line):
    new_line = line.replace("|", "|;;").split('|')
    complement = new_line[1] if len(new_line) > 1 else ''
    return re.sub(r'http\S+', '', new_line[0]) + complement.replace(";;", "|")


def cleanTweet(text):
    texto = clean_special_chars(clean_url(text))
    return texto

def response_options():
    response = HttpResponse(status=200)
    response['Allow'] = 'OPTIONS, GET, POST'
    response['Access-Control-Request-Method'] = 'OPTIONS, GET, POST'
    response['Access-Control-Request-Headers'] = 'Content-Type'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def response_cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def datos_compuesto_list(request):
    """
    """
    if request.method == 'GET':
        return response_cors(HttpResponse(status=501))

    elif request.method == 'POST':
        datos = JSONParser().parse(request)
        model_log = OLSResults.load("algoritmo/longley_results.pickle")
        response = [{           
           'Predicción':np.exp(model_log.predict(datos)) 
        }]
        return response_cors(JSONResponse(response, status=200))

    elif request.method == 'OPTIONS':
        return response_cors(response_options())


