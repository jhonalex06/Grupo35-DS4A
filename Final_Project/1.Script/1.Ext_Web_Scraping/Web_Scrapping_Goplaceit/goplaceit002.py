# -------------------------------------------------------------------------------------------------------- #
# Programa:     goplaceit002.py
# Objetivo:     Hacer webscrapping, usando selenium, al sitio web goplaceit.com
# Autor:        Adrián Ivanov
# Fecha:        2019-11-09
# Versión:      002 (la versión está en el nombre del programa)
# SubObjetivo:  En esta versión 002 quiero agregar a los datos, la dirección y de pronto las coordenadas
# -------------------------------------------------------------------------------------------------------- #
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import urllib.request
from socket import timeout
from urllib.error import HTTPError, URLError
import logging
import datetime
from selenium.webdriver.chrome.options import Options
import codecs

# Varibles - muchas son Xpaths de objetos dentro de goplaceit
print("Creando variables iniciales.")
blnUsarDatosDePrueba = True # Para usar TODOS o sólo las 2 primeras páginas
txtCsvFilename = 'goplaceit002.csv' # Archivo de salida
txtWebsiteUrl = "https://www.goplaceit.com/co/" # URL de goplaceit
cmdEntrarXpath = '/html/body/div[1]/div[1]/div/nav/div[2]/div[1]/form/a'
txtEmailXpath = '//*[@id="signin-email"]'
txtPasswordXpath = '//*[@id="signin-password"]'
cmdLoginXpath = "//button[contains(.,'Iniciar Sesión')]"
txtEmailKeys = 'ds4ajohn@gmail.com' # usuario en goplaceit
txtPassKeys = 'DS4A2019'            # password en goplaceit
cmdMisZonasXpath = '/html/body/div[2]/div[1]/div[2]/div/div[1]/div[1]/a'
lblPropertiesCountXpath = '/html/body/div[2]/div[1]/div[4]/div/div[1]/div[2]/div/div[1]/span[3]'
cmdRightArrowXpath = '/html/body/div[2]/div[1]/div[4]/div/div[1]/div[2]/button[2]'
txtPropertiesCount = "" # Variable donde queda el total de propiedades a registrar  (se lee en tiempo de ejecución)
intPages = 0    # Cantidad de páginas presentes en el sitio web (se calcula en tiempo de ejecución)
intPagesDummy = 2   # Cantidad de páginas a procesar al hacer pruebas
divInmuebleXpath = '/html/body/div[2]/div[1]/div[4]/div/div[2]/div[indice]'
tagImageXpath = divInmuebleXpath + '/div[2]/div/div[2]/img'
cmdPerfilCompletoXpath = '/html/body/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div[2]/a[1]'
iconCloseModalwindowXpath = '/html/body/div[3]/div/div/div[1]/button'
txtPerfilCompletoURL = ""

# Load Page
print("Cargando página web.")
driver = webdriver.Firefox()
#driver = webdriver.PhantomJS('C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe')
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(options=chrome_options)
driver.get(txtWebsiteUrl)


# Estamos en la Landing Page
# Buscar...esperar al botón Entrar, y cuando aparezca darle clic.
print("Logging in.")
blnEntrarFound = False
while(blnEntrarFound==False):
    try:
        cmdEntrar = driver.find_element_by_xpath(cmdEntrarXpath)
        cmdEntrar.click()
        blnEntrarFound = True
    except NoSuchElementException:
        blnEntrarFound = False
        time.sleep(1)

# Buscar...esperar a alguno de los botones, ya sea:
# - Login (una etapa más en el ingreso) o 
# - MisZonas (que indica que ingresamos directo)
blnLoginFound = False
blnMisZonasFound = False
while(blnLoginFound==False and blnMisZonasFound==False):
    try:    # Probar Por Login
        txtEmail = driver.find_element_by_xpath(txtEmailXpath)
        txtPass = driver.find_element_by_xpath(txtPasswordXpath)
        cmdLogin = driver.find_elements_by_xpath(cmdLoginXpath)
        txtEmail.send_keys(txtEmailKeys)
        txtPass.send_keys(txtPassKeys)
        txtPass.send_keys(Keys.RETURN)
        blnLoginFound = True  # Salir del ciclo
    except NoSuchElementException:  # Si no hay Login...
        blnLoginFound = False
        try:    # Probar MisZona
            cmdMisZonas = driver.find_element_by_xpath(cmdMisZonasXpath)
            blnMisZonasFound = True
        except NoSuchElementException:  # Si tampoco hubo MisZonas, seguir en el loop
            blnMisZonasFound = False
            time.sleep(1)


