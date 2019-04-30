"""
Created on: April 2019
Sasha Prokosheva

Enron (J Skilling) Mailbox analysis dashboard
"""
import pandas as pd
pd.set_option('display.max_colwidth', 500000)
pd.set_option('precision', 0)
import numpy as np
import re
import os

# Download objects
import pickle

# Date
import datetime

# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output, State


##############################################################################################
# Parameters
##############################################################################################
name = 'ENRON: Jeffrey Skilling Mailbox'

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

path = dname + '/data/'
##############################################################################################
# Functions
##############################################################################################
def transform_value(value):
    return 10 ** value

def save_obj(obj, name):
    with open(path + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(path + name + '.pkl', 'rb') as f:
        return pickle.load(f)

##############################################################################################
# Get data
##############################################################################################
# Graph 0
df_stats = pd.read_csv(path + 'df_stats.csv', encoding = 'utf-8')

##############################################################################################
# Graph 1
folders_list = pd.read_csv(path + 'folders_list.csv', encoding='utf-8')

##############################################################################################
# Graph 2
sent_date_count = pd.read_csv(path + 'sent_date_count.csv', encoding='utf-8')
in_date_count = pd.read_csv(path + 'in_date_count.csv', encoding='utf-8')

##############################################################################################
# Graph 3
in_day_mean = pd.read_csv(path + 'in_day_mean.csv', encoding='utf-8')
sent_day_mean = pd.read_csv(path + 'sent_day_mean.csv', encoding='utf-8')

##############################################################################################
# Graph 4
in_hour_mean = pd.read_csv(path + 'in_hour_mean.csv', encoding='utf-8')
in_hour_mean_orig = pd.read_csv(path + 'in_hour_mean_orig.csv', encoding='utf-8')
out_hour_mean = pd.read_csv(path + 'out_hour_mean.csv', encoding='utf-8')
out_hour_mean_orig = pd.read_csv(path + 'out_hour_mean_orig.csv', encoding='utf-8')

##############################################################################################
# Graph 5
df_to_from = pd.read_csv(path + 'df_to_from.csv', encoding='utf-8')

df_to_from.sort_values(by = ['OUT'], ascending=False, inplace = True)
groups_out = df_to_from.head(50)['group'].unique().tolist()
df_to_from.sort_values(by = ['IN'], ascending=False, inplace = True)
groups_in = df_to_from.head(50)['group'].unique().tolist()

# Filter for groups
groups = groups_in
groups = groups + [x for x in groups_out if x not in groups]
groups = [x for x in groups if x == x]
groups = [x for x in groups if x != '0']
groups_filter = []
for group in groups:
    groups_filter +=[{'label': group, 'value': group}]


# Graph 6
#dict_words = load_obj('25_depts_nonreply')
#options_filter_6 = []
#for dept in dict_words:
#    options_filter_6 += [{'label': dept, 'value': dept}]

# Graph 7
df_senders_20 = pd.read_csv(path + 'df_senders_20.csv', encoding = 'utf-8')

# Graph 8
df_senders_20_group = pd.read_csv(path + 'df_senders_20_group.csv', encoding = 'utf-8')

##############################################################################################
# Dash
##############################################################################################

# Style sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
app.title = name

##############################################################################################
# Start Layout
app.layout = html.Div([
# EMPTY Div
    html.Div([
        dcc.Input(
            id='none',
            value=''
        )],
        style={'display': 'none'}),

    html.Div([
        html.Div(
            html.Img(src='/assets/enron_logo.jpg', style={"width":"50px", "margin":"17.5px 0 0 10px"}), className = 'one column'),
        html.Div(name, style={"color":'rgb(48, 134, 217)', "font-size":"40px", "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif", "display":"table-cell", "text-align":"center", "vertical-align": "middle","margin":"10px 0 0 0"}, className='eleven columns'),
        ],
        style = {"background-color":"#F6F6F6", "height": "80px", "margin":"-10px", "text-align":"center"},
        className="row"
        ),


    html.Div(style = {"height":"15px"}),
##############################################################################################
    html.Div([
            dash_table.DataTable(
                id='stats',
                columns = [{"name": i, "id": i} for i in df_stats],
                data = df_stats.to_dict("rows"),
                style_cell={'textAlign': 'center', 'font-size': 16, "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif"},
                editable=False,
                filtering=False,
                sorting=False,
                sorting_type="multi",
            )],
        className="ten columns offset-by-one"),


##############################################################################################
# Row 1: Graphs
    html.Div([

##############################################################################################
# Row 1, Column 1: Daily Counts
    html.Div([
        dcc.Graph(
            id='graph-daily-line',
            config={'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'select2d', 'lasso2d', 'hoverClosestCartesian', 'sendDataToCloud', 'autoScale2d', 'toggleSpikelines', 'hoverCompareCartesian'], 'displaylogo': 0 },

            figure = go.Figure (
                data = [ go.Scatter(
                        x = sent_date_count['sent_date'],
                        y = sent_date_count['count'],
                        mode = 'lines+markers',
                        name = 'Sent',
                        marker = {'color': 'rgb(255, 165, 30)'},
                        line = {'width': 2}
                        ),
                        go.Scatter(
                                x = in_date_count['sent_date'],
                                y = in_date_count['count'],
                                mode = 'lines+markers',
                                name = 'Received',
                                marker = {'color': 'rgb(48, 134, 217)'},
                                line = {'width': 2}
                        ) ],

                layout = {
                    'title': {'text': 'Number of Incoming / Outgoing Emails'},
                    'legend': {'x':0, 'y':1.17, 'orientation':'h'}
                     }
                )

        )],
    className="ten columns offset-by-one"),

##############################################################################################
# Close Row 1: Graphs
    ],
     className="row"
    ),

##############################################################################################
# Row 1.2: Graphs
    html.Div([

##############################################################################################
# Row 1.2, Column 2: Counts per weekday
    html.Div([
        dcc.Graph(
            id='graph-counts-weekday',
            config={'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'select2d', 'lasso2d', 'hoverClosestCartesian', 'sendDataToCloud', 'autoScale2d', 'toggleSpikelines', 'hoverCompareCartesian'], 'displaylogo': 0 },

            figure = go.Figure (
                data = [ go.Bar(
                            x = sent_day_mean['day_of_week'],
                            y = sent_day_mean['body'],
                            #text = sent_day_mean['body'],
                            textposition = 'inside',
                            name = 'Sent',
                            marker = {'color': 'rgb(255, 165, 30)'}
                        ),
                        go.Bar(
                            x = in_day_mean['day_of_week'],
                            y = in_day_mean['body'],
                            #text = in_day_mean['body'],
                            textposition = 'inside',
                            name = 'Received',
                            marker = {'color': 'rgb(48, 134, 217)'}
                        ) ],

                layout = go.Layout(
                    title = 'Average Number of Emails per Weekday',
                    legend=dict(x=0, y=1.17, orientation="h"),
                    xaxis = dict(tickangle = -40)
                    )
                )

        )],
    className="six columns"),



##############################################################################################
# Row 1.2, Column 1: Counts by hour
    html.Div([
        dcc.Graph(
            id='graph-hour-line',
            config={'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'select2d', 'lasso2d', 'hoverClosestCartesian', 'sendDataToCloud', 'autoScale2d', 'toggleSpikelines', 'hoverCompareCartesian'], 'displaylogo': 0 },

            figure = go.Figure (
                    data = [ go.Scatter(
                                x = out_hour_mean['sent_hour'],
                                y = out_hour_mean['body'],
                                mode = 'lines+markers',
                                name = 'Out',
                                line = dict(
                                    color = ('rgb(255, 165, 30)') )
                                ),
                            go.Scatter(
                                    x = in_hour_mean['sent_hour'],
                                    y = in_hour_mean['body'],
                                    mode = 'lines+markers',
                                    name = 'In',
                                    line = dict(
                                        color = ('rgb(48, 134, 217)') )
                                    ) ],

                layout = go.Layout(
                    title ='Average Number of In/Out Emails by Hour',
                    legend=dict(x=0, y=1.17, orientation="h"),
                    shapes = [{
                        'type': 'rect',
                        'xref': 'x',
                        # y-reference is assigned to the plot paper [0,1]
                        'yref': 'paper',
                        'x0': 9,
                        'y0': 0,
                        'x1': 17,
                        'y1': 1,
                        'fillcolor': '#d3d3d3',
                        'opacity': 0.2,
                        'line': {'width': 0}
                        }],
                    annotations = [{
                        'x': '13',
                        'y': '0',
                        'xref': 'x',
                        'yref': 'paper',
                        'text': 'Working Hours 9-17',
                        'showarrow': False
                        }]
                    )
                )

        )],
    className="six columns"),

##############################################################################################
# Close Row 1.2: Graphs
    ],
     className="row"
    ),

html.Div(style = {"height":"20px"}),
##############################################################################################
# DIVIDER
    html.Div([
        html.Div('Folders by Number of Emails per Folder', style={"color":"rgb(48, 134, 217)", "font-size":"25px", "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif", "display":"table-cell", "text-align":"center", "vertical-align": "middle","margin":"20px 0 0 0"}, className='twelve columns')
        ],
        style = {"background-color":"#F6F6F6", "height": "80px", "margin":"-10px", "text-align":"center"},
        className='row'
        ),

html.Div(style = {"height":"15px"}),
##############################################################################################
# Row 2: Filters
    html.Div([

##############################################################################################
# Row 2, Column 1: Slider
    html.Div([
    dcc.RangeSlider(
        id='slider',
        marks={0: '0', 1: '10', 2: '100', 3: '1K'},
        min=0,
        max=3,
        value=[0, 3],
        step = 0.01,
        updatemode = 'drag',
        allowCross=False
    )],
    className="eight columns offset-by-two", style = {"text-align":"left"}),


##############################################################################################
# Close Row 2: Filters
    ],
     style = {"margin":"0 0 20px 0"},
     className="row"
    ),

##############################################################################################
# Row 3: Graph
    html.Div([

##############################################################################################
# Row 3, Column 1: Bars
    html.Div([
        dcc.Graph(
            id='graph-bars',
            #figure={ },
            config={'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'select2d', 'lasso2d', 'hoverClosestCartesian', 'sendDataToCloud', 'autoScale2d', 'toggleSpikelines', 'hoverCompareCartesian'], 'displaylogo': 0 }
        )],
    className="ten columns offset-by-one")
##############################################################################################
# Close Row 3: Graphs
    ],
    className="row"
    ),
html.Div(style = {"height":"15px"}),
##############################################################################################
# DIVIDER
    html.Div([
        html.Div('Who Sends Emails vs Who Gets the Emails', style={"color":"rgb(48, 134, 217)", "font-size":"25px", "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif", "display":"table-cell", "text-align":"center", "vertical-align": "middle","margin":"20px 0 0 0"}, className='twelve columns')
        ],
        style = {"background-color":"#F6F6F6", "height": "80px", "margin":"-10px", "text-align":"center"},
        className='row'
        ),

html.Div(style = {"height":"15px"}),

##############################################################################################
# Row 4: Filters
    html.Div([

##############################################################################################
# Row 4, Column 1: Group
    html.Div([
    html.Label('Group', style={"color":"#1A5336"}),
    dcc.Dropdown(
        id='group-dropdown',
        options= [{'label': 'All', 'value': 'All'}] + groups_filter,
        value = 'All',
        clearable=False,
        style = {"background-color":'rgb(248, 248, 248)'}
        #multi=True
    )],
    className="four columns offset-by-four", style = {"text-align":"left"}),


##############################################################################################
# Close Row 4: Filters
    ],
    className="row"
    ),

##############################################################################################
# Row 5: Graph
    html.Div([

##############################################################################################
# Row 5, Column 1: Scatter
    html.Div([
        dcc.Graph(
            id='graph-scatter',
            #figure={ },
            config = {'modeBarButtonsToRemove': ['toImage', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'sendDataToCloud', 'autoScale2d', 'toggleSpikelines', 'hoverCompareCartesian'], 'displaylogo': 0 }
        )],
    className="ten columns offset-by-one")
##############################################################################################
# Close Row 5: Graphs
    ],
    className="row"
    ),

html.Div(style = {"height":"15px"}),

##############################################################################################
# DIVIDER
    html.Div([
        html.Div('Top 20 Senders (Incoming & Outgoing emails)', style={"color":"rgb(48, 134, 217)", "font-size":"25px", "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif", "display":"table-cell", "text-align":"center", "vertical-align": "middle","margin":"20px 0 0 0"}, className='twelve columns')
        ],
        style = {"background-color":"#F6F6F6", "height": "80px", "margin":"-10px", "text-align":"center"},
        className='row'
        ),

html.Div(style = {"height":"15px"}),

##############################################################################################
# Row 10: Table Senders
    html.Div([

##############################################################################################
    html.Div([
            dash_table.DataTable(
                id='top-users',
                columns = [{"name": i, "id": i} for i in df_senders_20],
                data = df_senders_20.to_dict("rows"),
                style_cell={'textAlign': 'center', 'font-size': 16, "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif"},
                editable=False,
                filtering=False,
                sorting=True,
                sorting_type="single",
            )],
        className="ten columns offset-by-one"),
##############################################################################################
# Close Row 10: Table Senders
    ],
    className="row"
    ),

html.Div(style = {"height":"15px"}),
##############################################################################################
# DIVIDER
    html.Div([
        html.Div('Top 20 Groups (Incoming emails)', style={"color":"rgb(48, 134, 217)", "font-size":"25px", "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif", "display":"table-cell", "text-align":"center", "vertical-align": "middle","margin":"20px 0 0 0"}, className='twelve columns')
        ],
        style = {"background-color":"#F6F6F6", "height": "80px", "margin":"-10px", "text-align":"center"},
        className='row'
        ),

html.Div(style = {"height":"15px"}),

##############################################################################################
# Row 11: Table Groups
    html.Div([


##############################################################################################
    html.Div([
            dash_table.DataTable(
                id='top-groups',
                columns = [{"name": i, "id": i} for i in df_senders_20_group],
                data = df_senders_20_group.to_dict("rows"),
                style_cell={'textAlign': 'center', 'font-size': 16, "font-family": "'Webly Sleek Light',Helvetica-,droid sans,sans-serif"},
                editable=False,
                filtering=False,
                sorting=True,
                sorting_type="single",
            )],
        className="ten columns offset-by-one")
##############################################################################################
# Close Row 11: Table Groups
    ],
    className="row"
    ),

##############################################################################################
# CloseLayout
])

##############################################################################################
# Graph 1
@app.callback(
    Output('graph-daily-line', 'figure'),
    [Input('none', 'value')]
)
def update_graph1(value):
    data = [ go.Scatter(
            x = sent_date_count['sent_date'],
            y = sent_date_count['count'],
            mode = 'lines+markers',
            name = 'Sent',
            marker = {'color': 'rgb(255, 165, 30)'},
            line = {'width': 2}
            ),
            go.Scatter(
                    x = in_date_count['sent_date'],
                    y = in_date_count['count'],
                    mode = 'lines+markers',
                    name = 'Received',
                    marker = {'color': 'rgb(48, 134, 217)'},
                    line = {'width': 2}
            ) ]

    annotations = [dict(
            x=pd.Timestamp(year=2000, month=12, day=13),
            y=52,
            xref='x',
            yref='y',
            text='J. Skilling was announced as a CEO',
            showarrow=True,
            arrowhead=7,
            ax=130,
            ay=0
        ),
        dict(
            x=pd.Timestamp(year=2001, month=5, day=17),
            y=13,
            xref='x',
            yref='y',
            text='Secret meeting with Schwarzenegger in CA',
            showarrow=True,
            arrowhead=7,
            ax=-260,
            ay=-60
        ),
        dict(
            x=pd.Timestamp(year=2001, month=8, day=14),
            y=15,
            xref='x',
            yref='y',
            text='J. Skilling resignation',
            showarrow=True,
            arrowhead=7,
            ax=80,
            ay=-80
        )]

    layout = {
        'title': 'Number of Incoming / Outgoing Emails',
        'legend': dict(x=0, y=1.17, orientation="h"),
        'hovermode': 'closest',
        'annotations': annotations,
        }

    return {'data': data, 'layout': layout}

##############################################################################################
# Graph 2
@app.callback(
    Output('graph-counts-weekday', 'figure'),
    [Input('none', 'value')]
)
def update_graph2(value):
    data = [ go.Bar(
                x = sent_day_mean['day_of_week'],
                y = sent_day_mean['body'],
                text = sent_day_mean['body'],
                textposition = 'inside',
                name = 'Sent',
                marker = {'color': 'rgb(255, 165, 30)'}
            ),
            go.Bar(
                x = in_day_mean['day_of_week'],
                y = in_day_mean['body'],
                text = in_day_mean['body'],
                textposition = 'inside',
                name = 'Received',
                marker = {'color': 'rgb(48, 134, 217)'}
            ) ]

    layout = {
            'title': 'Average Number of Emails per Weekday',
            'legend': dict(x=0, y=1.17, orientation="h"),
            'xaxis' : {'tickangle':'-40'}
            }

    return {'data': data, 'layout': layout}

##############################################################################################
# Graph 3
@app.callback(
    Output('graph-hour-line', 'figure'),
    [Input('none', 'value')]
)
def update_graph3(value):
    data = [ go.Scatter(
                x = out_hour_mean['sent_hour'],
                y = out_hour_mean['body'],
                mode = 'lines+markers',
                name = 'Out',
                line = dict(
                    color = ('rgb(255, 165, 30)') )
                ),

            go.Scatter(
                    x = in_hour_mean['sent_hour'],
                    y = in_hour_mean['body'],
                    mode = 'lines+markers',
                    name = 'In',
                    line = dict(
                        color = ('rgb(48, 134, 217)') )
                    )  ]

    annotations = [{
            'x': 13,
            'y': 1.08,
            'xref': 'x',
            'yref': 'paper',
            'text': 'Working Hours 9-17',
            'showarrow': False
    }]

    shapes = [{
            'type': 'rect',
            'xref': 'x',
            # y-reference is assigned to the plot paper [0,1]
            'yref': 'paper',
            'x0': 9,
            'y0': 0,
            'x1': 17,
            'y1': 1,
            'fillcolor': '#d3d3d3',
            'opacity': 0.2,
            'line': {'width': 0}
            }]

    layout = {
        'title': 'Average Number of In/Out Emails by Hour',
        'annotations': annotations,
        'shapes': shapes,
        'legend': dict(x=0, y=1.17, orientation="h")
        }



    return {'data': data, 'layout': layout}

##############################################################################################
# Bar graph
@app.callback(
    Output('graph-bars', 'figure'),
    [Input('slider', 'value')]
    )
def update_bars(value):
    transformed_value = [transform_value(v) for v in value]
    min_emails = round(transformed_value[0])
    max_emails = round(transformed_value[1])
    num_folders = len(folders_list[(folders_list['count'] >= transformed_value[0] ) & (folders_list['count'] <= transformed_value[1] ) ])
    data = [go.Bar(
                x = folders_list[(folders_list['count'] >= transformed_value[0] ) & (folders_list['count'] <= transformed_value[1] ) ]['count'].values,
                y = folders_list[(folders_list['count'] >= transformed_value[0] ) & (folders_list['count'] <= transformed_value[1] ) ]['folder'].values,
                marker = dict(color = 'rgb(48, 134, 217)'),
                text = folders_list[(folders_list['count'] >= transformed_value[0] ) & (folders_list['count'] <= transformed_value[1] ) ]['count'].values,
                textposition = 'inside',
                #name = '# of ' + legend_dict[bar_status],
                hoverinfo = 'y+x',
                textfont = dict(size=14),
                showlegend=False,
                orientation = 'h'
                )
            ]

    graph_title =  str(num_folders) + ' folders with ' + str(min_emails) + ' to ' + str(max_emails) + ' emails'
    layout = {
        'title': graph_title,
        'margin': {'l':500},
    }

    return {'data': data, 'layout': layout}

##############################################################################################
# Scatter graph: In vs Out
@app.callback(
    Output('graph-scatter', 'figure'),
    [Input('group-dropdown', 'value')]
    )
def update_scatter(value_group):
    color_empty = 'rgba(48, 134, 217, 0)'
    color_full = 'rgb(48, 134, 217)'
    color_accent = 'rgb(255, 165, 30)'

    if (value_group != 'All'):
        df_group = df_to_from[df_to_from['group'] == value_group]
        df_other = df_to_from[df_to_from['group'] != value_group]
        data = [go.Scatter(
                        x = df_other['IN'],
                        y = df_other['OUT'],
                        mode = 'markers',
                        text = df_other['sender'],
                        marker = dict(size = 14, color = color_empty, line = dict(color = 'rgb(64, 65, 63)', width = 1)),
                        name = ''
                    ),
                go.Scatter(
                        x = df_group['IN'],
                        y = df_group['OUT'],
                        mode = 'markers',
                        text = df_group['sender'],
                        marker = dict(size = 14, color = color_full, line = dict(color = 'rgb(64, 65, 63)', width = 1)),
                        name = ''
                    ),
                ]

    else:
        df_other = df_to_from
        data = [go.Scatter(
                        x = df_other['IN'],
                        y = df_other['OUT'],
                        mode = 'markers',
                        text = df_other['sender'],
                        marker = dict(size = 14, color = color_empty, line = dict(color = 'rgb(64, 65, 63)', width = 1)),
                        name = ''
                    )
                ]


    title_graph = 'Incoming vs Outgoing'
    layout = {
            'title': title_graph,
            'showlegend': False,
            'hovermode': 'closest',
            'xaxis': {'title': 'Incoming (From)'},
            'yaxis': {'title': 'Outgoing (To + CC)'},
            'shapes': [{'type': 'line',
                        'x0': 0,
                        'y0': 0,
                         'x1': 80,
                         'y1': 80,
                        'line': {
                            'color': 'rgb(192, 57, 43)',
                            'width': 2,
                            'dash': 'dot'}
                        }]
    }

    return {'data': data, 'layout': layout}

##############################################################################################
if __name__ == '__main__':
    app.run_server(debug=True)
