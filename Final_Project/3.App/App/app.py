import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import json

df = pd.read_csv('web_scrapping_bogota.csv')
df = df[df['Price'] < 1000000000]
df = df[df['Price'] > 10000000]

def select_json_file(count=None):
    if count:
        with open('Transform_Data/dloc_{}.json'.format(count)) as f:
            geojson = json.loads(f.read())
    else:
        with open('/home/shade/person.json') as f:
            geojson = json.loads(f.read())

    geo = {}

    for i in geojson['features']:
        if i['properties']['SCaNombre'] == 'LA MAGDALENA I':
            geo = i

    return geo

app = dash.Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

token = 'pk.eyJ1IjoiamhvbmFsZXgwNiIsImEiOiJjazJ3c2g1c3owNHo1M3BwZnAzN3pnemwzIn0.SkIbPSPHdjtuvHNJuawvGQ'
with open('Transform_Data/dloc_1.json') as f:
    geojson = json.loads(f.read())


list_of_locations = {
    "1": {"lat": 4.74192856, "lon": -74.02788209},
    "2": {"lat": 4.64492472, "lon": -74.03693918},
    "3": {"lat": 4.59397273, "lon": -74.03621758},
    "4": {"lat": 4.54874901, "lon": -74.06607256},
    "5": {"lat": 4.39002513, "lon": -74.14280650},
    "6": {"lat": 4.57484140, "lon": -74.13598945},
    "7": {"lat": 4.62177996, "lon": -74.19438893},
    "8": {"lat": 4.63034735, "lon": -74.15266762},
    "9": {"lat": 4.67818293, "lon": -74.14015130},
    "10": {"lat": 4.70112556, "lon": -74.11318770},
    "11": {"lat": 4.76320812, "lon": -74.07584528},
    "12": {"lat": 4.66956693, "lon": -74.07355161},
    "13": {"lat": 4.64117359, "lon": -74.08576902},
    "14": {"lat": 4.60715594, "lon": -74.08794787},
    "15": {"lat": 4.58877067, "lon": -74.10284240},
    "16": {"lat": 4.61624547, "lon": -74.11158023},
    "17": {"lat": 4.59660508, "lon": -74.07207080},
    "18": {"lat": 4.56647690, "lon": -74.11336318},
    "19": {"lat": 4.48246027, "lon": -74.16195890},
    "20": {"lat": 4.03656875, "lon": -74.25697872}  
}

df_correc = pd.read_csv('count_bog_by_man_3.csv')
df_correc['SCaCodigo'] = df_correc['SCaCodigo'].apply(lambda x: str(x))
df_correc['SCaCodigo'] = df_correc['SCaCodigo'].str.zfill(6)

