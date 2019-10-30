******************************************************************
#11 / 09 / 2019   
# Datathon

##Questions to answer in 1 - 2 paragraphs:

* What did you team accomplish today ?

  * We splitted tasks between every member of the team. Initial taks where:
    * Create the geographic representation of the Uber zones in NYC using geopandas.
    * Compare the dates between the dataframes to identify those days in common in all of them.
    * Create the entity-relations model of the datasets using UML.

* Were there any interesting discoveries you made today and how will this impact what your team chooses to do next?

  * The nta_code attribute is presented in zones, demographic and geographic datasets.
  * Geographic has a 1:m relationship with and zones and demographic dataset.
  * The geographic dataset has the delimitation coordinates of the regions of NYC, which can be generated using geopandas.
  * There are five tables with trips data, in all of them there are date and time data of the start of the trip.
  * Trip datasets have either coordinates or location id so it is possible to establish spatial relationships.

* What, if any, current issues does your team have?

  * Executing scripts to all datasets takes long periods of time due to the size of them.