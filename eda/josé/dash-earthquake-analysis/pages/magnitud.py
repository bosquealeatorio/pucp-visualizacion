import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import numpy as np
# get relative data folder
from utils import Header

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
dfg = pd.read_csv(DATA_PATH.joinpath("opsales.csv"))
dataset = pd.read_csv(DATA_PATH.joinpath("earthquake_mag_animation.csv"))
years = [str(int(each)) for each in list(dataset.Year.unique())]  # str unique years
df = px.data.gapminder().query("country=='Canada'")


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


layout = html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [
                    # Row
                    # html.Div(
                    #     [
                    #         html.Div(
                    #             [
                    #                 html.H6(
                    #                     ["Current Prices"], className="subtitle padded"
                    #                 ),
                    #             ],
                    #             className="six columns",
                    #         ),
                    #         html.Div(
                    #             [
                    #                 html.H6(
                    #                     ["Historical Prices"],
                    #                     className="subtitle padded",
                    #                 ),
                    #             ],
                    #             className="six columns",
                    #         ),
                    #     ],
                    #     className="row ",
                    # ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
    html.Div([
    html.H4('Terremotos por magnitud a lo largo del tiempo', style={"textAlign": "center"},className="subtitle padded"),
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