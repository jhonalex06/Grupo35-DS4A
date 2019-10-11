#10 / 09 / 2019   
# Datathon

##Questions to answer in 1 - 2 paragraphs:

* What did you team accomplish today ?

  * We did a initial data exploration, generated profiles of the datasets.

* Were there any interesting discoveries you made today and how will this impact what your team chooses to do next?

  * No all the datasets have the same starting and ending date. This is relevant if we want to do analizes at specific dates.
  * Uber trips dataset in 2015 does not have location data so this kind of analyze will be difficult to achieve.
  * The format of the date atribute is diferent in each dataset so is necessary normalize the data attributes.

* What, if any, current issues does your team have?

  * The team has problems with the instalation of libraries in Windows.

#Summary

******************************************************************

##Variables

* Viajes de Uber 2014 (01/Abril/2014 - 31/Septiembre/2014)
* Viajes de Uber 2015 (01/Enero/2015 - 31/Junio/2015)
* Viajes Taxis Verdes (01/Abril/2014 - 30/Junio/2015)
* Viajes del Metro (29/Marzo/2014 - 26/Junio/2015)
* Viajes de Taxis Amarillos (01/Abril/2014 - 30/Junio/2015)
* Clima (01/Enero/2014 - 31/Diciembre/2015)
* Información demográfica NTA
* Información geográfica NTA
* Zonas de area metropolitana

***¿Cual es la influencia del clima en la selección del transporte?***
***¿Definición de las zonas en las cuales es mas frecuente el uso de Uber?***
***¿Preferencias de transportes según ingresos y edad de la persona?***
***¿Cuales son los horarios en los cuales es mas demandado el transporte en la ciudad de Nueva York?***

******************************************************************
#11 / 09 / 2019   
# Datathon

##Questions to answer in 1 - 2 paragraphs:

* What did you team accomplish today ?

  * We assigned tasks to every member of the team. Initial taks where:
    * Create the geographic representation of the Uber zones in NYC using geopandas.
    * Compare the dates between the dataframes to identify those days in common in all of them.
    * Create the entity-relations model of the datasets using UML.

* Were there any interesting discoveries you made today and how will this impact what your team chooses to do next?

  * Trips datasets (Uber, MTA, taxis)
  * The nta_code attribute is presented in zones, demographic and geographic datasets.
  * Geographic has a 1:m relationship with and zones and demographic dataset.
  * The geographic dataset has the delimitation coordinates of the regions of NYC, which can be generated using geopandas.
  * There are five tables with trips data, in all of them there are date and time data of the start of the trip.
  * Trip datasets have either coordinates or location id so it is possible to establish spatial relationships.

* What, if any, current issues does your team have?

  * Executing scripts to all datasets takes long periods of time due to the size of them.