#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output, State
import json
import requests
from sqlalchemy import create_engine

#df = pd.read_csv('web_scrapping_bogota.zip')

#engine = create_engine('postgresql://postgres:NAURpBox6xqQ818bohcy@team35.cg2dtisb0zbb.us-east-2.rds.amazonaws.com/realstate')
#df = pd.read_sql("SELECT * from realstate.data_full", engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
df = pd.read_csv('/home/shade/DS4A/Grupo35-DS4A/Final_Project/2.Export/2.Final/data_to_train.zip')
df = df[df['precio'] < 1000000000]
df = df[df['precio'] > 10000000]
df = df[df['area'] > 0]
df = df[df['estrato'] > 0]
URL = 'http://ec2-3-19-245-73.us-east-2.compute.amazonaws.com:8000/datos_compuestos/'

df = df[['area','edad','estrato','latitude','longitude','num_banos','num_garages','numero_habitaciones','piso_interior',
             'piso_ubicacion','precio','precio_administracion','tipo_inmueble','sector_catastral','CountBibliotecas','CountCanchasSinteticas',
             'CountCicloParqueadero','CountColegios','CountFarmacia','CountEPS','CountMuseos','CountSITP','CountParquesUrbanos',
             'CountTeatros','LocNombre','CountRestaurantes','CountIglesias','CountCAIS','Count_loc_DelitosSexuales','Count_loc_Hurtos',
             'zona']]

df.columns = ['Area (m2)','Age (Years)','Stratum','Latitude','Longitude','Num_bathrooms','Num_Garages','Num_Rooms','Interior_Floor',
              'Floor','Price','Administration_Fee','Type','Neighborhood','Count_Libraries','Count_FootballFields',
              'Count_BikeParking','Count_Schools','Count_Pharmacy','Count_IPS','Count_Museums','Count_SITP','Count_Parks',
              'Count_Theaters','Localitie','Count_Restaurants','Count_ReligiousCenters','Count_CAIs','Count_SexualCrimes2019','Count_Local_larceny2019',
              'Zone']

print (np.sort(df['Stratum'].unique()))

list_of_locations = {
    "Nororiente": [1,2],
    "Centro": [3,14,17],
    "Sur": [4,5,6,15,18,19],
    "Noroccidente": [10, 11, 12],
    "Occidente": [8,9,13,14,16]  
}

def select_zone_json_file(loc):
    with open('/home/shade/DS4A/Grupo35-DS4A/Final_Project/3.App/Transform_Data/All_loc_geo.json') as f:
        geojson = json.loads(f.read())

    features = []
    lon = []
    lat = []
    geo = {}
    loca = []

    for i in geojson['features']:
        for j in list_of_locations[loc]:
            if i['properties']['CODIGO_LOC'] == str(j):
                if i['properties']['NOMBRE'] != None:
                    loca.append(i['properties']['NOMBRE'].lower())
                features.append(i)
                lon.append(i['geometry']['coordinates'][0][0][0][0])
                lat.append(i['geometry']['coordinates'][0][0][0][1])
            
    geo['type'] = 'FeatureCollection'
    geo['features'] = features
    y = min(lat) + (max(lat) - min(lat))/2
    x = min(lon) + (max(lon) - min(lon))/2

    loca = list(dict.fromkeys(loca))

    return geo, x, y, loca

def select_loca_json_file(localities, geojson):
    features = []
    lon = []
    lat = []
    geo = {}
    sect = []

    for i in geojson['features']:
        if i['properties']['NOMBRE'] == localities.upper():
            if i['properties']['NOMBRE'] != None:
                sect.append(i['properties']['SCaNombre_'].lower())
            features.append(i)
            lon.append(i['geometry']['coordinates'][0][0][0][0])
            lat.append(i['geometry']['coordinates'][0][0][0][1])
            
    geo['type'] = 'FeatureCollection'
    geo['features'] = features
    y = min(lat) + (max(lat) - min(lat))/2
    x = min(lon) + (max(lon) - min(lon))/2

    sect = list(dict.fromkeys(sect))

    return geo, x, y, sect