# Estamos en la página del mapa.
# Buscar...esperar al label PropertiesCount, y cuando aparezca ... esperar a que cargue su innerHRML ... y leerlo!
print("Estamos en la página inicial.")
blnPropertiesCountFound = False
intFailCount = 0
while(blnPropertiesCountFound == False):
    try:
        lblPropertiesCount = driver.find_element_by_xpath(lblPropertiesCountXpath)
        txtPropertiesCount = "-"
        while(txtPropertiesCount == "-"):
            txtPropertiesCount = lblPropertiesCount.get_attribute('innerHTML')
            time.sleep(1)
        print("Total de Propiedades :",txtPropertiesCount)
        blnPropertiesCountFound = True
    except NoSuchElementException:
        intFailCount = intFailCount + 1
        blnPropertiesCountFound = False
        time.sleep(1)

# Calcular cuántos ciclos son necesarios para recorrer todo el listado
if blnUsarDatosDePrueba == True:
    intPages = intPagesDummy    # Usar valor de prueba
else:
    intPages = 1 + int(txtPropertiesCount.replace('.', '')) // 30      # Calcularlo

#f = open("goplaceit.txt","w+")
csv = open(txtCsvFilename,"w+")
csv.write("Precio;Tipo;Para;Cuartos;Baños;Area;Latitud;Longitud;Restaurante01;Dist;Restaurante02;Dist;Restaurante03;Dist;Bus01;Dist;Bus02;Dist;Bus03;Dist;Mercado01;Dist;Mercado02;Dist;Mercado03;Dist;Escuela01;Dist;Escuela02;Dist;Escuela03;Dist;Tren01;Dist;Tren02;Dist;Tren03;Dist;Universidad01;Dist;Universidad02;Dist;Universidad03;Dist;URL\n")
csv.close()
intCurrentPage = 1
start_time = datetime.datetime.now()
print ("Current date and time : ", end="", flush=True)
print (start_time.strftime("%Y-%m-%d %H:%M:%S"))
while(intCurrentPage <= intPages):
    # Recorrer los 30 registros de una página
    print("Recorriendo los 30 inmuebles de la página ", str(intCurrentPage), " de ", str(intPages))
    intCurrentProperty = 1
    while(intCurrentProperty <= 30):
        divInmuebleXpathCurrent = divInmuebleXpath.replace('indice',str(intCurrentProperty))  # Xpath de la property
        tagImageXpathCurrent = tagImageXpath.replace('indice',str(intCurrentProperty))  # Xpath de la imagen de la property
        txtInmuebleInnerHTML = ""
        blnDivInmuebleFound = False
        while(blnDivInmuebleFound == False):
            try:
                divInmueble = driver.find_element_by_xpath(divInmuebleXpathCurrent)  # El inmueble
                txtInmuebleInnerHTML = divInmueble.get_attribute("innerHTML")
                blnDivInmuebleFound = True
            except:
                blnDivInmuebleFound = False
                time.sleep(0.5)
        # info price 12 "(COP)"
        txtPrecio = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("$ ") + 2:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("(COP)")-1)) * (-1)]
        #print("Precio: ", txtPrecio)
        #f.write("Precio: " + txtPrecio.strip() + "\n")
        with open(txtCsvFilename, "a") as myfile:
            myfile.write(txtPrecio.replace('.','').replace(',','.').strip() + ";")
        # info -summary 10 "en" 2
        txtSummary = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-summary") + 10:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("-shower")-59)) * (-1)]
        #print("txtSummary: ", txtSummary)
        txtTipo = "-"
        txtModo = "-"
        if txtSummary.find("Casa") != (-1):
            txtTipo = "Casa"
        elif txtSummary.find("Apartamento") != (-1):
            txtTipo = "Apartamento"
        elif txtSummary.find("Oficina") != (-1):
            txtTipo = "Oficina"
        else:
            txtTipo = "Otro"
        #print("Tipo: ", txtTipo)
        #f.write("Tipo: " + txtTipo.strip() + "\n")
        with open(txtCsvFilename, "a") as myfile:
            myfile.write(txtTipo.strip() + ";")
        if txtSummary.find("Arriendo") != (-1):
            txtPara = "Arriendo"
        elif txtSummary.find("Venta") != (-1):
            txtPara = "Venta"
        else:
            txtPara = "Otro"
        #print("Para: ", txtPara)
        #f.write("Para: " + txtPara.strip() + "\n")
        with open(txtCsvFilename, "a") as myfile:
            myfile.write(txtPara.strip() + ";")
        # -bed 10
        if txtInmuebleInnerHTML.find("-bed") != -1 :
            txtCamas = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-bed") + 10:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("-shower")-59)) * (-1)]
            #print("Cuartos: ", txtCamas)
            #f.write("Cuartos: " + txtCamas.strip() + "\n")
            with open(txtCsvFilename, "a") as myfile:
                myfile.write(txtCamas.strip() + ";")
        if txtInmuebleInnerHTML.find("-desk") != -1 :
            txtCamas = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-desk") + 11:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("-shower")-59)) * (-1)]
            #print("Cuartos: ", txtCamas)
            #f.write("Cuartos: " + txtCamas.strip() + "\n")
            with open(txtCsvFilename, "a") as myfile:
                myfile.write(txtCamas.strip() + ";")
        # -shower 13
        txtBanios = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-shower") + 13:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("-size")-50)) * (-1)]
        #print("Baños: ", txtBanios)
        #f.write("Baños: " + txtBanios.strip() + "\n")
        with open(txtCsvFilename, "a") as myfile:
            myfile.write(txtBanios.strip() + ";")
        # -size 11 
        txtArea = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-size") + 11:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("m²")+2)) * (-1)]
        #print("Área: ", txtArea)
        #f.write("Área: " + txtArea.strip() + "\n")
        with open(txtCsvFilename, "a") as myfile:
            myfile.write(txtArea.replace('m²','').strip() + ";")
        # Imagen
        txtImageSrc = ""
        divInmueble.click()
        #print("Imagen: ", txtImageSrc)
        #f.write("Imagen: " + txtImageSrc.strip() + "\n")
        # Coordenadas... no es simple. Toca (1) dar clic en el Inmueble,...
        # blnTagImageFound = False
        # while(blnTagImageFound == False):
        #     try:
        #         tagImage = driver.find_element_by_xpath(tagImageXpathCurrent)  # La imagen
        #         blnTagImageFound = True
        #         txtImageSrc = tagImage.get_attribute('src')
        #         tagImage.click()
        #     except:
        #         blnTagImageFound = False
        #         time.sleep(0.5)
        #time.sleep(3)
        # ... (2) dar clic en el botón de Perfil Completo,...
        blnCmdPerfilCompletoFound = False
        while(blnCmdPerfilCompletoFound == False):
            try:
                cmdPerfilCompleto = driver.find_element_by_xpath(cmdPerfilCompletoXpath)
                txtPerfilCompletoURL = cmdPerfilCompleto.get_attribute('href')
                blnTimeout = True
                txtPerfilCompleto = ""
                while(blnTimeout == True):
                    try:
                        r = urllib.request.urlopen(txtPerfilCompletoURL,None,10)
                        site_content = r.read()
                        txtPerfilCompleto = site_content.decode(encoding='utf-8')
                        blnTimeout = False
                    except (HTTPError, URLError) as error:
                        #logging.error('Data not retrieved because %s\nURL: %s', error, txtPerfilCompletoURL)
                        blnTimeout = True
                    except timeout:
                        #logging.error('Socket timed out - URL %s', txtPerfilCompletoURL)
                        blnTimeout = True
                # Buscar la palabra ">Mapa<" y avanzar hacia atrás hasa encontrar 2 veces "/"
                intPosicion = txtPerfilCompleto.find(">Mapa<")
                intPosicionador = 1
                intCuentaSlashes = 0
                intSlashIzqPos = 0
                intSlashDerPos = 0
                while (intCuentaSlashes < 2):
                    if txtPerfilCompleto[intPosicion-intPosicionador] == "/":
                        intCuentaSlashes = intCuentaSlashes + 1
                        if intCuentaSlashes == 1:
                            intSlashDerPos = intPosicion-intPosicionador
                        elif intCuentaSlashes == 2:
                            intSlashIzqPos = intPosicion-intPosicionador
                    intPosicionador = intPosicionador + 1
                txtCoordenadas = txtPerfilCompleto[intSlashIzqPos:intSlashDerPos]
                txtLatitud = txtCoordenadas[1:txtCoordenadas.find(',')]
                txtLongiud = txtCoordenadas[txtCoordenadas.find(',')+1:]
                #print('Latitud: ',txtLatitud,' - Longitud:',txtLongiud)
                with open(txtCsvFilename, "a") as myfile:
                    myfile.write(txtLatitud + ";")
                with open(txtCsvFilename, "a") as myfile:
                    myfile.write(txtLongiud + ";")
                # Buscar las 6 características de Entorno (3 de cada una)
                # Extraer la sección Entorno
                intEntornoPosicionIni = txtPerfilCompleto.find("id='entorno'")
                intEntornoPosicionFin = txtPerfilCompleto.find("class='habitissimo-heading'")
                txtEntorno = txtPerfilCompleto[intEntornoPosicionIni:intEntornoPosicionFin]
                # Buscar ahora dentro de esa sección, para que sea más rápido
                # 1-Restaurantes - Son 3
                intRestaurantesPosicionIni = txtEntorno.find("class='fa-restaurant'")
                # Restaurante 01
                intRestaurante01PosicionIni = txtEntorno.find("<td>",intRestaurantesPosicionIni)+4
                intRestaurante01PosicionFin = txtEntorno.find("</td>",intRestaurante01PosicionIni)
                txtRestaurante01 = txtEntorno[intRestaurante01PosicionIni:intRestaurante01PosicionFin]
                intRestaurante01DistPosicionIni = txtEntorno.find("distance-cell'>",intRestaurante01PosicionFin)+15
                intRestaurante01DistPosicionFin = txtEntorno.find("</td>",intRestaurante01DistPosicionIni)-1
                txtRestaurante01Dist = txtEntorno[intRestaurante01DistPosicionIni:intRestaurante01DistPosicionFin]
                # Restaurante 02
                intRestaurante02PosicionIni = txtEntorno.find("<td>",intRestaurante01DistPosicionFin)+4
                intRestaurante02PosicionFin = txtEntorno.find("</td>",intRestaurante02PosicionIni)
                txtRestaurante02 = txtEntorno[intRestaurante02PosicionIni:intRestaurante02PosicionFin]
                intRestaurante02DistPosicionIni = txtEntorno.find("distance-cell'>",intRestaurante02PosicionFin)+15
                intRestaurante02DistPosicionFin = txtEntorno.find("</td>",intRestaurante02DistPosicionIni)-1
                txtRestaurante02Dist = txtEntorno[intRestaurante02DistPosicionIni:intRestaurante02DistPosicionFin]
                # Restaurante 03
                intRestaurante03PosicionIni = txtEntorno.find("<td>",intRestaurante02DistPosicionFin)+4
                intRestaurante03PosicionFin = txtEntorno.find("</td>",intRestaurante03PosicionIni)
                txtRestaurante03 = txtEntorno[intRestaurante03PosicionIni:intRestaurante03PosicionFin]
                intRestaurante03DistPosicionIni = txtEntorno.find("distance-cell'>",intRestaurante03PosicionFin)+15
                intRestaurante03DistPosicionFin = txtEntorno.find("</td>",intRestaurante03DistPosicionIni)-1
                txtRestaurante03Dist = txtEntorno[intRestaurante03DistPosicionIni:intRestaurante03DistPosicionFin]

                with codecs.open(txtCsvFilename, "a", encoding="utf-8") as myfile:
                #with open(txtCsvFilename, "a") as myfile:
                    myfile.write('"' + txtRestaurante01 + '"' + ";")
                    myfile.write(txtRestaurante01Dist + ";")
                    myfile.write('"' + txtRestaurante02 + '"' + ";")
                    myfile.write(txtRestaurante02Dist + ";")
                    myfile.write('"' + txtRestaurante03 + '"' + ";")
                    myfile.write(txtRestaurante03Dist + ";")

                # 2-Buss - Son 3
                intBussPosicionIni = txtEntorno.find("class='fa-bus-stop'")
                # Bus 01
                intBus01PosicionIni = txtEntorno.find("<td>",intBussPosicionIni)+4
                intBus01PosicionFin = txtEntorno.find("</td>",intBus01PosicionIni)
                txtBus01 = txtEntorno[intBus01PosicionIni:intBus01PosicionFin]
                intBus01DistPosicionIni = txtEntorno.find("distance-cell'>",intBus01PosicionFin)+15
                intBus01DistPosicionFin = txtEntorno.find("</td>",intBus01DistPosicionIni)-1
                txtBus01Dist = txtEntorno[intBus01DistPosicionIni:intBus01DistPosicionFin]
                # Bus 02
                intBus02PosicionIni = txtEntorno.find("<td>",intBus01DistPosicionFin)+4
                intBus02PosicionFin = txtEntorno.find("</td>",intBus02PosicionIni)
                txtBus02 = txtEntorno[intBus02PosicionIni:intBus02PosicionFin]
                intBus02DistPosicionIni = txtEntorno.find("distance-cell'>",intBus02PosicionFin)+15
                intBus02DistPosicionFin = txtEntorno.find("</td>",intBus02DistPosicionIni)-1
                txtBus02Dist = txtEntorno[intBus02DistPosicionIni:intBus02DistPosicionFin]
                # Bus 03
                intBus03PosicionIni = txtEntorno.find("<td>",intBus02DistPosicionFin)+4
                intBus03PosicionFin = txtEntorno.find("</td>",intBus03PosicionIni)
                txtBus03 = txtEntorno[intBus03PosicionIni:intBus03PosicionFin]
                intBus03DistPosicionIni = txtEntorno.find("distance-cell'>",intBus03PosicionFin)+15
                intBus03DistPosicionFin = txtEntorno.find("</td>",intBus03DistPosicionIni)-1
                txtBus03Dist = txtEntorno[intBus03DistPosicionIni:intBus03DistPosicionFin]

                with codecs.open(txtCsvFilename, "a", encoding="utf-8") as myfile:
                #with open(txtCsvFilename, "a") as myfile:
                    myfile.write('"' + txtBus01 + '"' + ";")
                    myfile.write(txtBus01Dist + ";")
                    myfile.write('"' + txtBus02 + '"' + ";")
                    myfile.write(txtBus02Dist + ";")
                    myfile.write('"' + txtBus03 + '"' + ";")
                    myfile.write(txtBus03Dist + ";")

                # 3-Supermercados - Son 3
                intSupermercadosPosicionIni = txtEntorno.find("class='fa-supermarket'")
                # Supermercado 01
                intSupermercado01PosicionIni = txtEntorno.find("<td>",intSupermercadosPosicionIni)+4
                intSupermercado01PosicionFin = txtEntorno.find("</td>",intSupermercado01PosicionIni)
                txtSupermercado01 = txtEntorno[intSupermercado01PosicionIni:intSupermercado01PosicionFin]
                intSupermercado01DistPosicionIni = txtEntorno.find("distance-cell'>",intSupermercado01PosicionFin)+15
                intSupermercado01DistPosicionFin = txtEntorno.find("</td>",intSupermercado01DistPosicionIni)-1
                txtSupermercado01Dist = txtEntorno[intSupermercado01DistPosicionIni:intSupermercado01DistPosicionFin]
                # Supermercado 02
                intSupermercado02PosicionIni = txtEntorno.find("<td>",intSupermercado01DistPosicionFin)+4
                intSupermercado02PosicionFin = txtEntorno.find("</td>",intSupermercado02PosicionIni)
                txtSupermercado02 = txtEntorno[intSupermercado02PosicionIni:intSupermercado02PosicionFin]
                intSupermercado02DistPosicionIni = txtEntorno.find("distance-cell'>",intSupermercado02PosicionFin)+15
                intSupermercado02DistPosicionFin = txtEntorno.find("</td>",intSupermercado02DistPosicionIni)-1
                txtSupermercado02Dist = txtEntorno[intSupermercado02DistPosicionIni:intSupermercado02DistPosicionFin]
                # Supermercado 03
                intSupermercado03PosicionIni = txtEntorno.find("<td>",intSupermercado02DistPosicionFin)+4
                intSupermercado03PosicionFin = txtEntorno.find("</td>",intSupermercado03PosicionIni)
                txtSupermercado03 = txtEntorno[intSupermercado03PosicionIni:intSupermercado03PosicionFin]
                intSupermercado03DistPosicionIni = txtEntorno.find("distance-cell'>",intSupermercado03PosicionFin)+15
                intSupermercado03DistPosicionFin = txtEntorno.find("</td>",intSupermercado03DistPosicionIni)-1
                txtSupermercado03Dist = txtEntorno[intSupermercado03DistPosicionIni:intSupermercado03DistPosicionFin]

                with codecs.open(txtCsvFilename, "a", encoding="utf-8") as myfile:
                #with open(txtCsvFilename, "a") as myfile:
                    myfile.write('"' + txtSupermercado01 + '"' + ";")
                    myfile.write(txtSupermercado01Dist + ";")
                    myfile.write('"' + txtSupermercado02 + '"' + ";")
                    myfile.write(txtSupermercado02Dist + ";")
                    myfile.write('"' + txtSupermercado03 + '"' + ";")
                    myfile.write(txtSupermercado03Dist + ";")

                # 4-Escuelas - Son 3
                intEscuelasPosicionIni = txtEntorno.find("class='fa-school'")
                # Escuela 01
                intEscuela01PosicionIni = txtEntorno.find("<td>",intEscuelasPosicionIni)+4
                intEscuela01PosicionFin = txtEntorno.find("</td>",intEscuela01PosicionIni)
                txtEscuela01 = txtEntorno[intEscuela01PosicionIni:intEscuela01PosicionFin]
                intEscuela01DistPosicionIni = txtEntorno.find("distance-cell'>",intEscuela01PosicionFin)+15
                intEscuela01DistPosicionFin = txtEntorno.find("</td>",intEscuela01DistPosicionIni)-1
                txtEscuela01Dist = txtEntorno[intEscuela01DistPosicionIni:intEscuela01DistPosicionFin]
                # Escuela 02
                intEscuela02PosicionIni = txtEntorno.find("<td>",intEscuela01DistPosicionFin)+4
                intEscuela02PosicionFin = txtEntorno.find("</td>",intEscuela02PosicionIni)
                txtEscuela02 = txtEntorno[intEscuela02PosicionIni:intEscuela02PosicionFin]
                intEscuela02DistPosicionIni = txtEntorno.find("distance-cell'>",intEscuela02PosicionFin)+15
                intEscuela02DistPosicionFin = txtEntorno.find("</td>",intEscuela02DistPosicionIni)-1
                txtEscuela02Dist = txtEntorno[intEscuela02DistPosicionIni:intEscuela02DistPosicionFin]
                # Escuela 03
                intEscuela03PosicionIni = txtEntorno.find("<td>",intEscuela02DistPosicionFin)+4
                intEscuela03PosicionFin = txtEntorno.find("</td>",intEscuela03PosicionIni)
                txtEscuela03 = txtEntorno[intEscuela03PosicionIni:intEscuela03PosicionFin]
                intEscuela03DistPosicionIni = txtEntorno.find("distance-cell'>",intEscuela03PosicionFin)+15
                intEscuela03DistPosicionFin = txtEntorno.find("</td>",intEscuela03DistPosicionIni)-1
                txtEscuela03Dist = txtEntorno[intEscuela03DistPosicionIni:intEscuela03DistPosicionFin]

                with codecs.open(txtCsvFilename, "a", encoding="utf-8") as myfile:
                #with open(txtCsvFilename, "a") as myfile:
                    myfile.write('"' + txtEscuela01 + '"' + ";")
                    myfile.write(txtEscuela01Dist + ";")
                    myfile.write('"' + txtEscuela02 + '"' + ";")
                    myfile.write(txtEscuela02Dist + ";")
                    myfile.write('"' + txtEscuela03 + '"' + ";")
                    myfile.write(txtEscuela03Dist + ";")

                # 5-Trains - Son 3
                intTrainsPosicionIni = txtEntorno.find("class='fa-train'")
                # Train 01
                intTrain01PosicionIni = txtEntorno.find("<td>",intTrainsPosicionIni)+4
                intTrain01PosicionFin = txtEntorno.find("</td>",intTrain01PosicionIni)
                txtTrain01 = txtEntorno[intTrain01PosicionIni:intTrain01PosicionFin]
                intTrain01DistPosicionIni = txtEntorno.find("distance-cell'>",intTrain01PosicionFin)+15
                intTrain01DistPosicionFin = txtEntorno.find("</td>",intTrain01DistPosicionIni)-1
                txtTrain01Dist = txtEntorno[intTrain01DistPosicionIni:intTrain01DistPosicionFin]
                # Train 02
                intTrain02PosicionIni = txtEntorno.find("<td>",intTrain01DistPosicionFin)+4
                intTrain02PosicionFin = txtEntorno.find("</td>",intTrain02PosicionIni)
                txtTrain02 = txtEntorno[intTrain02PosicionIni:intTrain02PosicionFin]
                intTrain02DistPosicionIni = txtEntorno.find("distance-cell'>",intTrain02PosicionFin)+15
                intTrain02DistPosicionFin = txtEntorno.find("</td>",intTrain02DistPosicionIni)-1
                txtTrain02Dist = txtEntorno[intTrain02DistPosicionIni:intTrain02DistPosicionFin]
                # Train 03
                intTrain03PosicionIni = txtEntorno.find("<td>",intTrain02DistPosicionFin)+4
                intTrain03PosicionFin = txtEntorno.find("</td>",intTrain03PosicionIni)
                txtTrain03 = txtEntorno[intTrain03PosicionIni:intTrain03PosicionFin]
                intTrain03DistPosicionIni = txtEntorno.find("distance-cell'>",intTrain03PosicionFin)+15
                intTrain03DistPosicionFin = txtEntorno.find("</td>",intTrain03DistPosicionIni)-1
                txtTrain03Dist = txtEntorno[intTrain03DistPosicionIni:intTrain03DistPosicionFin]

                with codecs.open(txtCsvFilename, "a", encoding="utf-8") as myfile:
                #with open(txtCsvFilename, "a") as myfile:
                    myfile.write('"' + txtTrain01 + '"' + ";")
                    myfile.write(txtTrain01Dist + ";")
                    myfile.write('"' + txtTrain02 + '"' + ";")
                    myfile.write(txtTrain02Dist + ";")
                    myfile.write('"' + txtTrain03 + '"' + ";")
                    myfile.write(txtTrain03Dist + ";")

                # 6-Universidads - Son 3
                intUniversidadsPosicionIni = txtEntorno.find("class='fa-university'")
                # Universidad 01
                intUniversidad01PosicionIni = txtEntorno.find("<td>",intUniversidadsPosicionIni)+4
                intUniversidad01PosicionFin = txtEntorno.find("</td>",intUniversidad01PosicionIni)
                txtUniversidad01 = txtEntorno[intUniversidad01PosicionIni:intUniversidad01PosicionFin]
                intUniversidad01DistPosicionIni = txtEntorno.find("distance-cell'>",intUniversidad01PosicionFin)+15
                intUniversidad01DistPosicionFin = txtEntorno.find("</td>",intUniversidad01DistPosicionIni)-1
                txtUniversidad01Dist = txtEntorno[intUniversidad01DistPosicionIni:intUniversidad01DistPosicionFin]
                # Universidad 02
                intUniversidad02PosicionIni = txtEntorno.find("<td>",intUniversidad01DistPosicionFin)+4
                intUniversidad02PosicionFin = txtEntorno.find("</td>",intUniversidad02PosicionIni)
                txtUniversidad02 = txtEntorno[intUniversidad02PosicionIni:intUniversidad02PosicionFin]
                intUniversidad02DistPosicionIni = txtEntorno.find("distance-cell'>",intUniversidad02PosicionFin)+15
                intUniversidad02DistPosicionFin = txtEntorno.find("</td>",intUniversidad02DistPosicionIni)-1
                txtUniversidad02Dist = txtEntorno[intUniversidad02DistPosicionIni:intUniversidad02DistPosicionFin]
                # Universidad 03
                intUniversidad03PosicionIni = txtEntorno.find("<td>",intUniversidad02DistPosicionFin)+4
                intUniversidad03PosicionFin = txtEntorno.find("</td>",intUniversidad03PosicionIni)
                txtUniversidad03 = txtEntorno[intUniversidad03PosicionIni:intUniversidad03PosicionFin]
                intUniversidad03DistPosicionIni = txtEntorno.find("distance-cell'>",intUniversidad03PosicionFin)+15
                intUniversidad03DistPosicionFin = txtEntorno.find("</td>",intUniversidad03DistPosicionIni)-1
                txtUniversidad03Dist = txtEntorno[intUniversidad03DistPosicionIni:intUniversidad03DistPosicionFin]

                with codecs.open(txtCsvFilename, "a", encoding="utf-8") as myfile:
                #with open(txtCsvFilename, "a") as myfile:
                    myfile.write('"' + txtUniversidad01 + '"' + ";")
                    myfile.write(txtUniversidad01Dist + ";")
                    myfile.write('"' + txtUniversidad02 + '"' + ";")
                    myfile.write(txtUniversidad02Dist + ";")
                    myfile.write('"' + txtUniversidad03 + '"' + ";")
                    myfile.write(txtUniversidad03Dist + ";")

                # Cerrar la ventana modal
                blnIconCloseModalwindowFound = False
                while(blnIconCloseModalwindowFound == False):
                    try:
                        iconCloseModalwindow = driver.find_element_by_xpath(iconCloseModalwindowXpath)
                        iconCloseModalwindow.click()
                        blnIconCloseModalwindowFound = True
                    except NoSuchElementException:
                        blnIconCloseModalwindowFound = False
                        #time.sleep(1)
                blnCmdPerfilCompletoFound = True
            except NoSuchElementException:
                blnCmdPerfilCompletoFound = False
                time.sleep(1)
        with open(txtCsvFilename, "a") as myfile:
            myfile.write(txtPerfilCompletoURL + ";")
        with open(txtCsvFilename, "a") as myfile:
            myfile.write(txtImageSrc.strip() + "\n")
        #print("==========================")
        #f.write("==========================" + "\n")
        print(intCurrentProperty, end="", flush=True)
        intCurrentProperty = intCurrentProperty + 1
        if intCurrentProperty <= 30:
            print(",", end="", flush=True)
        else:
            print(".")

    # Buscar...esperar al botón cmdRightArrow, y cuando aparezca darle clic.
    blnCmdRightArrowFound = False
    while(blnCmdRightArrowFound==False):
        try:
            cmdRightArrow = driver.find_element_by_xpath(cmdRightArrowXpath)
            cmdRightArrow.click()
            blnCmdRightArrowFound = True
        except NoSuchElementException:
            blnCmdRightArrowFound = False
            time.sleep(1)

    # Esperar a que cargue el listado - lo que sucede cuando ya hay un valor en el Total de inmuebles
    blnPropertiesCountFound = False
    while(blnPropertiesCountFound == False):
        try:
            lblPropertiesCount = driver.find_element_by_xpath(lblPropertiesCountXpath)
            txtPropertiesCount = "-"
            while(txtPropertiesCount == "-"):
                txtPropertiesCount = lblPropertiesCount.get_attribute('innerHTML')
                time.sleep(1)
            blnPropertiesCountFound = True
        except NoSuchElementException:
            blnPropertiesCountFound = False
            time.sleep(1)
    # Incrementar contador de páginas
    intCurrentPage = intCurrentPage + 1
    time.sleep(3)

# Terminando el proceso
#f.close()
#print("Cerrando el archivo CSV.")
#csv.close()
print("Cerrando el Browser.")
driver.quit
end_time = datetime.datetime.now()
print ("Current date and time : ", end="", flush=True)
print (end_time.strftime("%Y-%m-%d %H:%M:%S"))

