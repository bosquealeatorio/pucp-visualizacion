import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import numpy as np
# get relative data folder
from utils import *
import plotly.graph_objs as go


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

#Dataset de gráfico de terrememotos x magnitud a lo largo del tiempo
dataset = pd.read_csv(DATA_PATH.joinpath("earthquake_mag_animation.csv"))

years = [str(int(each)) for each in list(dataset.Year.unique())]  # str unique years

#Consecuencias de terremotos x magnitud
dataset_mag_no_nan = pd.read_csv(DATA_PATH.joinpath("df_with_magnitude_no_nan.csv"))

#Terremotos por magnitud a lo largo de cada década
dataset_mag_decade = pd.read_csv(DATA_PATH.joinpath("df_magnitude_decade.csv"))

#Terremotos por magnitud y profundidad
dataset_mag_depth = pd.read_csv(DATA_PATH.joinpath("df_magnitude_depth.csv"))

#Terremotos de mayor magnitud por año
dataset_highest_mag_year = pd.read_csv(DATA_PATH.joinpath("df_magnitude_max_year.csv"))

decadas_lst = [each  for each in list(dataset_mag_no_nan.Decade.unique())]
options_decades = []
options_decades.append({'label': 'TODOS', 'value': 'TODOS'})
options_decades.extend([{'label': x, 'value': x} for x in decadas_lst])
paises_lst = ["TODOS","PERU","MEXICO","INDONESIA","CHILE", "JAPAN" ,"TURKEY", "INDIA", "PHILIPPINES" ]
options_paises = []
options_paises.extend([{'label': x, 'value': x} for x in paises_lst])

def SetColor(x):
    if np.isnan(x):
        return "Na"
    else:
        x = int(x)
        if (x <= 5):
            return "Leve"
        elif (int(x) <= 7):
            return "Fuerte"
        elif (int(x) >= 7):
            return "Mayor"

#FIGURE GRÁFICO DE MAGNITUD VS DECADA
fig_mag_decade = px.bar(dataset_mag_decade, x="Decade", y="count",color="Mag Int")

#FIGURE GRÁFICO DE MAGNITUD VS PROFUNDIDAD
fig_mag_depth =go.Figure(data=go.Scatter(x=dataset_mag_depth['Focal Depth (km)'],
                                y=dataset_mag_depth['Mag'],
                                mode='markers',
                                marker_color=dataset_mag_depth['Mag'],
                                text=dataset_mag_depth['Label Name'],
                                      ))
#FIGURE GRÁFICO DE TERREMOTO DE MAYOR MAGNITUD POR AÑO
fig_highest_mag_year = px.line(dataset_highest_mag_year, x="Year", y="Mag",
	         hover_name="Location Name")

