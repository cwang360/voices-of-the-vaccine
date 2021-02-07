
import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly
import plotly.graph_objs as go
from collections import deque
import random


max_length = 20

X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)


df = pd.read_csv('plotting_points.csv')
print(df.head())


mapbox_access_token = ACCESS_TOKEN

px.set_mapbox_access_token(mapbox_access_token)

fig = px.scatter_mapbox(df, lat="lat", lon="long",  color="Polarity", size="num_tweets",
                  color_continuous_scale=px.colors.sequential.RdBu, size_max=15, zoom=3)

# # fig.show()
# fig.write_html('first_figure.html', auto_open=True)

app = dash.Dash("COVID Vaccine Sentiment Visualizer")
app.layout = html.Div(children=[
    html.H1('Dash Graph'),
    dcc.Input(id='input', value='Enter something', type='text'),
    html.Div(id='output'),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000, # milliseconds between each update
        n_intervals=0
    ),
    # dcc.Graph(id="example",
    #           figure={
    #               'data': [
    #                   {'x': [1, 2, 3, 4, 5], 'y': [1, 2, 3, 4, 3], 'type':'line','name':'boats'},
    #                   {'x': [1, 2, 3, 4, 5], 'y': [2, 2, 1, 5, 3], 'type':'bar','name':'cars'}
    #               ],
    #               'layout':{
    #                   'title':'Basic example'
    #               }
    #           }),
    dcc.Graph(id="map", figure=fig)
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update(input_data):
    try:
        return str(float(input_data)*5)
    except:
        return "not a number"

@app.callback(
    Output('live-graph','figure'),
    [Input('graph-update','n_intervals')]
)
def update_graph(n):
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1, 0.1))
    data=plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )
    return {'data':[data],
            'layout':go.Layout(
                xaxis=dict(range=[min(X),max(X)]),
                yaxis=dict(range=[min(Y),max(Y)]),
            )}

if __name__ == '__main__':
    app.run_server()
print("running")