def select_sec_json_file(sectors, geojson):
    features = []
    lon = []
    lat = []
    geo = {}

    for i in geojson['features']:
        if i['properties']['SCaNombre'] == sectors.upper():
            features.append(i)
            lon.append(i['geometry']['coordinates'][0][0][0][0])
            lat.append(i['geometry']['coordinates'][0][0][0][1])
            
    geo['type'] = 'FeatureCollection'
    geo['features'] = features
    y = min(lat) + (max(lat) - min(lat))/2
    x = min(lon) + (max(lon) - min(lon))/2

    return geo, x, y

app = dash.Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

token = 'pk.eyJ1IjoiY2Fsc2dlbyIsImEiOiJjanpyYmh6OGgxOWgyM29qc2QzNWk1Ym52In0.Jc2xgWTnJIre_JhUKSdFWA'
with open('Transform_Data/dloc_1.json') as f:
    geojson = json.loads(f.read())

df_correc = pd.read_csv('count_bog_by_man_3.csv')
df_correc['SCaCodigo'] = df_correc['SCaCodigo'].apply(lambda x: str(x))
df_correc['SCaCodigo'] = df_correc['SCaCodigo'].str.zfill(6)

centroides = pd.read_csv('centroides_scat.csv')
centroides['SCaCodigo'] = centroides['SCaCodigo'].apply(lambda x: str(x))
centroides['SCaCodigo'] = centroides['SCaCodigo'].str.zfill(6)

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H1(children="Real State Bogota", className="twelve column",)
        ],
        className='row flex-display'
    ),
    html.Div(
        className='row flex-display', 
        children=[
            html.Div(
                className='pretty_container eight columns',
                children=[
                    html.Div(
                        dcc.Graph(id='map-plot'),
                    ),                     
                ]),
            html.Div(
                className="pretty_container four columns",
                children=[
                    #html.Img(className="logo", src=app.get_asset_url("dash-logo.png")),
                    html.H2("DASH - REAL STATE BOGOTA APP"),
                    html.P("""Select the location of your dataframe."""),
                    # Change to side-by-side for mobile layout
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                className="div-for-dropdown",
                                children=[
                                    # Dropdown for locations on map
                                    dcc.Dropdown(
                                        id="location-dropdown",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in list_of_locations
                                        ],
                                        placeholder="Select a Zone",
                                    )
                                ],
                            ),
                            html.Div(
                                className="div-for-dropdown",
                                children=[
                                    # Dropdown to select times
                                    dcc.Dropdown(
                                        id="localities-selector",
                                        options=[
                                            {
                                                "label": str(n) + ":00",
                                                "value": str(n),
                                            }
                                            for n in range(24)
                                        ],
                                        placeholder="Select a Localities",
                                    )
                                ],
                            ),
                            html.Div(
                                className="div-for-dropdown",
                                children=[
                                    # Dropdown to select times
                                    dcc.Dropdown(
                                        id="sector-selector",
                                        options=[
                                            {
                                                "label": str(n) + ":00",
                                                "value": str(n),
                                            }
                                            for n in range(24)
                                        ],
                                        placeholder="Select a Neighborhood",
                                    )
                                ],
                            ),
                            html.Hr(),
                            html.P("""Select feature of interest and add to the map."""),
                            # Change to side-by-side for mobile layout
                            dcc.RadioItems(
                                id="items-selector",
                                options=[
                                    {'label': 'hotel', 'value': 'lodging'},
                                    {'label': 'bike', 'value': 'bicycle'},
                                    {'label': 'museum', 'value': 'museum'}
                                ],
                                value='lodging',
                                labelStyle={'display': 'inline-block'}
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.P(id='resume0', children=""),
                    html.P(id='resume1', children=""),
                    html.P(id='resume2', children=""),
                    html.P(id='resume3', children="")
                ],
            ),
            ]
        ),
    html.Div(
        className='row flex-display', 
        children=[
            html.Div(
                className='pretty_container eight columns',
                children=[
                    dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Histogram', value='tab-1'),
                    dcc.Tab(label='Scatter', value='tab-2'),
                    dcc.Tab(label='Heatmap', value='tab-3'),
                    dcc.Tab(label='Bubble', value='tab-4'),
                ]),
                html.Div(id='tabs-grap'),        
                html.P("""Select the Variable of your dataframe."""),
                    dcc.Dropdown(
                        id="filter_1",
                        options=[
                            {"label": i, "value": i}
                            for i in df.columns
                        ],
                        multi=False,
                        placeholder="Select a location",
                    ),    
                #html.Img(id="zack", className="logo", src=app.get_asset_url("zack2.png"))         
                ]),
            html.Div(
                className="pretty_container four columns",
                children=[
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                className="div-for-dropdown",
                                children=[
                                    # Dropdown for locations on map
                                    html.P("""Select the stratum."""),
                                    dcc.Dropdown(
                                        id="stratum_id",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in range(1,7)
                                        ],
                                        multi=False,
                                        placeholder="Select a stratum",
                                    ),
                                    html.P("""Input the Area."""),
                                    dcc.Input(id="area_id", type="text", placeholder="Input the Area"),
                                    html.P("""Select the number of Bathrooms."""),
                                    dcc.Dropdown(
                                        id="baths_id",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in range(1,11)
                                        ],
                                        multi=False,
                                        placeholder="Select a number of bathrooms",
                                    ),
                                    html.P("""Select the number of Rooms."""),
                                    dcc.Dropdown(
                                        id="rooms_id",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in range(1,11)
                                        ],
                                        multi=False,
                                        placeholder="Select a number of rooms",
                                    ),
                                    html.P("""Select the number of Garage."""),
                                    dcc.Dropdown(
                                        id="garage_id",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in range(1,5)
                                        ],
                                        multi=False,
                                        placeholder="Select a number of Garages",
                                    ),
                                    html.P("""Select the number of Floor."""),
                                    dcc.Dropdown(
                                        id="floor_id",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in range(1,5)
                                        ],
                                        multi=False,
                                        placeholder="Select a number of Floors",
                                    ),
                                    html.P("""Select the Type."""),
                                    dcc.Dropdown(
                                        id="type_id",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in np.sort(df['Type'].unique())
                                        ],
                                        multi=False,
                                        placeholder="Select a Type",
                                    ),
                                    html.Hr(),
                                    html.Button('Predict', id='button'),
                                    html.Hr(),
                                    html.H2(id='result_prediction', children='jhon'),
                                    html.Hr(),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ]
        ),
        ]
)

