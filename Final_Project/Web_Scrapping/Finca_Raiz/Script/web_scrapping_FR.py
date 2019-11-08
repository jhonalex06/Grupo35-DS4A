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

count = 1
multiplicador = 1

while True:    
    site_url = 'https://www.fincaraiz.com.co/apartamento-apartaestudio-casa-casa-campestre-casa-lote/venta/bogota/?ad=30|{}||||1||8,22,9,21,23|||67|3630001|||||||||||||||||||1||griddate%20desc||||||'.format(count)
    r = requests.get(site_url, 'html.parser')
    soup = BeautifulSoup(r.content)

    total = int(soup.find_all('span',{'id':'lblNumInm'})[0].text.split()[0].replace(',',''))

    path = []
    links = soup.find_all('li',{"class":"title-grid"})
    for i in links:
        path.append(i.find('a').get('href'))

    for i in path:
        site_url = 'https://www.fincaraiz.com.co{}'.format(i)
        r = requests.get(site_url, 'html.parser')
        soup = BeautifulSoup(r.content)

        for i in soup.find_all('script',{"type":"text/javascript"}):
            if str(i).find('var sfAdvert') > 0:
                new_soup = i

        Data = ast.literal_eval(new_soup.text.split('var sfAdvert = ')[1].split(';\r\n')[0])

        csvfile = "example.csv"
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            A1 = Data['ClientId']
            A2 = Data['ClientName']
            A3 = Data['TransactionId']
            A4 = Data['TransactionType']
            A5 = Data['Category1Id']
            A6 = Data['Category2Id']
            A7 = Data['Category3Id']
            A8 = Data['Category1']
            A9 = Data['Category2']
            A10 = Data['Category3']
            A11 = Data['Location1']
            A12 = Data['Location2']
            A13 = Data['Location3']
            A14 = Data['Location4']
            A15 = Data['Description']
            A16 = Data['Price']
            A17 = Data['ContractType']
            A18 = Data['OutStanding']
            A19 = Data['TopAdvert']
            A20 = Data['ProductLabel']
            A21 = Data['GridDate']
            A22 = Data['Keywords']
            A23 = Data['Status']
            A24 = Data['Surface']
            A25 = Data['Area']
            A26 = Data['LivingArea']
            A27 = Data['Address']
            A28 = Data['Rooms']
            A29 = Data['Capacity']
            A30 = Data['Baths']
            A31 = Data['Ages']
            A32 = Data['DeliveryDate']
            A33 = Data['Condition']
            A34 = Data['Floor']
            A35 = Data['AdministrationPrice']
            A36 = Data['Neighborhood']
            A37 = Data['Stratum']
            A38 = Data['Garages']
            A39 = Data['Extras']
            A40 = Data['Latitude']
            A41 = Data['Longitude']
            A42 = Data['ModifyDate']
            A43 = Data['PriceType']
            A44 = Data['InteriorFloors']
            print ('Page: {}'.format(count))
            writer.writerow([A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17, A18, A19, A20, A21, A22, A23
                            , A24, A25, A26, A27, A28, A29, A30, A31, A32, A33, A34, A35, A36, A37, A38, A39, A40, A41, A42, A43, A44])
        
    count = count + 1
    if count/multiplicador*12:
        time.sleep(5)
        multiplicador = multiplicador + 1








