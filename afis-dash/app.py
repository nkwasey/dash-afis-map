# -*- coding: utf-8 -*-
"""
Created on Mon May 18 03:24:26 2020

@author: nkwas
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt




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


df = pd.read_csv('Data/West_Africa_Monthly_Firecounts.csv')

app = dash.Dash()



year_options = []
for year in df['Year'].unique():
    year_options.append({'label':str(year),'value':year})

source_options = []
for source in df['Source'].unique():
    source_options.append({'label':str(source),'value':source})

country_options = []
for country in df['Country'].unique():
    country_options.append({'label':str(country),'value':country})




app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = 'pk.eyJ1Ijoibmt3YXNleSIsImEiOiJja2E2dThpeHAwM2l2MnBtemVja25hZHphIn0.HhZtkswYL5b3O7cJbrhyUw'


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
                                    min_date_allowed=dt(2016, 1, 1),
                                    max_date_allowed=dt(2019, 12, 31),
                                    initial_visible_month=dt(2019, 12, 1),
                                    date=dt(2019, 12, 1).date(),
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
               Input("location-dropdown", "value"),])


def update_graph(selected_date, selectedLocation):
    zoom = 3
    latInitial = 8.56
    lonInitial = 1.56
    bearing = 0
    mapData = pd.read_csv('Data/West_Africa_MODIS_FireHotspots.csv')
    # mapData['acq_date'] = pd.to_datetime(mapData['acq_date'])
    mapData1 = mapData[mapData['acq_date'] == selected_date]

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
                hoverinfo= mapData['brightness'],
                marker=go.scattermapbox.Marker(
                    size=5,
                    color='rgb(255,99,71)',
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
    app.run_server(debug=False)