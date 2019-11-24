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

n=0

rutaCarpeta = os.path.dirname(os.path.realpath(__file__))
os.chdir(rutaCarpeta)

def createFolder(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def AjusteHora():
    time_run = datetime.datetime.now()
    time_run = str(time_run).replace(':','_')
    time_run = str(time_run).replace('.','_')
    return time_run

def saveCSV(df):
    df.to_csv(r'{}/OLX_Data_{}.csv'.format(folderCSV,AjusteHora()))

# folderJSON = 'json_Ofertas'
folderLog = 'logDescargas'
folderCSV = 'CSV_OLX'
# createFolder(folderJSON)
createFolder(folderLog)
createFolder(folderCSV)
tipoReporte = 'Log Web Scraping OLX'
fechaHora = AjusteHora()
archivoReporte = f'{folderLog}/{tipoReporte}_{fechaHora}'

site_sales = 'https://www.olx.com.co/bogota_g2007000/apartamentos-casas-venta_c367'
site_arriendos = 'https://www.olx.com.co/bogota_g2007000/apartamentos-casas-arriendo_c363'
r = requests.get(site_sales, 'html.parser')
soup = BeautifulSoup(r.content, 'html.parser')
with open(f"pPaginaPrincipal_{fechaHora}.html", "w") as file:
    file.write(str(soup))
numPaginas = soup.find_all('img',{"class":"tracking"})
print (numPaginas)
# print(numPaginas)
numPaginas = str(numPaginas[1]).split(';')
pattern = r'[\D]'
for text in numPaginas:
    if 'pageCount=' in text:
        numWebPages = int(re.sub(pattern, " ", text))
    elif 'resultCount' in text:
        numOffers = int(re.sub(pattern, " ", text))
print(f'Number of Offers: {numOffers}')
print(f'Number of Web Pages: {numWebPages}')

f = open(f"{archivoReporte}.txt", "w")
f.write(f"Inicio web scraping OLX: {datetime.datetime.now()}\n")
f.write(f"Nro. Ofertas publicadas: {numOffers}\n")
f.close()
sys.exit(0)

listWebPages = []
listWebPages.append(site_sales)
num=2
while num<=numWebPages:
    webPage = f'{site_sales}-p-{num}'
    listWebPages.append(webPage)
    num+=1

print(f'Número de Páginas a recorrer {len(listWebPages)}')
columns = ['id','offer_url','title','category','surface','streetaddress','stratus','sellerType','parking','bedrooms',
'bathrooms','antiquity','description','price','contactName','phone','coordinates']
df_Offers = pd.DataFrame(columns=columns)

listMilestones = list(range(0,2000,50))
#for wp in listWebPages:
list_IdOffers = []
print(f'Script start for 30 pages: {datetime.datetime.now()}')
while n<=numWebPages: 
# while n<=1: 
    r = requests.get(listWebPages[n], 'html.parser')
    soup = BeautifulSoup(r.content, 'html.parser')
    print(f'Page {n} of {numWebPages}')
    print(f'Begin page: {datetime.datetime.now()}')
    links = soup.find_all('a',{"data-qa":"list-item"})
    path = []
    
    for i in links:
        path.append(i.get('href').strip('//'))

    path.sort()
    pathOffers = list(set(path))
    for path in pathOffers:
        offer_url = 'https://{}'.format(path)
        r = requests.get(offer_url, 'html.parser')
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup)
        sys.exit(0)
        info_oferta = soup.find('main',{'class':'item_index_view wide'})
        loc_oferta = soup.find('a',{'class':'image'})
        if info_oferta is not None:
            dicOferta = info_oferta.get('data-item')
            d = json.loads(dicOferta)
            for key in d:
                if key == 'id':
                    id = d[key]
                ################### saving json
                    # f = open( f'{folderJSON}/{id}.json', 'w' )
                    # f.write(dicOferta)
                    # f.close()
                #################
                elif key == 'title':
                    if d[key] is not None:
                        title = d[key]
                    else:
                        title is None
                elif key == 'coordinates':
                    if d[key] is not None:
                        coordinates = f'{d[key]["latitude"]},{d[key]["longitude"]}'
                    else:
                        coordinates = '0,0'
                elif key == 'optionals':
                    listOferta = d[key]
                    surface=None
                    streetaddress=None
                    parking=None
                    sellerType=None
                    stratus=None
                    bedrooms=None
                    bathrooms=None
                    antiquity = None
                    for i in listOferta:
                        if i['name'] == 'surface':
                            surface = i['value']
                        elif i['name'] == 'streetaddress':
                            streetaddress = i['value']
                        elif i['name'] == 'parking':
                            parking = i['value']
                        elif i['name'] == 'sellerType':
                            sellerType = i['value']
                        elif i['name'] == 'stratus':
                            stratus = i['value']
                        elif i['name'] == 'bedrooms':
                            bedrooms = i['value']
                        elif i['name'] == 'bathrooms':
                            bathrooms = i['value']
                        elif i['name'] == 'antiquity':
                            antiquity = i['value']
                        else:
                            pass
                elif key == 'price':
                    if d[key] is not None:
                        price = d[key]['amount']
                    else:
                        price = None
                elif key == 'description':
                    if d[key] is not None:
                        description = d[key]
                    else:
                        description = None
                elif key == 'category':
                    if d[key] is not None:
                        category = d[key]['name']
                    else:
                        category = None
                elif key == 'contactName':
                    if d[key] is not None:
                        contactName = d[key]
                    else:
                        contactName = None
                elif key == 'title':
                    if d[key] is not None:
                        title = d[key]
                    else:
                        title = None
                elif key == 'phone':
                    if d[key] is not None:
                        phone = d[key]
                    else:
                        phone = None
                else:
                    pass
            
            if id not in list_IdOffers and title is not None:
                df_Offers.loc[len(df_Offers)] = [id,offer_url,title,category,surface,streetaddress,stratus,sellerType,parking,bedrooms,bathrooms,antiquity,description,price,contactName,phone,coordinates] 
                list_IdOffers.append(id)
                print(f'id: {id} - Row saved')
            else:
                pass
            time.sleep(1)
            print('sleep time ended')
    print(f'end page: {datetime.datetime.now()}')
    print(f'number of Offers {df_Offers.shape[0]}')
    time.sleep(5)
    if n in listMilestones:
        saveCSV(df_Offers)
        f = open(f"{archivoReporte}.txt", "a")
        f.write(f"Nro ofertas almacenadas: {df_Offers.shape[0]} - {datetime.datetime.now()}\n")
    n +=1
saveCSV(df_Offers)
f = open(f"{archivoReporte}.txt", "a")
f.write(f"Nro Total ofertas ofertas almacenadas: {df_Offers.shape[0]}\n")
f.write(f"Hora Finalización: {datetime.datetime.now()}\n")
f.close()
print('script ended')