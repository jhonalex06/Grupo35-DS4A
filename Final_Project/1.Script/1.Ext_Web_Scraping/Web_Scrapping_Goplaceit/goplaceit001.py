from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Varibles
txtWebsiteUrl = "https://www.goplaceit.com/co/"
cmdEntrarXpath = '/html/body/div[1]/div[1]/div/nav/div[2]/div[1]/form/a'
txtEmailXpath = '//*[@id="signin-email"]'
txtPasswordXpath = '//*[@id="signin-password"]'
cmdLoginXpath = "//button[contains(.,'Iniciar Sesión')]"
txtEmailKeys = 'ds4ajohn@gmail.com'
txtPassKeys = 'DS4A2019'
cmdMisZonasXpath = '/html/body/div[2]/div[1]/div[2]/div/div[1]/div[1]/a'
lblPropertiesCountXpath = '/html/body/div[2]/div[1]/div[4]/div/div[1]/div[2]/div/div[1]/span[3]'
cmdRightArrowXpath = '/html/body/div[2]/div[1]/div[4]/div/div[1]/div[2]/button[2]'
txtPropertiesCount = ""
intPages = 0
divInmuebleXpath = '/html/body/div[2]/div[1]/div[4]/div/div[2]/div[indice]'

# Load Page
driver = webdriver.Firefox()
driver.get(txtWebsiteUrl)


# Estamos en la Landing Page
# Buscar...esperar al botón Entrar, y cuando aparezca darle clic.
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
    except NoSuchElementException:  # Si no hay Facebook...
        blnLoginFound = False
        try:    # Probar MisZona
            cmdMisZonas = driver.find_element_by_xpath(cmdMisZonasXpath)
            blnMisZonasFound = True
        except NoSuchElementException:  # Si tampoco hubo MisZonas, seguir en el loop
            blnMisZonasFound = False
            time.sleep(1)


# Estamos en la página del mapa.
# Buscar...esperar al label PropertiesCount, y cuando aparezca ... esperar a que cargue su innerHRML ... y leerlo!
blnPropertiesCountFound = False
intFailCount = 0
while(blnPropertiesCountFound == False):
    try:
        lblPropertiesCount = driver.find_element_by_xpath(lblPropertiesCountXpath)
        txtPropertiesCount = "-"
        while(txtPropertiesCount == "-"):
            txtPropertiesCount = lblPropertiesCount.get_attribute('innerHTML')
            time.sleep(1)
        print(txtPropertiesCount)
        blnPropertiesCountFound = True
    except NoSuchElementException:
        intFailCount = intFailCount + 1
        blnPropertiesCountFound = False
        time.sleep(1)

# Calcular cuántos ciclos son necesarios para recorrer todo el listado
intPages = 1 + int(txtPropertiesCount.replace('.', '')) // 30

#f = open("goplaceit.txt","w+")
csv = open("goplaceit.csv","w+")
csv.write("Precio;Tipo;Para;Cuartos;Baños;Area\n")
intCurrentPage = 1
while(intCurrentPage <= intPages):
    # Recorrer los 30 registros de una página
    print("Recorriendo los 30 inmuebles de la página ", str(intCurrentPage), " de ", str(intPages))
    intCurrentProperty = 1
    while(intCurrentProperty <= 30):
        divInmuebleXpathCurrent = divInmuebleXpath.replace('indice',str(intCurrentProperty))
        divInmueble = driver.find_element_by_xpath(divInmuebleXpathCurrent)
        txtInmuebleInnerHTML = divInmueble.get_attribute("innerHTML")
        # data-src 10 '"' #Era la imagen, pero creo que no sirve; toca esperar a abrir la ventana modal
        # info price 12 "(COP)"
        txtPrecio = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("$ ") + 2:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("(COP)")-1)) * (-1)]
        #print("Precio: ", txtPrecio)
        #f.write("Precio: " + txtPrecio.strip() + "\n")
        csv.write(txtPrecio.replace('.','').replace(',','.').strip() + ";")
        # info type-summary 18 "en" 2
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
        csv.write(txtTipo.strip() + ";")
        if txtSummary.find("Arriendo") != (-1):
            txtPara = "Arriendo"
        elif txtSummary.find("Venta") != (-1):
            txtPara = "Venta"
        else:
            txtPara = "Otro"
        #print("Para: ", txtPara)
        #f.write("Para: " + txtPara.strip() + "\n")
        csv.write(txtPara.strip() + ";")
        # -bed 10
        if txtInmuebleInnerHTML.find("-bed") != -1 :
            txtCamas = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-bed") + 10:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("-shower")-59)) * (-1)]
            #print("Cuartos: ", txtCamas)
            #f.write("Cuartos: " + txtCamas.strip() + "\n")
            csv.write(txtCamas.strip() + ";")
        if txtInmuebleInnerHTML.find("-desk") != -1 :
            txtCamas = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-desk") + 11:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("-shower")-59)) * (-1)]
            #print("Cuartos: ", txtCamas)
            #f.write("Cuartos: " + txtCamas.strip() + "\n")
            csv.write(txtCamas.strip() + ";")
        # -shower 13
        txtBanios = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-shower") + 13:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("-size")-50)) * (-1)]
        #print("Baños: ", txtBanios)
        #f.write("Baños: " + txtBanios.strip() + "\n")
        csv.write(txtBanios.strip() + ";")
        # -size 11 
        txtArea = txtInmuebleInnerHTML[txtInmuebleInnerHTML.find("-size") + 11:(len(txtInmuebleInnerHTML) - (txtInmuebleInnerHTML.find("m²")+2)) * (-1)]
        #print("Área: ", txtArea)
        #f.write("Área: " + txtArea.strip() + "\n")
        csv.write(txtArea.replace('m²','').strip() + "\n")
        #print("==========================")
        #f.write("==========================" + "\n")
        intCurrentProperty = intCurrentProperty + 1

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

#f.close()
csv.close()