@app.callback(
    [Output('result_prediction', 'children')],
    [Input('button', 'n_clicks'),
     Input('stratum_id', 'value'),
     Input('location-dropdown', 'value'),
     Input('area_id', 'value'),
     Input('baths_id', 'value'),
     Input('rooms_id', 'value'),
     Input('garage_id', 'value'),
     Input('items-selector', 'value'),
     Input('floor_id', 'value'),
     Input('type_id', 'value'),
     Input('localities-selector', 'value'),
     Input('sector-selector', 'value')])

def prediction_model(n_clicks, stratum, zona, area, baths, rooms, garage, item_counts, floor, types, localities, sector):
    if n_clicks is not None and stratum is not None and zona is not None and area is not None and baths is not None and rooms is not None and garage is not None and item_counts is not None and floor is not None and types is not None and localities is not None and sector is not None:
        estrato = stratum
        zona = zona
        area = area
        banos = baths
        hab = rooms
        garajes = garage

        if item_counts == 'lodging':
            countah = 100
            countcp = 0
            countms = 0
        if item_counts == 'bicycle':
            countah = 0
            countcp = 100
            countms = 0
        if item_counts == 'museum':
            countah = 0
            countcp = 0
            countms = 100

        piso_int = floor

        geojson, x, y, loca = select_zone_json_file(zona)
        geojson, x, y = select_sec_json_file(sector, geojson)
        lat = y
        long = x

        tip_inmu = types
        loc = localities

        param = {
        'estrato':[estrato], 
        'zona':[zona], 
        'log_area':[np.log(float(area))], 
        'num_banos':[banos],
        'numero_habitaciones':[hab], 
        'num_garages':[garajes], 
        'Count_loc_AlojamientoHospedaje':[countah], 
        'Count_loc_CicloParqueadero':[countcp], 
        'Count_loc_Museos':[countms],
        'piso_interior':[piso_int],
        'latitude':[lat],
        'longitude':[long],
        'tipo_inmueble':[tip_inmu],
        'Locnombre':[loc]}
   
        r = requests.post(url = URL, json = param)
        print (r.json()[0].keys())
        result = r.json()

    print (n_clicks)
    if n_clicks is None:
        return ['']
    else:
        return ['Your prediction is: {0:.0f}'.format(result[0].values()[0][0])]


