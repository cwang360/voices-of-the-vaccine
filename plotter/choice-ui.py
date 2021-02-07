import dash
import dash_core_components as dcc
import dash_html_components as html
import time
import pandas as pd


import plotly.express as px

from collections import deque
import plotly.graph_objs as go
import random

max_length = 50
times = deque(maxlen=max_length)
map = deque(maxlen=max_length)
line = deque(maxlen=max_length)
bar = deque(maxlen=max_length)

data_dict = {"Map Graph":map,
"Line Graph": line,
"Bar Graph": bar,
}

mapbox_access_token = ACCESS_TOKEN
df = pd.read_csv('plotting_points.csv')
print(df.head())
px.set_mapbox_access_token(mapbox_access_token)
fig = px.scatter_mapbox(df, lat="lat", lon="long",  color="Polarity", size="num_tweets",
                  color_continuous_scale=px.colors.sequential.RdBu, size_max=15, zoom=3)

def update_obd_values(times, map, line, bar):

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        map.append(random.randrange(180,230))
        line.append(random.randrange(95,115))
        bar.append(random.randrange(170,220))
    else:
        for data_of_interest in [map, line, bar]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, map, line, bar

times, map, line, bar = update_obd_values(times, map, line, bar)

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
app = dash.Dash('sentiment-data',
                external_scripts=external_js,
                external_stylesheets=external_css)

app.layout = html.Div([
    html.Div([
        html.H2('Sentiment Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='sentiment-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Map Graph','Line Graph','Bar Graph'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=0),

    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10})

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('sentiment-data-name', 'value'),
     dash.dependencies.Input('graph-update', 'n_intervals')],
    )
def update_graph(data_names, n):
    graphs = []
    update_obd_values(times, map, line, bar)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'

    for data_name in data_names:
        if(data_name is not "Map Graph"):
            data = go.Scatter(
                x=list(times),
                y=list(data_dict[data_name]),
                name='Scatter',
                fill="tozeroy",
                fillcolor="#6897bb"
                )

            graphs.append(html.Div(dcc.Graph(
                id=data_name,
                animate=True,
                figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                            yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                            margin={'l':50,'r':1,'t':45,'b':1},
                                                            title='{}'.format(data_name))}
                ), className=class_choice))
    graphs.append(html.Div(dcc.Graph(id="map", figure=fig), className=class_choice))
    return graphs

if __name__ == '__main__':
    app.run_server()