centroides = pd.read_csv('centroides_scat.csv')
centroides['SCaCodigo'] = centroides['SCaCodigo'].apply(lambda x: str(x))
centroides['SCaCodigo'] = centroides['SCaCodigo'].str.zfill(6)

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H2(children="Real State Bogota", style={"margin-bottom": "0px"}, className="one-half column",)
        ],
        className='row flex-display'
    ),
    html.Div(
        className='row flex-display', 
        children=[
            html.Div(
                className='pretty_container seven columns',
                children=[
                    html.Div(
                        dcc.Graph(id='map-plot'),
                    ),                     
                ]),
            html.Div(
                className="pretty_container four columns",
                children=[
                    html.Img(
                        className="logo", src=app.get_asset_url("dash-logo.png")
                    ),
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
                                        id="bar-selector",
                                        options=[
                                            {
                                                "label": str(n) + ":00",
                                                "value": str(n),
                                            }
                                            for n in range(24)
                                        ],
                                        multi=True,
                                        placeholder="Select a Localities",
                                    )
                                ],
                            ),
                            html.Div(
                                className="div-for-dropdown",
                                children=[
                                    # Dropdown to select times
                                    dcc.Dropdown(
                                        id="bar-selector2",
                                        options=[
                                            {
                                                "label": str(n) + ":00",
                                                "value": str(n),
                                            }
                                            for n in range(24)
                                        ],
                                        multi=True,
                                        placeholder="Select a Neighborhood",
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ]
        ),
    html.Div(
        className='row flex-display', 
        children=[
            html.Div(
                className='pretty_container seven columns',
                children=[
                    dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Histograma', value='tab-1'),
                    dcc.Tab(label='Scatter', value='tab-2'),
                    dcc.Tab(label='Heatmap', value='tab-3'),
                    dcc.Tab(label='Bubble', value='tab-4'),
                ]),
                html.Div(id='tabs-grap')                     
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
                                    html.P("""Select the Variable of your dataframe."""),
                                    dcc.Dropdown(
                                        id="filter_2",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in df.columns
                                        ],
                                        multi=False,
                                        placeholder="Select a location",
                                    )
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
    [Output('map-plot', 'figure')],
    [Input('map-plot', 'clickData'),
    Input('location-dropdown', 'value')])

def display_click_data(clickData, loc):
    geojson = select_json_file(loc)

    if loc:
        lat = list_of_locations[loc]['lat']
        lon = list_of_locations[loc]['lon']
        zoom = 11
    else:
        lat = 4.6109886
        lon = -74.072092
        zoom = 9

    figure={ 
            'data': [go.Choroplethmapbox(
                geojson=geojson,
                locations=df_correc['SCaCodigo'],
                z=df_correc['count'],
                colorscale='hsv',
                text=df_correc['SCaNombre'],
                colorbar_title="Number of offers"
            ),go.Scattermapbox(
                mode = "markers",
                lon = [lon], lat = [lat],
                marker = {'size': 20, 'color': ["cyan"]})],
            'layout': go.Layout(
                    mapbox_style='mapbox://styles/jhonalex06/ck3kjaj3i3u6x1cpjlnzxxjwy',
                    mapbox_accesstoken=token,
                    mapbox_zoom=zoom,
                    margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
                    mapbox_center={"lat": lat, "lon": lon}
                )
        }
    if clickData is not None:
        point = centroides[centroides['SCaCodigo'] == click_select_1['points'][0]['location']]
        print (point['lat'])
        print (point['long'])
        figure = { 
                'data': [go.Choroplethmapbox(
                    geojson=geojson,
                    locations=df_correc['SCaCodigo'],
                    z=df_correc['count'],
                    colorscale='hsv',
                    text=df_correc['SCaNombre'],
                    colorbar_title="Thousands USD"
                ),go.Scattermapbox(
                    mode = "markers",
                    lon = [-74.072092, -74.092092], lat = [4.6109886, 4.6109886],
                    marker = {'size': 20, 'color': ["cyan"]})],
                'layout': go.Layout(
                        mapbox_style='mapbox://styles/jhonalex06/ck3kjaj3i3u6x1cpjlnzxxjwy',
                        mapbox_accesstoken=token,
                        mapbox_zoom=9,
                        margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},
                        mapbox_center={"lat": 4.6109886, "lon": -74.072092}
                    )
            }
    return [figure]

@app.callback(
    Output('tabs-grap', 'children'),
    [Input('tabs', 'value'),
     Input('filter_1', 'value'),
     Input('filter_2', 'value')])

def render_content(tab, click_select_1, click_select_2):
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
            click_select_1 = 'Price'
        if click_select_2 == None:
            click_select_2 = 'Rooms'

        df_g = df.groupby(click_select_2)

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
                                xaxis={"title": click_select_2, "showgrid": True},
                                yaxis={"title": "Price", "showgrid": True})}

        return html.Div([
                dcc.Graph(id='group-plots',
                        figure=figure),
        ])

    elif tab == 'tab-3':
        if click_select_1 == None:
            click_select_1 = 'Price'

        data = []
        data.append(go.Histogram(
            x=df[click_select_1], opacity=0.7, name="Male", marker={"line": {"color": "#dd1f70", "width": 0.2}}
        ))

        figure={
            'data': data,
            'layout': go.Layout(title="{} Distribution".format(click_select_1), colorway=['#1fddb3', '#c51b8a'], 
                                xaxis={"title": click_select_1, "showgrid": False},
                                yaxis={"title": "Count", "showgrid": False})}

        return html.Div([
                dcc.Graph(id='group-plots',
                        figure=figure),
        ])

    elif tab == 'tab-4':
        if click_select_1 == None:
            click_select_1 = 'Price'
        if click_select_2 == None:
            click_select_2 = 'Rooms'

        df_g = df.groupby(click_select_2)

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
            'layout': go.Layout(title="{} Distribution".format(click_select_1), colorway=['#1fddb3', '#c51b8a'], 
                                xaxis={"title": click_select_2, "showgrid": True},
                                yaxis={"title": "Price", "showgrid": True})}

        return html.Div([
                dcc.Graph(id='group-plots',
                        figure=figure),
        ])


if __name__ == "__main__":
    app.run_server(debug=True)