@app.callback(
    [Output('resume0', 'children'),
     Output('resume1', 'children'),
     Output('resume2', 'children'),
     Output('resume3', 'children')],
    [Input('sector-selector', 'value')])

def resume_variables(sector):

    price = ''
    rooms = ''
    baths = ''
    area = ''

    if sector != None:
        df_sector = df[df['Neighborhood'] == sector.lower()]
        price = 'The price per square meters is: $ {0:.0f}'.format((df_sector['Price']/ df_sector['Area (m2)']).mean())
        rooms = 'The average of rooms is: {0:.1f}'.format(df_sector['Num_Rooms'].mean())
        baths = 'The average of baths is: {0:.1f}'.format(df_sector['Num_bathrooms'].mean())
        area = 'The average of area is: {0:.1f} square meters'.format(df_sector['Area (m2)'].mean())

    return [price, rooms, baths, area]

@app.callback(
    [Output('map-plot', 'figure'),
     Output('localities-selector', 'options'),
     Output('localities-selector', 'disabled'),
     Output('sector-selector', 'options'),
     Output('sector-selector', 'disabled')],
    [Input('map-plot', 'clickData'),
     Input('location-dropdown', 'value'),
     Input('localities-selector', 'value'),
     Input('sector-selector', 'value'),
     Input('items-selector', 'value')])

def control_display_data(clickData, loc, localities, sectors, item):

    loca_array = []
    loca_state = True
    sect_array = []
    sect_state = True
    geojson = {}
    backup = []
    loca = []
    sect = []

    if loc:
        geojson, x, y, loca = select_zone_json_file(loc)
        lat = y
        lon = x
        zoom = 10
        loca_array = [{"label": i,"value": i} for i in loca]
        loca_state = False
        backup.append(loc)
        if localities:
            if localities in loca:
                geojson, x, y, sect = select_loca_json_file(localities, geojson)
                lat = y
                lon = x
                zoom = 11
                sect_array = [{"label": i,"value": i} for i in sect]
                sect_state = False
            else:
                sect_state = True
            if sectors:
                if sectors in sect:
                    geojson, x, y = select_sec_json_file(sectors, geojson)
                    lat = y
                    lon = x
                    zoom = 14
    else:
        with open('/home/shade/DS4A/Grupo35-DS4A/Final_Project/3.App/Transform_Data/All_loc_geo.json') as f:
            geojson = json.loads(f.read())
        lat = 4.6109886
        lon = -74.072092
        zoom = 9

    figure={ 
            'data': [go.Choroplethmapbox(
                geojson=geojson,
                locations=df_correc['SCaCodigo'],
                z=df_correc['count'],
                colorscale='temps',
                text=df_correc['SCaNombre'] + '<br>' + df_correc['SCaNombre'],
                colorbar_title="Number of offers"
            )],
            'layout': go.Layout(
                    mapbox_style='mapbox://styles/calsgeo/ck3xtpgfk12c61cmmnt3puusu',
                    mapbox_accesstoken=token,
                    mapbox_zoom=zoom,
                    margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
                    mapbox_center={"lat": lat, "lon": lon}
                )
        }
    if clickData is not None and sectors != None:
        point = centroides[centroides['SCaCodigo'] == clickData['points'][0]['location']]
        figure = { 
                'data': [go.Choroplethmapbox(
                    geojson=geojson,
                    locations=df_correc['SCaCodigo'],
                    z=df_correc['count'],
                    colorscale='deep',
                    text=df_correc['SCaNombre'],
                    colorbar_title="Thousands USD"
                ),
                go.Scattermapbox(
                    mode = "markers",
                    #lon = point['long'].tolist(), lat = point['lat'].tolist(),
                    lon = point['lat'].tolist(), lat = point['long'].tolist(),
                    marker = {'size': 20, 'symbol': [item]})],
                'layout': go.Layout(
                        mapbox_style='mapbox://styles/calsgeo/ck3xtpgfk12c61cmmnt3puusu',
                        mapbox_accesstoken=token,
                        mapbox_zoom=14,
                        margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
                        mapbox_center={"lat": lat, "lon": lon}
                    )
            }

    return [figure, loca_array, loca_state, sect_array, sect_state]

