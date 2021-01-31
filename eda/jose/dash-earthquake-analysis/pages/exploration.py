import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from dash.dependencies import Input, Output
from app import app

from utils import Header

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

#reading source dataframes
earthquakes = pd.read_csv(DATA_PATH.joinpath("earthquakes.tsv"), sep = '\t')
earthquakes_counts = pd.read_csv(DATA_PATH.joinpath("earthquakes_counts.csv"))

def get_earthquake_counts(earthquakes, year_min = 1900, year_max = 2020):
    earthquakes = earthquakes.query('Year > @year_min & Year < @year_max')
    cuentas = earthquakes.rename(columns={'Location Name': 'Cantidad'}) \
                        .get(['Country', 'Cantidad']) \
                        .groupby('Country', as_index=False) \
                        .count() \
                        .sort_values(by='Cantidad', ascending=False)

    return cuentas.head(10)

def get_tsu_comparison(earthquakes, column, year_min=1900, year_max=2020):
    earthquakes = earthquakes.query('Year > @year_min & Year < @year_max')
    tsu = earthquakes.query('Tsu.notnull()')

    comparison_tsu = earthquakes.get(['Year', column]).groupby('Year').mean()
    comparison_tsu['tsu'] = tsu.get(['Year', column]).groupby('Year').mean()
    years = comparison_tsu.index.astype('str').tolist()

    return years, comparison_tsu[column].astype('str').values.tolist(), comparison_tsu['tsu'].astype(
        'str').values.tolist()

years, no_tsu, tsu = get_tsu_comparison(earthquakes, 'Mag')
df_counts = get_earthquake_counts(earthquakes_counts)


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # years slider
                   html.H5(
                        "Paises con mayor número de terremotos ",
                        className="subtitle padded",
                        style={"textAlign": "center"}
                    ),
                    html.Div([
                        html.H6(id='output-container-range-slider'),
                        dcc.RangeSlider(
                            id='my-range-slider',
                            min=1900,
                            max=earthquakes['Year'].max(),
                            step=1,
                            value=[1900, 2010]
                        ),
                    ]),

                    # barplot of earthquakes over time period
                    html.Div([
                        dcc.Graph(id='the_barplot',)
                    ]),

                    # tsunamis and earthquake magnitude
                    html.Div(
                        [
                            html.H5(
                                "Influencia de magnitudes en tsunamis",
                                style={"textAlign": "center"},
                                className="subtitle padded",
                            ),
                            dcc.Graph(
                                id="graph-2",
                                figure={
                                    "data": [
                                        go.Scatter(
                                            x= years,
                                            y= no_tsu,
                                            line={"color": "#20639b"},
                                            mode="lines",
                                            name="No Tsunami",
                                        ),
                                        go.Scatter(
                                            x=years,
                                            y=tsu,
                                            line={"color": "#97151c"},
                                            mode="lines",
                                            name="tsunami",
                                        )
                                    ],
                                    "layout": go.Layout(
                                        autosize=True,
                                        title="",
                                        font={"family": "Raleway", "size": 10},
                                        height=400,
                                        hovermode="closest",
                                        legend={
                                            "x": -0.0277108433735,
                                            "y": -0.142606516291,
                                            "orientation": "h",
                                        },
                                        margin={
                                            "r": 20,
                                            "t": 20,
                                            "b": 20,
                                            "l": 50,
                                        },
                                        showlegend=True,
                                        xaxis={
                                            "autorange": True,
                                            "linecolor": "rgb(0, 0, 0)",
                                            "linewidth": 1,
                                            "range": [2008, 2018],
                                            "showgrid": False,
                                            "showline": True,
                                            "title": "",
                                            "type": "linear",
                                        },
                                        yaxis={
                                            "autorange": True,
                                            "gridcolor": "rgba(127, 127, 127, 0.2)",
                                            "mirror": False,
                                            "nticks": 4,
                                            "showgrid": True,
                                            "showline": True,
                                            "ticklen": 10,
                                            "ticks": "outside",
                                            "title": "$",
                                            "type": "linear",
                                            "zeroline": False,
                                            "zerolinewidth": 4,
                                        },
                                    ),
                                },
                                config={"displayModeBar": False},
                            ),

                        ],
                        className="row ",
                    ),

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )



@app.callback(
    #Output('output-container-range-slider', 'children'),
    [Output('the_barplot', 'figure'), Output('output-container-range-slider', 'children')],
    [Input('my-range-slider', 'value')])
def update_range(value):

    years, no_tsu, tsu = get_tsu_comparison(earthquakes, 'Mag')
    df_counts = get_earthquake_counts(earthquakes_counts, value[0], value[1])
    df_counts = df_counts.rename(columns = {'Cantidad': 'Quantity'})

    fig = px.bar(df_counts, x='Country', y='Quantity')
    fig.update_traces()

    return (fig, f'Rango de inicio: {value[0]}           Rango de Fin: {value[1]}')


