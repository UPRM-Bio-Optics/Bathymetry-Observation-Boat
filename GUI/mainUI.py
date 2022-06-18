# Graphical User Interface (GUI)

# Dependencies
import subprocess
import sys
import PySimpleGUI as gui
import ctypes
import platform
from graphsUI import showGraphsMenu, showCSVgraph

def main():
    # Set theme
    gui.theme('Dark Green 6')

    # Font type
    font = 'courier'


    # Define layout
    layout = [
        # Title
        [gui.Text(
            text="The Hydronautical Observation Platform for Hydrographic Sounding",
            font=(font+' 16 bold')
        )],

        # Spacing
        [gui.Text(text="")],

        # Label above input field
        [gui.Text(
            text='Enter a command to execute (e.g. dir or ls)',
            font=font
        )],

        # input field where you'll type command
        [
            gui.Input(
                key='_IN_',
                expand_x='true'
            ),
            gui.Button(
                button_text='Run',
                size=(10, 1)
                )
        ],
        # an output area where all print output will go
        [gui.Output(
            size=(60, 25),
            expand_x='true'
            )],

        # Spacing
        [gui.Text(text="")],

        # CSV Button
        [gui.Button(button_text="Analyze CSV File",
                    font=font,
                    expand_x='true'
                    )],

        # Spacing
        [gui.Text(text="")],

        # Maps Button
        [gui.Button(button_text="View Generated Maps",
                    font=font,
                    expand_x='true'
                    )]
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

        if event == 'Run':                  # the two lines of code needed to get button and run command
            runCommand(cmd=values['_IN_'], window=window)

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

# This function does the actual "running" of the command.  Also watches for any output. If found output is printed
def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (
            3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)

if __name__ == '__main__':
    main()