@app.callback(
    Output('tabs-grap', 'children'),
    [Input('tabs', 'value'),
     Input('filter_1', 'value')])

def render_content(tab, click_select_1):
    if tab == 'tab-1':
        if click_select_1 == None:
            click_select_1 = 'Price'

        data = []
        data.append(go.Histogram(
            x=df[click_select_1], opacity=0.7, name="Male", marker={"line": {"color": "#dd1f70", "width": 0.2}}
        ))

        figure={
            'data': data,
            'layout': go.Layout(title="{} Distribution".format(click_select_1), colorway=['#1fddb3', '#c51b8a'], 
                                xaxis={"title": click_select_1, "showgrid": True},
                                yaxis={"title": "Count", "showgrid": True})}

        return html.Div([
                dcc.Graph(id='group-plots',
                        figure=figure),
        ])
    
    elif tab == 'tab-2':
        if click_select_1 == None:
            click_select_1 = 'Num_Rooms'

        df_g = df.groupby(click_select_1)

        x = []
        y = []

        for i in df_g:
            x.append(i[0])
            y.append(i[1]['Price'].mean())

        data = []
        data.append(go.Scatter(
            x=x, y=y, opacity=0.7, name="Male", mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}
        ))

        figure={
            'data': data,
            'layout': go.Layout(title="{} Distribution".format(click_select_1), colorway=['#1fddb3', '#c51b8a'], 
                                xaxis={"title": click_select_1, "showgrid": True},
                                yaxis={"title": "Price", "showgrid": True})}

        return html.Div([
                dcc.Graph(id='group-plots',
                        figure=figure),
        ])

    elif tab == 'tab-3':
        if click_select_1 == None:
            click_select_1 = 'Stratum'

        x = []
        z1 = []
        z = []
        y = df[click_select_1].unique().tolist()
        y.sort()
        range_p = (df['Price'].max() - df['Price'].min())/10

        for i in range(1,11):
            if i != 1:
                precio_ant = df['Price'].min() + (range_p * (i-1))
            else:
                precio_ant = 0
                
            precio = df['Price'].min() + (range_p * i)
            x.append(precio)

            for j in y:
                z1.append(df[(df[click_select_1] == j) & (df['Price'] >= precio_ant) & (df['Price'] <= precio)]['Price'].count())
                
            z.append(z1)
            z1 = []

        data = []
        data.append(go.Heatmap(x=y, y=x, z=z, colorscale='greens', colorbar={"title": "Count"}, showscale=True))

        figure={
            'data': data,
            'layout': go.Layout(title="{} Distribution".format(click_select_1), colorway=['#1fddb3', '#c51b8a'], 
                                xaxis={"title": click_select_1, "showgrid": True},
                                yaxis={"title": "Price", "showgrid": True},
                                yaxis_tickformat = '$,.2s')}

        return html.Div([
                dcc.Graph(id='group-plots',
                        figure=figure),
        ])

    elif tab == 'tab-4':
        if click_select_1 == None:
            click_select_1 = 'Zone'

        df_g = df.groupby(click_select_1)

        x = []
        y = []
        z = []
        z1 = []

        for i in df_g:
            x.append(i[0])
            y.append(i[1]['Price'].mean())
            z.append(len(i[1]))

        for i in z:
            z1.append((float(i)/max(z))*100)

        data = []
        data.append(go.Scatter(
            x=x, y=y, opacity=0.7, name="Male", mode='markers',
                                marker={'size': z1, "opacity": 0.6}
        ))

        figure={
            'data': data,
            'layout': go.Layout(title="{} Distribution".format(click_select_1), colorway=['#1fddb3', '#dc5948'], 
                                xaxis={"title": click_select_1, "showgrid": True},
                                yaxis={"title": "Price", "showgrid": True})}

        return html.Div([
                dcc.Graph(id='group-plots',
                        figure=figure),
        ])


if __name__ == "__main__":
    app.run_server(debug=True)