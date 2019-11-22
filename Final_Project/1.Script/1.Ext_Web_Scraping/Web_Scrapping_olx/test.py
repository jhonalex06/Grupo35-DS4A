# Libraries needed for basic web-scraping
from IPython.core.display import HTML
from bs4 import BeautifulSoup
from IPython.display import IFrame
import urllib # package required to interact with live webpage
import requests
import pandas as pd
import ast# will use to store the data from the webpage
import csv
import time

site_url = 'https://bogotacity.olx.com.co/apartamentos-casas-venta-cat-367-p-3'
r = requests.get(site_url, 'html.parser')
soup = BeautifulSoup(r.content)

links = soup.find_all('a',{"data-qa":"list-item"})

path = []

for i in links:
    path.append(i.get('href').strip('//'))

path.sort()
path = list(set(path))

site_url = 'https://{}'.format(path[0])
r = requests.get(site_url, 'html.parser')
soup = BeautifulSoup(r.content)

print (soup)
print (soup.title)