import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table
import plotly.express as px

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

#Dataset de gráfico de terrememotos x magnitud a lo largo del tiempo
dataset = pd.read_csv(DATA_PATH.joinpath("earthquakes-prec.csv"))
px.set_mapbox_access_token("pk.eyJ1Ijoiam9zZWJsZXgiLCJhIjoiY2trZ3U3MjBpMDk1ODJxczdsY3o4eHlociJ9.aIZv4zfwVt3XcUCiIefVVQ")

#FIGURA DE DISTRIBUCIÓN DE TERRMOTOS
fig_distribucion = px.scatter_mapbox(dataset[dataset["Mag"].notna()], lat="Latitude", lon="Longitude", size="Mag",
                        color="Mag"
                        , color_continuous_scale=px.colors.cyclical.IceFire, size_max=12

                        , zoom=1)

#HEATMAP MEAN MAP

df=dataset.get(['ISO_APLHA','Country','Mag']).groupby(['ISO_APLHA','Country']).mean().reset_index()
fig_heatmap = px.choropleth(df, locations="ISO_APLHA",
                        color='Mag', # lifeExp is a column of gapminder
                        hover_name="Country", # column to add to hover information
                        color_continuous_scale=px.colors.cyclical.IceFire)

#HEATMAP SUM MAP
df2 = dataset.get(['ISO_APLHA', 'Country', 'Damage ($Mil)']).groupby(['ISO_APLHA', 'Country']).sum().reset_index()
fig_heatmap2 = px.choropleth(df2, locations="ISO_APLHA",
                    color='Damage ($Mil)',  # lifeExp is a column of gapminder
                    hover_name="Country",  # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Cividis_r)

#HEATMAP SUM MAP DEATHS
df3 = dataset.get(['ISO_APLHA', 'Country', 'Total Deaths']).groupby(['ISO_APLHA', 'Country']).sum().reset_index()
fig_heatmap3 = px.choropleth(df3, locations="ISO_APLHA",
                    color='Total Deaths',  # lifeExp is a column of gapminder
                    hover_name="Country",  # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Cividis_r)



def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div([
                                        html.H5('Distribución de terremotos',
                                                style={"textAlign": "center"}, className="subtitle padded"),
                                        dcc.Graph(id='my-map-1', figure=fig_distribucion, style={'width': '600', 'height': '500'}),

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
                                        html.H5('Mapa de calor por país de terremotos por magnitud promedio',
                                                style={"textAlign": "center"}, className="subtitle padded"),
                                         dcc.Graph(id='graph-heatmap', figure=fig_heatmap,
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
                            html.Div(
                                [
                                    html.Div([
                                        html.H5('Mapa de calor por país de terremotos con mayores perdidas económicas',
                                                style={"textAlign": "center"}, className="subtitle padded"),
                                        dcc.Graph(id='graph-heatmap', figure=fig_heatmap2,
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
                            html.Div(
                                [
                                    html.Div([
                                        html.H5('Mapa de calor por país de terremotos con mayores perdidas humanas',
                                                style={"textAlign": "center"}, className="subtitle padded"),
                                        dcc.Graph(id='graph-heatmap', figure=fig_heatmap3,
                                                  style={'width': '600', 'height': '500'}),

                                    ])
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
