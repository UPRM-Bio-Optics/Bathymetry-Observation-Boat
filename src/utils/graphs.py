
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os


from matplotlib import cm
from datetime import date
from scipy.interpolate import griddata

'''
TODO
- make scannable variable into function -> boolean
'''


def plotlyContour2d(csvpath: str):
    """plot 2d contour of depth data

    Args:
        csvpath (str): path to csv
    """

    df = pd.read_csv(csvpath)
    lat = df.Latitude
    lon = df.Longitude
    topo = df.Depth_in_Feet

    xi = np.linspace(min(lon), max(lon), len(lon))
    yi = np.linspace(min(lat), max(lat), len(lat))

    zi = griddata((lon, lat),
                  topo,
                  (xi[None, :], yi[:, None]),
                  method='linear')

    fig = go.Figure(data=go.Contour(
        z=zi,
        x=xi,
        y=yi,
        colorscale="RdBu",
        ncontours=30
    ))

    fileName = " 2D Contour.png"
    today = date.today().strftime("%b-%d-%Y")
    image = os.sep.join([os.getcwd(), "Data", "Graphs", today + fileName])

    fig.write_image(image)
    fig.show()


def plotlyContour3d(csvpath: str):
    """plot 3d contour of depth data

    Args:
        csvpath (str): path to csv
    """
    df = pd.read_csv(csvpath)
    lat = df.Latitude
    lon = df.Longitude
    topo = df.Depth_in_Feet

    xi = np.linspace(min(lon), max(lon), len(lon))
    yi = np.linspace(min(lat), max(lat), len(lat))

    zi = griddata((lon, lat),
                  topo,
                  (xi[None, :], yi[:, None]),
                  method='linear')

    fig = go.Figure(data=go.Surface(
        z=zi,
        x=xi,
        y=yi,
        colorscale="RdBu",
    ))

    fileName = " 3D Contour.png"
    today = date.today().strftime("%b-%d-%Y")
    image = os.sep.join([os.getcwd(), "Data", "Graphs", today + fileName])

    fig.write_image(image)
    fig.show()


def plotlyGraph(csvpath: str):
    """Make both 2d and 3d graphs

    Args:
        csvpath (str): _description_
    """
    plotlyContour2d(csvpath)
    plotlyContour3d(csvpath)


def MapOverlay(csvpath: str) -> None:
    """ Creates overlay heatmap of Depth Data with a map. 

    Args:
        csvpath (str): Path to csv containing data: Lat, Lon, Depth in feet
        zoom (int, optional):  Defaults to 18.
        map_type (str, optional): type of google map. Defaults to 'satellite'.

    Returns:
        NONE
    """

    df = pd.read_csv(csvpath)
    lat = df.Latitude
    lon = df.Longitude
    topo = df.Depth_in_Feet
    xi = np.linspace(min(lon), max(lon), len(lon))
    yi = np.linspace(min(lat), max(lat), len(lat))

    zi = griddata((lon, lat),
                  topo,
                  (xi[None, :], yi[:, None]),
                  method='linear')

    fig = px.density_mapbox(df, lat="Latitude", lon="Longitude", z="Depth_in_Feet",
                            center=dict(lat=np.mean(lat), lon=np.mean(lon)), zoom=18, height=300)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fileName = " Map Overlay.png"
    today = date.today().strftime("%b-%d-%Y")
    image = os.sep.join([os.getcwd(), "Data", "Graphs", today + fileName])

    fig.write_image(image)
    fig.show()

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server()  # Turn off reloader if inside Jupyter

if __name__ == '__main__':
    csvpath = "C:/Users/dasus/Documents/NCAS-M/NCAS/Data/echo_sounder/Mar-25-2022.csv"
    MapOverlay(csvpath) 
