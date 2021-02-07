
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



df = pd.read_csv('plotting_points.csv')
print(df.head())


mapbox_access_token = ACCESS_TOKEN

px.set_mapbox_access_token(mapbox_access_token)

fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",  color="Sentiment", size="Number of Tweets",
                 color_continuous_scale=plotly.colors.sequential.Jet_r, size_max=15, zoom=3)
fig.update_layout(coloraxis_colorbar=dict(
    title="Sentiment",
    tickvals=[-3,15],
    tickmode="array",
    ticktext=["Negative", "Positive"],
    ticks="outside",
))

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
app = dash.Dash("COVID Vaccine Sentiment Visualizer", external_scripts=external_js,
                external_stylesheets=external_css)
app.title = ("Voices of the Vaccine")

app.layout = html.Div(children=[
    html.Div(children=[html.H3("Voices of the Vaccine"),
             html.H5("COVID-19 Vaccine Sentiment Visualizer")],
             style={'padding': '5% 10%', 'margin': '0px', 'background-color': '#e9edf0'
                    }
             ),
    dcc.Graph(id="map", figure=fig, style={"height":"600px"}),
    html.Div(children=[
                       html.H5("About"),
                        html.P(
                            "Ever felt bombarded by social media posts? In today's fast-paced climate, it feels "
                            "difficult to gauge others' opinions on important topics such as the COVID vaccine. "
                            "If only information could be condensed into an all-encompassing, user-friendly "
                            "visualization tool that can help vaccine providers and marketing professionals "
                            "determine appropriate geographic areas to focus their efforts on. We designed Voices"
                            " of the Vaccine to address these concerns and help users develop a better understanding "
                            "of the vast spectrum of global opinions on the vaccine. "
                        ),
                        html.H5("Check out our source code:"),
                       html.A([
                           html.Img(
                               src='assets/github.png',
                               style={
                                   'height': '4%',
                                   'width': '4%',
                                   'float': 'left',
                                   'position': 'relative',
                                   'padding-top': 0,
                                   'padding-left': 0
                               })
                       ], href='https://github.com/cwang360/voices-of-the-vaccine')
                       ],
            style={'padding': '8%', 'margin': '0px','background-color': '#e9edf0'}
            ),
])


if __name__ == '__main__':
    app.run_server()
print("running")


