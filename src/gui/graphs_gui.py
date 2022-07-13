# Dependencies
import PySimpleGUI as gui
import os.path
import os
import pandas
import numpy
import matplotlib.pyplot as pyplot
from datetime import date
from matplotlib import cm
from scipy.interpolate import griddata
from bokeh.models import GMapOptions, HoverTool, LogTicker, ColorBar, ColumnDataSource
from bokeh.plotting import gmap, figure
from bokeh.models import GMapOptions, HoverTool, LogTicker, ColorBar, ColumnDataSource
from bokeh.io import export_png
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.layouts import row


# Constants
ROOT_DIR = os.path.abspath(os.curdir)
GRAPHS_DIR = os.sep.join([ROOT_DIR , "Data","Graphs"])
CSV_DIR = os.sep.join([ROOT_DIR , "Data", "depth_data"])

def showGraphsMenu():

    # First the window layout in 2 columns
    file_list_column = [
        [
            gui.Text("Graphs Folder"),
            gui.InputText(default_text=GRAPHS_DIR,
                          enable_events=True, key="-FOLDER-"),
            gui.FolderBrowse(initial_folder=GRAPHS_DIR),
        ],
        [
            gui.Listbox(
                values=os.listdir(GRAPHS_DIR), 
                size=(65, 100), 
                enable_events=True, 
                key="-FILE LIST-")
        ]
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [gui.Text("Choose a graph from the list on the left",
                    size=(200,), 
                    justification='center', 
                    key="-TOUT-")],
        [gui.Image(
            expand_x='true',
            size=(200, 200),  
            key="-IMAGE-"
            )],
    ]

    # ----- Full layout -----
    layout = [
        [
            gui.Column(file_list_column),
            gui.VSeperator(),
            gui.Column(image_viewer_column),
        ]
    ]

    window = gui.Window(
        title="Graph Viewer", 
        layout=layout,
        size=(1200, 900), 
        relative_location=(0, 100),
        resizable=True,
        )

    # Run the Event Loop
    while True:
        event, values = window.read()

        if event == "Exit" or event == gui.WIN_CLOSED:
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]

            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".gif"))
            ]

            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(values["-FILE LIST-"][0])
                window["-IMAGE-"].update(filename=filename)

            except:
                pass

    window.close()


def showCSVgraph():

    layout = [
        [
            gui.Text("CSV Folder"),
            gui.InputText(default_text=CSV_DIR,
                          enable_events=True, key="-FOLDER-"),
            gui.FolderBrowse(initial_folder=CSV_DIR),
        ],
        [
            gui.Listbox(values=os.listdir(CSV_DIR), size=(65, 20),
                        enable_events=True, key="-FILE LIST-")
        ],
        [
            gui.Button(button_text="Analyze",
                       enable_events='true', expand_x='true')
        ]
    ]

    window = gui.Window(title="CSV Analyzer", layout=layout)

    file_selected = False

    # Run the Event Loop
    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]

            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".csv"))
            ]

            window["-FILE LIST-"].update(fnames)

        elif event == "-FILE LIST-":
            file_selected = True
            continue

        elif event == "Analyze" and file_selected:  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )

                try:
                    Contour(filename)
                    window.close()

                except Exception as err:

                    errorWindow('Could not parse file')
                    continue

                showGraphsMenu()

                # MapOverlay(filename)

            except:
                pass

        window.close()


