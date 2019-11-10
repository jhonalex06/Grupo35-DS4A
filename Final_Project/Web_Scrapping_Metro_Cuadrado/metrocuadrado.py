print("Inicio web scraping metrocuadrado")

# Import librerias
from IPython.core.display import HTML
from bs4 import BeautifulSoup
import requests # package required to interact with live webpage
import pandas as pd # will use to store the data from the webpage
import csv
import time
import os

######## Creacion de funciones
'''
url = Url de la pagina a consultar
name_file_out = Nombre del archivo con el cual desea guardar los datos consultados
'''
def get_page_html(url, name_file_out,is_save):
    site_content = requests.get(url).text
    if is_save == 1:
        with open(name_file_out+'.html', 'w', encoding="utf-8") as f:
            f.write(site_content)
    return site_content
        
def get_links_from_page_m2(site_content):
    s = BeautifulSoup(site_content, 'html.parser')
    offset = 3
    cont = 0
    list_inmuebles = []
    for t in s.find_all("a"):
        if len(str(t.get('href')).split("/")) > offset:
            if str(t.get('href')).split("/")[offset] == 'inmueble':
                cont += 1
                list_inmuebles.append(t.get('href'))
    return list_inmuebles

def save_df(data, path_name, typ_insert,header):
    #with open(path_name, typ_insert) as f:
    data.to_csv(path_name,header=header,index=False,mode=typ_insert)

fecha_actual = time.strftime("%Y_%m_%d")
if not os.path.exists('2.csv/'):
    os.mkdir('2.csv/')

url_path = 'https://www.metrocuadrado.com//search/list/non-ajax/?'
list_ciudad = ['bogota'] # Listado de las ciudades donde se hace la busqueda
list_mtiponegocio = ['venta'] # Listado del tipo de negocio a buscar
list_mtipoinmueble = ['casas','apartamentos'] # Tipo de inmueble a consultar
list_banos = ['','1','2','3','4','5']

print("")
print("*********************** Parametros de busqueda *******************")
print("Ciudad:          ",list_ciudad)
print("Tipo negocio:    ",list_mtiponegocio)
print("Tipo inmueble:   ",list_mtipoinmueble)
print("Banos:           ",list_banos)


for ciudad in list_ciudad:
    print("Inicio Ciudad",ciudad)
    for mtiponegocio in list_mtiponegocio:
        print("  Inicio tipo_negocio",mtiponegocio)
        for mtipoinmueble in list_mtipoinmueble:
            print("   Inicio tipo_inmueble",mtipoinmueble)
            for mnumbano in list_banos:
                print("    Inicio num_banos",mnumbano)
                # Numero de paginas a consultar
                for i in range(1,200):
                    list_total = []
                    if i%10 == 0:
                        time.sleep(10)
                    df_url_inmuebles_new = pd.DataFrame( columns=['ciudad','tipo_negocio','tipo_inmueble','fecha_consulta','currentPage','url_inmuebles'])
                    currentPage = str(i)
                    #name_file = ciudad+'_'+mtiponegocio+'_'+mtipoinmueble+fecha_actual
                    name_file = 'listado_link_inmuebles_metrocuadrado'
                    site_url= url_path+'&mciudad='+ciudad+'&mnrobanos='+mnumbano+'&mtiponegocio='+mtiponegocio+'&mtipoinmueble='+mtipoinmueble+'&mzona=&msector=&mbarrio=&selectedLocationCategory=&selectedLocationFilter=&mestadoinmueble=&madicionales=&orderBy=&sortType=&companyType=&companyName=&midempresa=&mgrupo=&mgrupoid=&mbasico=&msemillero=&currentPage='+currentPage+'&totalPropertiesCount=999999&totalUsedPropertiesCount=999999&totalNewPropertiesCount=0&sfh=1#2259-92874B1'
                    site_content = get_page_html(site_url,'1.html/'+name_file+'.html',0)
                    list_total = list_total + get_links_from_page_m2(site_content)
                    list_total.sort()
                    list_total = list(set(list_total))
                    df_url_inmuebles_new['url_inmuebles'] = list_total
                    df_url_inmuebles_new['currentPage'] = currentPage
                    df_url_inmuebles_new['ciudad'] = ciudad
                    df_url_inmuebles_new['tipo_negocio'] = mtiponegocio
                    df_url_inmuebles_new['tipo_inmueble'] = mtipoinmueble
                    df_url_inmuebles_new['fecha_consulta'] = fecha_actual
                    if (os.path.exists('2.csv/'+name_file+'.csv')):
                        save_df(df_url_inmuebles_new,'2.csv/'+name_file+'.csv','a',False)
                    else:
                        save_df(df_url_inmuebles_new,'2.csv/'+name_file+'.csv','w',True)
                            
                print("    Fin num_banos",mnumbano)
            print("   Fin tipo_inmueble",mtipoinmueble)
        print("  Fin tipo_negocio",mtiponegocio)
    print("Fin Ciudad",ciudad)

'''data_link_url = pd.read_csv('2.csv/listado_link_inmuebles_metrocuadrado.csv')
data_link_url_unique = pd.DataFrame(data_link_url['url_inmuebles'].unique(),columns=['url_inmuebles'])

list_atributes = {'nombreEmpresa','propertyId','propertyType','propertyTypeId',
                'businessTypeId','hdnBusinessType','cityname','hdCompanyUrl',
                 'hdIsOcasional','propertyPrice','valorVenta','valorArriendo',
                 'areaPrivada','areaConstruida','numHabitaciones','numBanos',
                 'numGaraje','nomBarrio','zona','nameProperty','latitude','longitude'}


atributs_list = {}
cont = 0
for inmueble in data_link_url_unique['url_inmuebles']:
    cont += 1
    if cont%10 == 0:
        time.sleep(5)
    name = inmueble.split('/')[5]
    site_content = get_page_html(inmueble, name,0)
    s = BeautifulSoup(site_content, 'html.parser') 
    is_despublicado = 0
    try:
        if s.find("span",{'class':'label label-default'}).text =='Despublicado':
            is_despublicado= 1
    except:
        is_despublicado= 0

    if is_despublicado == 1:
        print("despublicado")
    else:
        for atributs in s.find_all("input"):
            id = atributs.get('id')
            value = atributs.get('value')
            if id is not None and value is not None:
                if id in list_atributes:
                    atributs_list[id] = str(value)
                    #print(id+': '+value)
        atributs_list['description'] = s.find('p',{'id':'pDescription'}).text
        div = s.find('div',{'class':'m_property_info_details'})

        try:
            for each in div.find_all('dl'):
                id = each.find('h3').text
                text = each.find('h4').text
                atributs_list[id] = str(text)
        except:
            print('m_property_info_details')

        try:
            div = s.find('div',{'class':'m_property_info_details more_info'})
            for each in div.find_all('dl'):
                id = each.find('h3').text
                text = each.find('h4').text
                atributs_list[id] = str(text)
        except:
            print('m_property_info_details more_info')

        try:
            cont = 1
            for div in s.find_all('div',{'class':'m_property_info_details services complements'}):

                for each in div.find_all('li'):
                    id = 'complemento_'+str(cont)
                    text = each.find('h4').text
                    atributs_list[id] = str(text)
                    cont += 1
        except:
            print('m_property_info_details services complements')

        asd = pd.DataFrame.from_dict(atributs_list, orient="index")
        asd.to_csv('2.csv/'+name+'.csv')
        for key in atributs_list.keys():
        print(key+': '+atributs_list.get(key))'''