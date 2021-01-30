import dash_html_components as html
import dash_core_components as dcc
import pathlib
# Create color bar in Matplotlib
import matplotlib
from matplotlib import cm

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [html.H5("Análisis de Terremotos")],
                        className="seven columns main-title",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/dash-earthquake-analysis/overview",
                className="tab first",
            ),
            dcc.Link(
                "Magnitud",
                href="/dash-earthquake-analysis/magnitud",
                className="tab",
            ),
            dcc.Link(
                "Visualización 3D",
                href="/dash-earthquake-analysis/visualizacion-3d",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


import numpy as np
from netCDF4 import Dataset


def Etopo(lon_area, lat_area, resolution):
    ### Input
    # resolution: resolution of topography for both of longitude and latitude [deg]
    # (Original resolution is 0.0167 deg)
    # lon_area and lat_area: the region of the map which you want like [100, 130], [20, 25]
    ###
    ### Output
    # Mesh type longitude, latitude, and topography data
    ###

    # Read NetCDF data
    #data = Dataset(DATA_PATH.joinpath("ETOPO1_Ice_g_gdal.grd"), "r")
    data = Dataset("D:/DIPLOMADO_IA/DATA_VISUALIZATION/TRABAJO_FINAL/repo/pucp-visualizacion/eda/jose/dash-earthquake-analysis/data/ETOPO1_Ice_g_gdal.grd", "r")

    # Get data
    lon_range = data.variables['x_range'][:]
    lat_range = data.variables['y_range'][:]
    topo_range = data.variables['z_range'][:]
    spacing = data.variables['spacing'][:]
    dimension = data.variables['dimension'][:]
    z = data.variables['z'][:]
    lon_num = dimension[0]
    lat_num = dimension[1]

    # Prepare array
    lon_input = np.zeros(lon_num);
    lat_input = np.zeros(lat_num)
    for i in range(lon_num):
        lon_input[i] = lon_range[0] + i * spacing[0]
    for i in range(lat_num):
        lat_input[i] = lat_range[0] + i * spacing[1]

    # Create 2D array
    lon, lat = np.meshgrid(lon_input, lat_input)

    # Convert 2D array from 1D array for z value
    topo = np.reshape(z, (lat_num, lon_num))

    # Skip the data for resolution
    if ((resolution < spacing[0]) | (resolution < spacing[1])):
        print('Set the highest resolution')
    else:
        skip = int(resolution / spacing[0])
        lon = lon[::skip, ::skip]
        lat = lat[::skip, ::skip]
        topo = topo[::skip, ::skip]

    topo = topo[::-1]

    # Select the range of map
    range1 = np.where((lon >= lon_area[0]) & (lon <= lon_area[1]))
    lon = lon[range1];
    lat = lat[range1];
    topo = topo[range1]
    range2 = np.where((lat >= lat_area[0]) & (lat <= lat_area[1]))
    lon = lon[range2];
    lat = lat[range2];
    topo = topo[range2]

    # Convert 2D again
    lon_num = len(np.unique(lon))
    lat_num = len(np.unique(lat))
    lon = np.reshape(lon, (lat_num, lon_num))
    lat = np.reshape(lat, (lat_num, lon_num))
    topo = np.reshape(topo, (lat_num, lon_num))

    return lon, lat, topo


def degree2radians(degree):
    # convert degrees to radians
    return degree * np.pi / 180


def mapping_map_to_sphere(lon, lat, radius=1):
    # this function maps the points of coords (lon, lat) to points onto the sphere of radius radius
    lon = np.array(lon, dtype=np.float64)
    lat = np.array(lat, dtype=np.float64)
    lon = degree2radians(lon)
    lat = degree2radians(lat)
    xs = radius * np.cos(lon) * np.cos(lat)
    ys = radius * np.sin(lon) * np.cos(lat)
    zs = radius * np.sin(lat)
    return xs, ys, zs



def matplotlib_to_plotly(cmap, pl_entries):
    h = 1.0 / (pl_entries - 1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k * h)[:3]) * 255))
        pl_colorscale.append([k * h, 'rgb' + str((C[0], C[1], C[2]))])

    return pl_colorscale


def MlibCscale_to_Plotly(cbar):
    cmap = matplotlib.cm.get_cmap(cbar)
    rgb = []
    norm = matplotlib.colors.Normalize(vmin=0, vmax=255)

    for i in range(0, 255):
        k = matplotlib.colors.colorConverter.to_rgb(cmap(norm(i)))
        rgb.append(k)

    Cscale = matplotlib_to_plotly(cmap, 255)

    return Cscale


# Draw coast line
# Reference: https://plot.ly/~Dreamshot/9152

# Make shortcut to Basemap object,
# not specifying projection type for this example
#from mpl_toolkits.basemap import Basemap

#m = Basemap(resolution='i')


# Functions converting coastline/country polygons to lon/lat traces
def polygons_to_traces(poly_paths, N_poly):
    '''
    pos arg 1. (poly_paths): paths to polygons
    pos arg 2. (N_poly): number of polygon to convert
    '''
    # init. plotting list
    lons = []
    lats = []

    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]

        # get the Basemap coordinates of each segment
        coords_cc = np.array(
            [(vertex[0], vertex[1])
             for (vertex, code) in poly_path.iter_segments(simplify=False)]
        )

        # convert coordinates to lon/lat by 'inverting' the Basemap projection
        lon_cc, lat_cc = m(coords_cc[:, 0], coords_cc[:, 1], inverse=True)

        lats.extend(lat_cc.tolist() + [None])
        lons.extend(lon_cc.tolist() + [None])

    return lons, lats


# Function generating coastline lon/lat
def get_coastline_traces():
    poly_paths = m.drawcoastlines().get_paths()  # coastline polygon paths
    N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
    cc_lons, cc_lats = polygons_to_traces(poly_paths, N_poly)
    return cc_lons, cc_lats


# Function generating country lon/lat
def get_country_traces():
    poly_paths = m.drawcountries().get_paths()  # country polygon paths
    N_poly = len(poly_paths)  # use all countries
    country_lons, country_lats = polygons_to_traces(poly_paths, N_poly)
    return country_lons, country_lats