def Contour(csvpath: str, threeD=False):
    df = pandas.read_csv(csvpath)
    lat = df.Latitude
    lon = df.Longitude
    topo = df.Depth_in_Feet

    if(threeD):
        fig, ax1 = pyplot.subplots(subplot_kw={"projection": "3d"})
        fileName = "ThreeD Map.png"
    else:
        fig, ax1 = pyplot.subplots()
        fileName = "TwoD Map.png"

    fig.set_figheight(10)
    fig.set_figwidth(15)
    xi = numpy.linspace(min(lon), max(lon), len(lon))
    yi = numpy.linspace(min(lat), max(lat), len(lat))

    zi = griddata((lon, lat),
                  topo,
                  (xi[None, :], yi[:, None]),
                  method='linear')

    cntr1 = ax1.contourf(xi, yi, zi, levels=30, cmap=cm.coolwarm)
    cbar = fig.colorbar(cntr1, ax=ax1)
    cbar.set_label('Depth in Feet', fontsize=20)

    # uncomment to see where each sample was taken
    #ax1.plot(lon, lat, 'bo', ms=1)

    ax1.set(xlim=(min(lon), max(lon)), ylim=(min(lat), max(lat)))

    ax1.set_title('Bathymetry Map in Parguera', fontsize=20)
    ax1.set_xlabel('Latitude', fontsize=20)
    ax1.set_ylabel('Longitude', fontsize=20)

    today = date.today().strftime("%b-%d-%Y")
    pyplot.savefig(os.sep.join([os.getcwd() + "Data", "Graphs", today + fileName]))

    if(threeD):
        return
    Contour(csvpath, threeD=True)


def MapOverlay(csvpath: str, zoom=18, map_type='satellite'):

    api_key = os.environ['GOOGLE_API_KEY']
    bokeh_width, bokeh_height = 500, 400

    df = pandas.read_csv(csvpath)
    df['radius'] = numpy.sqrt(df['Depth_in_Feet'])/0.8

    lat = numpy.mean(df.Latitude)
    lon = numpy.mean(df.Longitude)

    gmap_options = GMapOptions(lat=lat, lng=lon,
                               map_type=map_type, zoom=zoom)
    hover = HoverTool(
        tooltips=[
            ('Depth in Feet', '@Depth_in_Feet '),
            # the {0.} means that we don't want decimals
            # for 1 decimal, write {0.0}
        ]
    )
    p = gmap(api_key, gmap_options, title='Bathymetry Map Parguera',
             width=bokeh_width, height=bokeh_height,
             tools=[hover, 'reset', 'wheel_zoom', 'pan'])
    source = ColumnDataSource(df)
    # defining a color mapper, that will map values of pricem2
    # between 2000 and 8000 on the color palette
    mapper = linear_cmap('Depth_in_Feet', palette, min(
        df.Depth_in_Feet), max(df.Depth_in_Feet))
    # we use the mapper for the color of the circles
    center = p.circle('Longitude', 'Latitude', radius='radius', alpha=0.4,
                      color=mapper, source=source)
    # and we add a color scale to see which values the colors
    # correspond to
    color_bar = ColorBar(color_mapper=mapper['transform'],
                         location=(0, 0), label_standoff=12,
                         ticker=LogTicker(), border_line_color=None
                         )

    color_bar_title = figure(title='Depth in Feet', title_location='left',
                             height=400,
                             width=200,
                             toolbar_location=None, min_border=0,
                             outline_line_color=None
                             )

    color_bar_title.add_layout(color_bar, 'left')
    color_bar_title.title.align = "center"
    color_bar_title.title.text_font_size = '12pt'

    pu = row(p, color_bar_title)
    today = date.today().strftime("%b-%d-%Y")
    filename = os.sep.join([os.getcwd(),  "Data", "Graphs",   today + ' ' + "MapOverlay.png"])
    export_png(pu, filename=filename)


def errorWindow(text):
    # Define layout
    layout = [
        # Message
        [gui.Text(
            text=text)],

        # Spacing
        [gui.Text(text="")],
        [gui.Text(text="")],

        # Ok Button
        [gui.Button(button_text="OK",
                    expand_x='true'
                    )],
    ]

    # Create the window
    window = gui.Window(title="ERROR", layout=layout, margins=(100, 50))

    # Create an event loop
    while True:

        # Read user inputs
        event, values = window.read()

        # End program if user closes window or
        if event == gui.WIN_CLOSED or event == 'Ok':
            break

    # Exit GUI
    window.close()
