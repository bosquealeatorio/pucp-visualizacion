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
dataset = pd.read_csv(DATA_PATH.joinpath("earthquake_mag_animation.csv"))


layout = html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [   html.H4('Visualización 3D de terremotos en base a la profundidad y su magnitud', style={"textAlign": "center"},className="subtitle padded"),
                    html.Div([
                        dcc.Graph(id='my-globe', figure={}),
                dcc.Slider(
                        id='year-slider',
                        min=dataset['Year'].min(),
                        max=dataset['Year'].max(),
                        value=dataset['Year'].min(),
                        marks={str(year): str(year) for year in dataset['Year'].unique()},
                        step=None
                    )
                    ]),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )

@app.callback(
    Output(component_id='my-globe', component_property='figure'),
    [Input('year-slider', 'value'),]
)
def update_figure_globe_depth(selected_year):
    # Import topography data
    # Select the area you want
    resolution = 0.8
    lon_area = [-180., 180.]
    lat_area = [-90., 90.]
    # Get mesh-shape topography data
    lon_topo, lat_topo, topo = Etopo(lon_area, lat_area, resolution)
    xs, ys, zs = mapping_map_to_sphere(lon_topo, lat_topo)

    Ctopo = [[0, 'rgb(0, 0, 70)'], [0.2, 'rgb(0,90,150)'],
             [0.4, 'rgb(150,180,230)'], [0.5, 'rgb(210,230,250)'],
             [0.50001, 'rgb(0,120,0)'], [0.57, 'rgb(220,180,130)'],
             [0.65, 'rgb(120,100,0)'], [0.75, 'rgb(80,70,0)'],
             [0.9, 'rgb(200,200,200)'], [1.0, 'rgb(255,255,255)']]
    cmin = -8000
    cmax = 8000

    topo_sphere = dict(type='surface',
                       x=xs,
                       y=ys,
                       z=zs,
                       colorscale=Ctopo,
                       surfacecolor=topo,
                       cmin=cmin,
                       cmax=cmax)

    noaxis = dict(showbackground=False,
                  showgrid=False,
                  showline=False,
                  showticklabels=False,
                  ticks='',
                  title='',
                  zeroline=False)

    titlecolor = 'white'
    bgcolor = 'black'

    layout = go.Layout(
        autosize=False, width=700 , height=600,
        titlefont=dict(family='Courier New', color=titlecolor),
        showlegend=False,
        scene=dict(
            xaxis=noaxis,
            yaxis=noaxis,
            zaxis=noaxis,
            aspectmode='manual',
            aspectratio=go.layout.scene.Aspectratio(
                x=1, y=1, z=1)),
        paper_bgcolor=bgcolor,
        plot_bgcolor=bgcolor)

    # Data selection
    data = dataset.copy()
    data = data[(data['Mag'].notnull()) & (data['Focal Depth (km)'].notnull())]
    # Change format to datetime for event date
    # data['np_DateTime']=pd.to_datetime(data['time'].str[:-2],format='%Y-%m-%dT%H:%M:%S')
    evlon = np.array(data['Longitude'])
    evlat = np.array(data['Latitude'])
    evDepth = np.array(data['Focal Depth (km)'])
    evMag = np.array(data['Mag'])

    # Convert to spherical coordinates
    xs_ev_org, ys_ev_org, zs_ev_org = mapping_map_to_sphere(evlon, evlat)

    cbar = 'jet_r'
    Cscale_EQ = MlibCscale_to_Plotly(cbar)

    # Create three-dimensional effect
    ratio = 1. - evDepth * 2e-4
    xs_ev = xs_ev_org * ratio
    ys_ev = ys_ev_org * ratio
    zs_ev = zs_ev_org * ratio

    ratio = 1.15 - evDepth * 2e-4
    xs_ev_up = xs_ev_org * ratio
    ys_ev_up = ys_ev_org * ratio
    zs_ev_up = zs_ev_org * ratio

    # Get list of of coastline, country, and state lon/lat
    cc_lons, cc_lats = get_coastline_traces()
    country_lons, country_lats = get_country_traces()

    # concatenate the lon/lat for coastlines and country boundaries:
    lons = cc_lons + [None] + country_lons
    lats = cc_lats + [None] + country_lats

    xs_bd, ys_bd, zs_bd = mapping_map_to_sphere(lons, lats, radius=1.01)  # here the radius is slightly greater than 1
    # to ensure lines visibility; otherwise (with radius=1)
    # some lines are hidden by contours colors

    boundaries = dict(type='scatter3d',
                      x=xs_bd,
                      y=ys_bd,
                      z=zs_bd,
                      mode='lines',
                      line=dict(color='gray', width=4)
                      )

    depmax = 700.
    depmin = 0.
    depbin = 50.

    cmin = depmin
    cmax = depmax
    cbin = depbin

    seis_3D_depth_up = go.Scatter3d(x=xs_ev_up,
                                    y=ys_ev_up,
                                    z=zs_ev_up,
                                    mode='markers',
                                    #name='measured',
                                    #hover_data=data['Label Name'],
                                    marker=dict(
                                        size=1. * evMag,
                                        cmax=cmax,
                                        cmin=cmin,
                                        colorbar=dict(
                                            title='Source Depth',
                                            titleside='right',
                                            titlefont=dict(size=16,
                                                           color=titlecolor,
                                                           family='Courier New'),
                                            tickmode='array',
                                            ticks='outside',
                                            ticktext=list(np.arange(cmin, cmax + cbin, cbin)),
                                            tickvals=list(np.arange(cmin, cmax + cbin, cbin)),
                                            tickcolor=titlecolor,
                                            tickfont=dict(size=14, color=titlecolor,
                                                          family='Courier New')
                                        ),
                                        ### choose color option
                                        color=evDepth,
                                        ### choose color option
                                        colorscale=Cscale_EQ,
                                        showscale=True,
                                        opacity=1.),
                                    hovertext=data['Label Name']#, hover_data=["Mag", "pop"]
                                    #hoverinfo='skip'
                                    )

    plot_data = [topo_sphere, seis_3D_depth_up]
    fig = go.Figure(data=plot_data, layout=layout)

    return fig
