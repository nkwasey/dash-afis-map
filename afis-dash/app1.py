# -*- coding: utf-8 -*-
"""
Created on Mon May 18 03:24:26 2020

@author: nkwas
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import pandas as pd

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

import requests
import io

USERNAME_PASSWORD_PAIRS = [
    ['eoric', 'password'],['username', 'password']
]



barurl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSso5sOh1-OELOgKS_f7dm_gCelFiOEc68pLmDCfGue1CQAwx0ViznWk_OyTMsxvYe3ZMqCEDY41O0N/pub?gid=1718145299&single=true&output=csv'

mapbox_access_token = 'pk.eyJ1Ijoibmt3YXNleSIsImEiOiJja2E2dThpeHAwM2l2MnBtemVja25hZHphIn0.HhZtkswYL5b3O7cJbrhyUw'


list_of_countries = {
    "Benin": {"lat": 9.1803, "lon": 2.289},
    "Burkina Faso": {"lat": 11.959, "lon": -1.903},
    "Cote D'Ivoire": {"lat": 8.0215, "lon": -5.416},
    "Cape Verde": {"lat": 15.0788, "lon": -23.6225},
    "Ghana": {"lat": 8.14, "lon": -1.3308},
    "Guinea": {"lat": 10.992, "lon": -11.721},
    "Guinea Bissau": {"lat": 12.192, "lon": -14.946},
    "Liberia": {"lat": 6.4906, "lon": -9.5166},
    "Mali": {"lat": 16.764, "lon": -3.204},
    "Mauritania": {"lat": 20.764, "lon": -10.258},
    "Niger": {"lat": 17.853, "lon": 9.2677},
    "Nigeria": {"lat": 9.006, "lon": 8.242},
    "Senegal": {"lat": 14.576, "lon": -14.531},
    "Sierra Leone": {"lat": 8.921, "lon": -11.716},
    "The Gambia": {"lat": 13.797, "lon": -14.773},
    "Togo": {"lat": 8.370, "lon": 1.137},
}



barurlData = requests.get(barurl).content
bar_rawData = pd.read_csv(io.StringIO(barurlData.decode('utf-8')))

df = bar_rawData



year_options = []
for year in df['Year'].unique():
    year_options.append({'label':str(year),'value':year})

source_options = []
for source in df['Source'].unique():
    source_options.append({'label':str(source),'value':source})

country_options = []
for country in df['Country'].unique():
    country_options.append({'label':str(country),'value':country})



# Plotly mapbox public token
mapbox_access_token = 'pk.eyJ1Ijoibmt3YXNleSIsImEiOiJja2E2dThpeHAwM2l2MnBtemVja25hZHphIn0.HhZtkswYL5b3O7cJbrhyUw'


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        
                        html.H2("Fire Map"),
                        html.P(
                            """Select different days using the date picker."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2020, 1, 1),
                                    max_date_allowed=dt(2020, 5, 20),
                                    initial_visible_month=dt(2020, 5, 20),
                                    date=dt(2020, 5, 20).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        html.P(
                            """Select country to zoom into."""
                        ),                        
                        html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_countries
                                            ],
                                            placeholder="Select a location",
                                        )
                                    ],
                                ),
                        html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        
                                        html.P(
                                            """Select data source to show on map"""
                        ),
                                        dcc.RadioItems(
                                            id="source-select",
                                            options=[
                                                {"label": 'MODIS', "value": 'MODIS'},
                                                {"label": 'VIIRS', "value": 'VIIRS'},
                                            ],
                                            
                                            labelStyle = {
                                                'display' : 'inline-block',
                                                'margin-right' : 80
                                                },
                                            value = 'MODIS',
                                        )
                                    ],
                                ),
                        
                        
                        html.Div(
                            className="text1-padding",
                            children=[
                                """
                             
                                """
                                
                            ],
                        ),
                        
                        
                        html.H2(" Monthly Fire Charts"),
                        html.P(
                            """Select different year and source using the dropdown menu
                                to view different bar charts"""
                        ),
                        
                        
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="year-picker",
                                            options= year_options,
                                            value = df['Year'].min(),
                                            placeholder="Select a year",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="source-picker",
                                            options= source_options,
                                            value = df['Source'].min(),
                                            placeholder="Select source",
                                            
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.H4(" Data Sources: "),
                        
                        dcc.Markdown(
                            children=[
                                "Source: [EORIC](https://www.eoric.uenr.edu.gh/)",
                                "Source: [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/download/)"
                                
                            ]
                        ),
                        
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id='graph'),
                        html.Div(
                            className="text-padding",
                            children=[
                                "   "
                            ],
                        ),
                        dcc.Graph(id = 'bar'),
                    ],
                ),
            ],
        )
    ]
)

