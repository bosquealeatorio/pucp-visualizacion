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

#Dataset de gráfico de terrememotos vs tsunamis
df_mag_terrem_vs_tsu = pd.read_csv(DATA_PATH.joinpath("df_magnitud_terremotos_vs_tsunami.csv"))

#Dataset de gráfico de terrememotos vs terremotos con erupciones volcánicas
df_mag_terrem_vs_terrem_volc = pd.read_csv(DATA_PATH.joinpath("df_magnitud_terremotos_vs_terremoto_volcanes.csv"))
#Dataset de gráfico de terrememotos vs terremotos con erupciones volcánicas
df_mag_terrem_vs_terrem_sin_fenom = pd.read_csv(DATA_PATH.joinpath("df_magnitud_terremotos_vs_terremoto_sin_fenomenos.csv"))


#Dataset Comparacion Terremotos General
df_comp_terremotos = pd.read_csv(DATA_PATH.joinpath("df_comparacion_terremoto_general.csv"))

#Dataset Comparacion Tsunami General
df_comp_tsunami = pd.read_csv(DATA_PATH.joinpath("df_comparacion_tsunami.csv"))

#Dataset Comparacion Terremotos General
df_comp_erupciones = pd.read_csv(DATA_PATH.joinpath("df_comparacion_erupciones.csv"))




#FIGURE GRÁFICO DE MAGNITUD DE TERREMOTO VS TSUNAMI
fig_mag_terrem_vs_tsu = px.line(df_mag_terrem_vs_tsu, x='year', y="Mag")
fig_mag_terrem_vs_tsu.add_scatter(x=df_mag_terrem_vs_tsu['year'], y=df_mag_terrem_vs_tsu['tsu'],
                mode='lines',name="tsu")

#FIGURE GRÁFICO DE TERREMOTO VS TERREMOTO CON ERUPCIONES VOL.C

fig_terrem_vs_terrem_volc = px.line(df_mag_terrem_vs_terrem_volc, x='year', y="Mag")
fig_terrem_vs_terrem_volc.add_scatter(x=df_mag_terrem_vs_terrem_volc['year'], y=df_mag_terrem_vs_terrem_volc['vol'],
                mode='lines',name="vol")

#FIGURE GRÁFICO DE TERREMOTO VS TERREMOTO CON ERUPCIONES VOL.C

fig_terrem_vs_terrem_sin_fenom = px.line(df_mag_terrem_vs_terrem_sin_fenom, x='year', y="Mag")
fig_terrem_vs_terrem_sin_fenom .add_scatter(x=df_mag_terrem_vs_terrem_sin_fenom['year'], y=df_mag_terrem_vs_terrem_sin_fenom['no_vol_no_tsu'],
                mode='lines',name="no_vol_no_")

#FIGURE GRÁFICO COMP CANT TERREMOTO VS CANT TSUNAMI
years = [int(x) for x in df_comp_terremotos.index.tolist()]
fig_cant_terrem_vs_cant_tsu = px.line( x=years, y=df_comp_terremotos['count'])
fig_cant_terrem_vs_cant_tsu.add_scatter(x=years, y=df_comp_tsunami['count'], mode='lines',name="tsunami")

#FIGURE GRÁFICO COMP CANT TERREMOTO VS CANT ERUPCIONES
fig_cant_terrem_vs_cant_erup = px.line( x=years, y=df_comp_terremotos['count'])
fig_cant_terrem_vs_cant_erup.add_scatter(x=years, y=df_comp_erupciones['count'], mode='lines', name="eruption")






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
                            html.H5('Relación entre intensidad de terremotos e intensidad de terremotos con tsunamis a lo largo del tiempo ', style={"textAlign": "center"},className="subtitle padded"),
                            dcc.Graph(id='graph-mag-terr-tsu', figure=fig_mag_terrem_vs_tsu,style={'width': '600', 'height': '500'}),

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
                            html.H5('Relación entre intensidad de terremotos e intensidad de terremotos con erupciones volcanicas a lo largo del tiempo', style={"textAlign": "center"},className="subtitle padded"),
                            dcc.Graph(id='graph-mag-depth', figure=fig_terrem_vs_terrem_volc,style={'width': '600', 'height': '500'}),

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
                                        html.H5('Relación entre intensidad de terremotos e intensidad de terremotos sin otros fenómenos a lo largo del tiempo', style={"textAlign": "center"},
                                                className="subtitle padded"),
                                        dcc.Graph(id='graph-terrem-vs-terrem-no-fen', figure=fig_terrem_vs_terrem_sin_fenom,
                                                  style={'width': '600', 'height': '500'}),

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
                                        html.H5(
                                            'Relación entre intensidad de terremotos e intensidad de terremotos sin otros fenómenos a lo largo del tiempo',
                                            style={"textAlign": "center"},
                                            className="subtitle padded"),
                                        dcc.Graph(id='graph-terrem-vs-terrem-no-fen',
                                                  figure=fig_terrem_vs_terrem_sin_fenom,
                                                  style={'width': '600', 'height': '500'}),

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
                                        html.H5(
                                            'Terremotos vs Tsunamis',
                                            style={"textAlign": "center"},
                                            className="subtitle padded"),
                                        dcc.Graph(id='graph-cant-terrem-vs-cant-tsu',
                                                  figure=fig_cant_terrem_vs_cant_tsu,
                                                  style={'width': '600', 'height': '500'}),

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
                                        html.H5(
                                            'Terremotos vs Erupciones Volcánicas',
                                            style={"textAlign": "center"},
                                            className="subtitle padded"),
                                        dcc.Graph(id='graph-cant-terrem-vs-cant-erup',
                                                  figure=fig_cant_terrem_vs_cant_erup,
                                                  style={'width': '600', 'height': '500'}),

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



