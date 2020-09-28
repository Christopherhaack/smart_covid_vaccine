import pandas as pd
import plotly.express as px
import numpy as np 
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
app = dash.Dash(__name__)
import dash_table
### Data Processing 

data = pd.read_csv('data/county_stats.csv', index_col=False, dtype= {'FIPS': 'str'})


options = {'7 day increase in cases', 
            '14 day increase in cases',
            '7 day increase in deaths', 
            '14 day increase in deaths',
            'at risk pop',
            'percent at risk',
            'Total Population',
            'total cases',
            'total deaths'}
options = [{'value' : x, 'label': x} for x in options]

app.layout = html.Div([

    html.H1("Covid Infections dashboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_metric",
                 options=options,
                 multi=False,
                 value='7 day increase in cases',
                 style={'width': "40%"}
                 ),
    
    dcc.Graph(id='us_map', figure={}),
    dcc.Graph(id='us_table', figure={})
])

@app.callback(
    [
        Output(component_id='us_map', component_property='figure'),
        Output(component_id='us_table', component_property='figure')
        ],
    [    Input(component_id='slct_metric', component_property='value'),
    ])
def return_data(slct_metric):
    df = data.copy()
    print(slct_metric)
    fig = px.choropleth(df, geojson=counties, locations='FIPS', color=df[slct_metric],
                           color_continuous_scale="Reds",
                           range_color=(0, max(df[slct_metric])),
                           scope="usa",
                           hover_data=['County Name', 
                                        'State Name', 
                                        '7 day increase in cases', 
                                        '7 day increase in deaths', 
                                        'percent at risk', 
                                        'total cases',
                                        'total deaths',]
                          )
    df= df.sort_values(slct_metric, ascending=False)
    table = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df[col] for col in list(df.columns)],
               fill_color='lavender',
               align='left'))
    ])

    return [fig, table]


if __name__ == '__main__':
    
    
    app.run_server(debug=True)