@app.callback(Output('bar', 'figure'),
              [Input('year-picker', 'value'), Input('source-picker', 'value')])


def update_bar(selected_year, selected_source):
    if selected_year == None and selected_source == None:
        selected_year = 2019
        selected_source = 'MODIS'
        
    if selected_source == None:
        selected_source = 'MODIS'
        
    if selected_year == None:
        selected_year = 2019
        
    filtered_df = df[(df['Year'] == selected_year) & (df['Source'] == selected_source)]
    traces = []
    for country_name in filtered_df['Country'].unique():
        df_by_country = filtered_df[filtered_df['Country'] == country_name]
        #print(df_by_country)
        traces.append(go.Bar(
            x=df_by_country['Month'],
            y=df_by_country['Fire Count'],
            text=df_by_country['Country'],
            name=country_name
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            title = 'Monthly Fire Counts in ' + str(selected_year) + ' (' + selected_source + ')',
            xaxis={'title': 'Months'},
            yaxis={'title': 'Fire Counts'},
            hovermode='closest',
            plot_bgcolor="#323130",
            paper_bgcolor="#323130",
            dragmode="select",
            font=dict(color="white"),
        )
    }


@app.callback(Output('graph', 'figure'),
              [Input('date-picker', 'date'),
               Input("location-dropdown", "value"),
               Input("source-select", "value"),
               ])


def update_graph(selected_date, selectedLocation, selectedSource):
    zoom = 3
    latInitial = 8.56
    lonInitial = 1.56
    bearing = 0
    
    modisurl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR3CsShpxOEx1XUMCdaUlkKU6KEG2Zk9cma3ICabCHttcMWTYSNdwgbiBRRbHK7gxyTzosxhgGElpmh/pub?gid=807295561&single=true&output=csv'
    
    
    viirsurl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQk5nb9-ktHR5ap3rJSQr6o1EEnJRCHIrT2Kh1cXCqJUFqLHHY5imDcwb0E9qdMwvW-AC4HFzy7zEOh/pub?gid=1876585659&single=true&output=csv'
    
    
    if selectedSource == "MODIS":
        modis_urlData = requests.get(modisurl).content
        #mapData = pd.read_csv('Data/West_Africa_MODIS_FireHotspots.csv')
        mapData = pd.read_csv(io.StringIO(modis_urlData.decode('utf-8')))
        mapData['acq_date'] = pd.to_datetime(mapData['acq_date'])
        mapData1 = mapData[mapData['acq_date'] == selected_date]
        color ='rgb(255,99,71)'
        
    if selectedSource == "VIIRS":
        viirs_urlData = requests.get(viirsurl).content
        #mapData = pd.read_csv('Data/West_Africa_VIIRS_FireHotspots.csv')
        mapData = pd.read_csv(io.StringIO(viirs_urlData.decode('utf-8')))
        mapData['acq_date'] = pd.to_datetime(mapData['acq_date'])
        mapData1 = mapData[mapData['acq_date'] == selected_date]
        color ='rgb(222, 15, 11)'

    if selectedLocation:
        zoom = 5
        latInitial = list_of_countries[selectedLocation]["lat"]
        lonInitial = list_of_countries[selectedLocation]["lon"]

    return go.Figure(
        data=[
            # Data for all fires in W/A based on date and location
            go.Scattermapbox(
                lat=mapData1['latitude'],
                lon=mapData1['longitude'],
                mode="markers",
                #hoverinfo= mapData['brightness'],
                marker=go.scattermapbox.Marker(
                    size=5,
                    color= color,
                    opacity=0.7
                )
                ),   
        ],
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 3,
                                        "mapbox.center.lon": "8.56",
                                        "mapbox.center.lat": "8.56",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )



if __name__ == "__main__":
    app.run_server()