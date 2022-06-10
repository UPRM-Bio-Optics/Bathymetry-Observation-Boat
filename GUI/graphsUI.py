# Dependencies
import PySimpleGUI as gui
import os.path

# Constants
ROOT_DIR = os.path.abspath(os.curdir)


def showGraphsMenu():
    
    # First the window layout in 2 columns
    file_list_column = [
        [
            gui.Text("Graphs Folder"),
            gui.In(enable_events=True, key="-FOLDER-"),
            gui.FolderBrowse(initial_folder=ROOT_DIR+'\\Data\\Graphs'),
        ],
        [
            gui.Listbox(values=[], size=(65,100), enable_events=True, key="-FILE LIST-")
        ],
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [gui.Text("Choose a graph from the list on the left", size=(200,), justification='center')],
        [gui.Text(size=(200, 0), key="-TOUT-")],
        [gui.Image(expand_x='true', key="-IMAGE-")],
    ]

    # ----- Full layout -----
    layout = [
        [
            gui.Column(file_list_column),
            gui.VSeperator(),
            gui.Column(image_viewer_column),
        ]
    ]

    window = gui.Window(title="Graph Viewer", layout=layout, size=(1900, 1000), relative_location=(0,-32))

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
                window["-TOUT-"].update('')
                window["-IMAGE-"].update(filename=filename)

            except:
                pass

    window.close()

def showCSVgraph():
    exit