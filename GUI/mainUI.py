# Graphical User Interface (GUI)

# Dependencies
import PySimpleGUI as gui
import ctypes
import platform
from graphsUI import showGraphsMenu, showCSVgraph

# Set theme
gui.theme('Dark Green 6')

# Font type
fontType = 'courier'

# Define layout
layout = [
    # Title
    [gui.Text(
        text="The Hydronautical Observation Platform for Hydrographic Sounding", font=fontType)],

    # Spacing
    [gui.Text(text="")],
    [gui.Text(text="")],

    # CSV Button
    [gui.Button(button_text="Analyze CSV File",
                            font=fontType, expand_x='true')],

    # Spacing
    [gui.Text(text="")],
    [gui.Text(text="")],

    # Maps Button
    [gui.Button(button_text="View Generated Maps",
                            font=fontType, expand_x='true')]
]

# Create the window
window = gui.Window(title="HOPHS", layout=layout, margins=(50, 50))


# Display correct resolution
if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)


# Create an event loop
while True:

    # Read user inputs
    event, values = window.read()

    # Show CSV Graph when button pressed
    if event == "Analyze CSV File":
        showCSVgraph()

    # Show generated maps when button pressed
    if event == "View Generated Maps":
        showGraphsMenu()

    # End program if user closes window or
    if event == gui.WIN_CLOSED:
        break

# Exit GUI
window.close()