layout = html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [
                       # Row

                    html.Div(
                        [
                            html.Div(
                                [
                            html.Div([
                            html.H5('Terremotos por magnitud a lo largo del tiempo', style={"textAlign": "center"},className="subtitle padded"),
                            dcc.Graph(id='my-map', figure={},style={'width': '600', 'height': '500'}),
                            html.Div(id='slider-output'),
                            dcc.Slider(
                                id='year-slider',
                                min=dataset['Year'].min(),
                                max=dataset['Year'].max(),
                                value=dataset['Year'].min(),
                                marks={str(year): str(year) for year in dataset['Year'].unique()},
                                step=None
                            )
])
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
   # Row

                    html.Div(
                        [
                            html.Div(
                                [
                            html.Div([
                            html.H5('Terremotos por magnitud durante décadas', style={"textAlign": "center"},className="subtitle padded"),
                            dcc.Graph(id='graph-mag-decade', figure=fig_mag_decade,style={'width': '600', 'height': '500'}),

])
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    #Row
                    html.Div(
                        [
                            html.Div(
                                [
                            html.Div([
                            html.H5('Terremotos por magnitud y profundidad', style={"textAlign": "center"},className="subtitle padded"),
                            dcc.Graph(id='graph-mag-depth', figure=fig_mag_depth,style={'width': '600', 'height': '500'}),

                        ])
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div([
                                        html.H5('Terremoto de mayor magnitud por año', style={"textAlign": "center"},
                                                className="subtitle padded"),
                                        dcc.Graph(id='graph-highest-mag-year', figure=fig_highest_mag_year,
                                                  style={'width': '600', 'height': '500'}),

                                    ])
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                     html.Div(
                        [
                            html.H5('Consecuencias de terremotos por magnitud', style={"textAlign": "center"},
                                    className="subtitle padded"),
                            html.Div([
                                html.Pre(children="Década", style={"fontSize": "150%"}),
                                dcc.Dropdown(
                                    id='decade-dropdown', value='DEBIT', clearable=False,
                                    persistence=True, persistence_type='session',
                                    options=options_decades
                                )
                            ], className='six columns'),

                            html.Div([
                                html.Pre(children="País", style={"fontSize": "150%"}),
                                dcc.Dropdown(
                                    id='country-dropdown', value='India', clearable=False,
                                    persistence=True, persistence_type='local',
                                    options=options_paises
                                )
                            ], className='six columns'),

                        ],
                        className="row ",
                    ),


                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Relación Magnitud vs Pérdidas humanas"], className="subtitle padded"
                                    ),
                                    dcc.Graph(
                                        id="graph-mag-human-losses",
                                        figure = {},
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Relación Magnitud vs Pérdidas económicas",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-mag-economical-losses",
                                        figure={},
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Relación Magnitud vs Personas perdidas"], className="subtitle padded"
                                    ),
                                    dcc.Graph(
                                        id="graph-mag-human-missing",
                                        figure={},
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Relación Magnitud vs Personas heridas",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-mag-human-injured",
                                        figure={},
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Relación Magnitud vs Casas dañadas"], className="subtitle padded"
                                    ),
                                    dcc.Graph(
                                        id="graph-mag-damaged-houses",
                                        figure={},
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Relación Magnitud vs Casas destruidas",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-mag-destroyed-houses",
                                        figure={},
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),

                ],

                className="sub_page",
            ),
        ],
        className="page",
    )




@app.callback(
    Output(component_id='slider-output', component_property='children'),
    [Input('year-slider', 'value'),
     ]
)
def display_slider_value(selected_year):
    return 'Año : ' + str(selected_year)


@app.callback(
    Output(component_id='my-map', component_property='figure'),
    [Input('year-slider', 'value'),
     ]
)
def update_figure(selected_year):
    filtered_df = dataset[dataset.Year == int(selected_year)]
    layout={}
    layout['geo'] = dict(showframe=False, showland=True, showcoastlines=True, showcountries=True,
                                   countrywidth=1,
                                   landcolor='rgb(217, 217, 217)',
                                   subunitwidth=1,
                                   showlakes=True,
                                   lakecolor='rgb(255, 255, 255)',
                       )
    layout['hovermode'] = 'closest'

    fig = px.scatter_geo(filtered_df,
                         lon=filtered_df['Longitude'],
                         lat=filtered_df['Latitude'],
                         hover_name=filtered_df['Label Name'],
                         color= list(map(SetColor, filtered_df['Mag'])),
                         )
    fig.update_layout(layout)
    return fig



@app.callback(
Output(component_id='graph-mag-human-losses', component_property='figure'),
    [Input('decade-dropdown', 'value'),
    Input('country-dropdown', 'value'),
     ]
)
def update_figure(selected_decade,selected_country):
    dataset_fig = dataset_mag_no_nan.copy()
    if selected_country != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Country'] == selected_country]
    if selected_decade != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Decade'] == int(selected_decade)]
    avg_death_magnitude =  dataset_fig.get(['Mag Int', 'Total Deaths']).groupby('Mag Int', as_index = False).mean()
    return px.line(avg_death_magnitude, x="Mag Int", y="Total Deaths",
                  )

@app.callback(
Output(component_id='graph-mag-economical-losses', component_property='figure'),
    [Input('decade-dropdown', 'value'),
    Input('country-dropdown', 'value'),
     ]
)
def update_mag_economical_losses_figure(selected_decade, selected_country):
    dataset_fig = dataset_mag_no_nan[dataset_mag_no_nan['Damage ($Mil)'].notnull()].copy()

    if selected_country != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Country'] == selected_country]
    if selected_decade != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Decade'] == int(selected_decade)]
    avg_damage_mil_magnitude = dataset_fig.get(
        ['Mag Int', 'Damage ($Mil)']).groupby('Mag Int', as_index=False).mean()

    return px.line(avg_damage_mil_magnitude, x="Mag Int", y="Damage ($Mil)",
                  )



@app.callback(
Output(component_id='graph-mag-human-missing', component_property='figure'),
    [Input('decade-dropdown', 'value'),
    Input('country-dropdown', 'value'),
     ]
)
def update_mag_human_missing_figure(selected_decade, selected_country):
    dataset_fig = dataset_mag_no_nan[dataset_mag_no_nan['Total Missing'].notnull()].copy()

    if selected_country != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Country'] == selected_country]
    if selected_decade != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Decade'] == int(selected_decade)]
    avg_missing_magnitude = dataset_fig.\
        get(['Mag Int', 'Total Missing']).groupby('Mag Int', as_index = False).mean()


    return  px.line(avg_missing_magnitude, x="Mag Int", y="Total Missing",
                  )



@app.callback(
Output(component_id='graph-mag-human-injured', component_property='figure'),
    [Input('decade-dropdown', 'value'),
    Input('country-dropdown', 'value'),
     ]
)
def update_mag_injuries_figure(selected_decade, selected_country):
    dataset_fig = dataset_mag_no_nan[dataset_mag_no_nan['Injuries'].notnull()].copy()

    if selected_country != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Country'] == selected_country]
    if selected_decade != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Decade'] == int(selected_decade)]
    avg_injuries_magnitude = dataset_fig.\
        get(['Mag Int', 'Injuries']).groupby('Mag Int', as_index = False).mean()
    return  px.line(avg_injuries_magnitude, x="Mag Int", y="Injuries",
                  )


@app.callback(
Output(component_id='graph-mag-damaged-houses', component_property='figure'),
    [Input('decade-dropdown', 'value'),
    Input('country-dropdown', 'value'),
     ]
)
def update_mag_damaged_houses_figure(selected_decade, selected_country):
    dataset_fig = dataset_mag_no_nan[dataset_mag_no_nan['Total Houses Damaged'].notnull()].copy()

    if selected_country != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Country'] == selected_country]
    if selected_decade != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Decade'] == int(selected_decade)]
    avg_damaged_houses_magnitude = dataset_fig.\
        get(['Mag Int', 'Total Houses Damaged']).groupby('Mag Int', as_index = False).mean()

    return px.line(avg_damaged_houses_magnitude, x="Mag Int", y="Total Houses Damaged",
                  )


@app.callback(
Output(component_id='graph-mag-destroyed-houses', component_property='figure'),
    [Input('decade-dropdown', 'value'),
    Input('country-dropdown', 'value'),
     ]
)
def update_mag_destroyed_houses_figure(selected_decade, selected_country):
    dataset_fig = dataset_mag_no_nan[dataset_mag_no_nan['Total Houses Destroyed'].notnull()].copy()

    if selected_country != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Country'] == selected_country]
    if selected_decade != 'TODOS':
        dataset_fig = dataset_fig[dataset_fig['Decade'] == int(selected_decade)]
    avg_destroyed_houses_magnitude = dataset_fig.get(['Mag Int', 'Total Houses Destroyed']).groupby(
        'Mag Int', as_index=False).mean()
    return px.line(avg_destroyed_houses_magnitude, x="Mag Int", y="Total Houses Destroyed",
            )



