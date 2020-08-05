# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 21:15:20 2020

@author: Joanna Khek Cuina
"""
# from scraping script
#from spotify_top_songs_artists import short_top_artists, long_top_artists, df_short_track, df_long_track

import pandas as pd
import numpy as np
import os
import glob
import base64
import plotly.express as px

# dash
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt
import plotly.graph_objs as go

# import data
df_short_artists = pd.read_csv("short_top_artists.csv")
df_long_artists = pd.read_csv("long_top_artists.csv")
df_short_tracks = pd.read_csv("df_short_track.csv")
df_long_tracks = pd.read_csv("df_long_track.csv")
    
# combine
df_short_artists["category"] = "Short Term"
df_long_artists["category"] = "Long Term"
df_short_tracks["category"] = "Short Term"
df_long_tracks["category"] = "Long Term"

df_short_artists["rank"] = np.arange(1, len(df_short_artists) +1)
df_long_artists["rank"] = np.arange(1, len(df_long_artists) +1)
df_short_tracks["rank"] = np.arange(1, len(df_short_tracks)+1)
df_long_tracks["rank"] = np.arange(1, len(df_long_tracks)+1)

df_artists = pd.concat([df_short_artists, df_long_artists], axis=0)
df_tracks = pd.concat([df_short_tracks, df_long_tracks], axis=0)
df_artists = df_artists.reset_index().drop("index", axis=1)
df_tracks = df_tracks.reset_index().drop("index", axis=1)

artists_col = ["rank", "name", "image"]
tracks_col = ["rank", "name", "album", "artists"]

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color":"#4e5d6c"}

CONTENT_STYLE = {
    "margin-left": "25rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    }

sidebar = html.Div(
    [
         html.H2("Spotify Explorer", className="display-4"),
         html.Hr(),
         html.P(
             "Explore your Spotify music taste", className="lead"
             ),
         dbc.Nav(
             [  
                 dbc.NavLink("Homepage", href="/page-1", id="page-1-link"),
                 dbc.NavLink("Artists", href="/page-2", id="page-2-link"),
                 dbc.NavLink("Tracks", href="/page-3", id="page-3-link"),
                 dbc.NavLink("Track Details", href="/page-4", id="page-4-link"),
             ],
             vertical = True,
             pills = True,
             ),
    ],
    style = SIDEBAR_STYLE,
    )
    
content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

options = [dbc.DropdownMenuItem("Long Term"), 
           dbc.DropdownMenuItem("Short Term"), 
           dbc.DropdownMenuItem("Recent")]

dropdown_type = {
    "background-color": "#aa2222",
    # "color": "white",
    # "color": "#ffffff",
    # "fontColor": "white",
    # "font-color": "white",
    "width": "155px",
    "font-family": "sans-serif",
    "font-size": "large",
}
# Page 1 (Homepage)

page_1_layout = html.Div([
    html.H1("Explore your Spotify music taste!"),
    html.Br(),
    html.P("Ever wondered about the kind of music you listen to? This web application allows you to explore the top artists and tracks you've been listening to.")
    ])

page_2_layout = html.Div([
    html.H1("Your Top Artists"),
    html.Br(),
    html.Div([
        dcc.Dropdown(
                    id='dropdown-2',
                    style={
                            'width': '200px', 
                            'background-color': "#ffffff",
                            'color': '#000',
                            'border-radius': '5px',
                            },
                    options=[{'label': i, 'value': i} for i in ["Long Term", "Short Term"]],
                    value="Long Term"
                    ),
        ]),
    html.Br(),
    # html.Div([
    #     dt.DataTable(id='table-container-2',
    #                  columns=[{"name": i, "id": i} for i in artists_col],
    #                  data=list(df_artists.to_dict("index").values()),
    #                  style_as_list_view=True,
    #                  style_data_conditional=[
    #                      {
    #                         'if': {'row_index': 'odd'},
    #                         'backgroundColor': 'rgb(248, 248, 248)'
    #                     }
    #                      ],
    #                  style_cell={
    #                      'textAlign': 'left',
    #                      'padding': '5px',
    #                      'color': "#303030"},
    #                  style_header={
    #                      'backgroundColor': 'rgb(230, 230, 230)',
    #                      'fontWeight': 'bold'
    #                      }
    #                  )
    #     ]),

    
    html.Div(
        id = 'output-div-2'
                    )
    ])

page_3_layout = html.Div([
     html.H1("Your Top Tracks"),
    html.Br(),
    html.Div([
        dcc.Dropdown(
                    id='dropdown-3',
                    style={
                            'width': '200px', 
                            'background-color': "#ffffff",
                            'color': '#000',
                            'border-radius': '5px',
                            },
                    options=[{'label': i, 'value': i} for i in ["Long Term", "Short Term"]],
                    value="Long Term",
                    ),
        ]),
    html.Br(),
    # html.Div([
    #     dt.DataTable(id='table-container-3',
    #                   columns=[{"name": i, "id": i} for i in tracks_col],
    #                   data=list(df_tracks.to_dict("index").values()),
    #                   style_as_list_view=True,
    #                   style_data_conditional=[
    #                       {
    #                         'if': {'row_index': 'odd'},
    #                         'backgroundColor': 'rgb(248, 248, 248)'
    #                     }
    #                       ],
    #                   style_cell={
    #                       'textAlign': 'left',
    #                       'padding': '5px',
    #                       'color': "#303030"},
    #                   style_header={
    #                       'backgroundColor': 'rgb(230, 230, 230)',
    #                       'fontWeight': 'bold'
    #                       }
    #                   )
    #     ]),
    
    html.Div(
        id = 'output-div-3'
                    )
    ])



page_4_layout = html.Div([
     html.H1("Your Top Tracks Details"),
    html.Br(),
    html.Div([
        dcc.Dropdown(
                    id='dropdown-4',
                    style={
                            'width': '200px', 
                            'background-color': "#ffffff",
                            'color': '#000',
                            'border-radius': '5px',
                            },
                    options=[{'label': i, 'value': i} for i in ["Long Term", "Short Term"]],
                    value="Long Term",
                    ),
        ]),
    html.Br(),
    html.Div(
        [
            dbc.Spinner(
                id = "loading-1",
                children=[html.Div([html.Div(id="output-4")])],
                type="circle"
                )
            ]
        ),
    html.Div([
        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Acousticness"),
                        dbc.ListGroupItemText("A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic")
                        ]
                    ),
                
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Danceability"),
                        dbc.ListGroupItemText("Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.")
                        ]
                    ),
                
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Energy"),
                        dbc.ListGroupItemText("Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.")
                        ]
                    ),
                
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Instrumentalness"),
                        dbc.ListGroupItemText("Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.")
                        ]
                    ),
                
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Liveliness"),
                        dbc.ListGroupItemText("Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.")
                        ]
                    ),
                
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Speechiness"),
                        dbc.ListGroupItemText("Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.")
                        ]
                    )
                ]
            )
        ])
                
    
    ])

####### PAGE 4 #########
@app.callback(
    Output("output-4", "children"),
    [Input("dropdown-4", "value")]
    )
def radar_plot(selected_value):
    dff = df_tracks[df_tracks["category"] == selected_value]
    dff = dff.loc[:,['danceability','energy', 'speechiness', 'acousticness','instrumentalness', 'liveness']]
    dff = dff.describe().loc['mean'].reset_index()
    dff["mean"] = dff["mean"].apply(lambda x: round(x,3))
    fig = px.line_polar(dff, r='mean', theta='index', line_close=True, template="plotly_dark")
    fig.update_traces(fill='toself')
    fig.update_layout(paper_bgcolor ='rgba(0, 0, 0, 0)')

                      
    return dbc.Row(
        [
            dbc.Col(dcc.Loading(id = "loading_icon", 
                                children = [
                                    html.Div([
                                        dcc.Graph(figure=fig)
                                        ])
                                    ]
                                )
                    ),
            
                    
                # dbc.Col(html.Div([
                #     dt.DataTable(id='table-container-4',
                #                   columns=[{"name": i, "id": i} for i in dff],
                #                   data=list(dff.to_dict("index").values()),
                #                   style_as_list_view=True,
                #                   style_data_conditional=[
                #                       {
                #                         'if': {'row_index': 'odd'},
                #                         'backgroundColor': 'rgb(248, 248, 248)'
                #                     }
                #                       ],
                #                   style_cell={
                #                       'textAlign': 'left',
                #                       'padding': '5px',
                #                       'color': "#303030"},
                #                   style_header={
                #                       'backgroundColor': 'rgb(230, 230, 230)',
                #                       'fontWeight': 'bold'
                #                       }
                #                   )

                #     ])
                #     )
                
                dbc.Col(html.Div([
                    dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)
                    ])
                    )
                ]
            )
            

####### PAGE 2 ##########
@app.callback(
    Output("table-container-2", "data"),  
    [Input("dropdown-2", "value")]
    )
def update_table_2(selected_value):
    dff = df_artists[df_artists["category"] == selected_value]
    dff = dff.reset_index().drop("index", axis=1) 
    return dff.to_dict("records")

@app.callback(
    Output("output-div-2", "children"),
    [Input("dropdown-2", "value")])
def image_output_2(selected_value):
    dff = df_artists[df_artists["category"] == selected_value]
    dff = dff.reset_index().drop("index", axis=1) 
    temp = []
    for i in range(0, 6):
        if (i % 5 == 0):
            temp.append(dbc.Row([
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i], dff["name"][i]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+1]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+1], dff["name"][i+1]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+2]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+2], dff["name"][i+2]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+3]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+3], dff["name"][i+3]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+4]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+4], dff["name"][i+4]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                )
                            ])
                )

    return temp
            


############ PAGE 3 ##############
@app.callback(
    Output("table-container-3", "data"),  [Input("dropdown-3", "value")]
    )
def update_table_3(selected_value):
    dff = df_tracks[df_tracks["category"] == selected_value]
    return dff.to_dict("records")

@app.callback(
    Output("output-div-3", "children"),
    [Input("dropdown-3", "value")])

def image_output_3(selected_value):
    dff = df_tracks[df_tracks["category"] == selected_value]
    dff = dff.reset_index().drop("index", axis=1)
    temp = []
    for i in range(0, 21):
        if (i % 5 == 0):
            temp.append(dbc.Row([
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i], dff["title"][i]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+1]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+1], dff["title"][i+1]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+2]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+2], dff["title"][i+2]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+3]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+3], dff["title"][i+3]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                ),
                            dbc.Col(
                                html.Div([
                                    dbc.Card([
                                            dbc.CardImg(src="{}".format(dff["image"][i+4]), bottom=True),
                                            dbc.CardBody(
                                                html.P("{}. {}".format(dff["rank"][i+4], dff["title"][i+4]), className="card-text")
                                                )
                                            ],
                                        style={"width": "15rem"})
                                    ])
                                )
                            ])
                )

    return temp
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]


@app.callback(Output("page-content", "children"), 
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page_1_layout
    elif pathname == "/page-2":
        return page_2_layout
    elif pathname == "/page-3":
        return page_3_layout
    elif pathname == "/page-4":
        return page_4_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

        
if __name__ == "__main__":
    app.run_server(port=8887)
    
