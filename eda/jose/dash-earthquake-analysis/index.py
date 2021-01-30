# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import (
    overview,
      magnitud,
    visualizacion3D)
# Connect to main app.py file
from app import app
import pandas as pd
import plotly.express as px

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)
app.config.suppress_callback_exceptions = True


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):

    if pathname == "/dash-earthquake-analysis/magnitud":
        return magnitud.layout
    elif pathname == "/dash-earthquake-analysis/visualizacion-3d":
        return visualizacion3D.layout

    else:
        return overview.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
