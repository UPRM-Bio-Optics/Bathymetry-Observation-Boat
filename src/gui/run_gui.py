# Graphical User Interface (GUI)

# Dependencies
import subprocess
import sys
import PySimpleGUI as gui
import ctypes
import platform
from graphs_gui import showGraphsMenu, showCSVgraph

def run():

    # Set theme
    gui.theme('Dark Green 6')

    # Font type
    font = 'arial 12'
    titleFont = 'arial 24'

    # Define layout
    layout = [
        # Title
        [gui.Text(
            text="Hydronautical Observation Platform for Hydrographic Sounding",
            font=titleFont
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
                expand_x='true',
                do_not_clear=False
            ),
            gui.Button(
                button_text='Run',
                size=(10, 1),
                bind_return_key=True
            )
        ],
        # an output area where all print output will go
        [gui.Multiline(
            key='_OUT_',
            size=(60, 25),
            expand_x=True,
            auto_refresh=True,
            echo_stdout_stderr=True,
            disabled=True,
            autoscroll=True
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
    window = gui.Window(
        title="HOPHS", 
        layout=layout, 
        margins=(50, 50),
        finalize='true'
        )

    output = window["_OUT_"]
    
    window.refresh()

    # Display correct resolution
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)

    # Create an event loop
    while True:

        # Read user inputs
        event, values = window.read()

        if event == 'Run':

            output.print('\n--> '+values['_IN_']+'\n')

            try: 
                # Send commands to shell                 
                process = subprocess.run(
                    args=values['_IN_'], 
                    shell=True, 
                    capture_output=True
                    ).stdout

                process = process.decode(errors='replace').rstrip()
                # process = process.decode(errors='backslashreplace').rstrip()
                output.print(process)
            
            except:
                output.print('Super Mega Fatal Error: WOW!')
                continue
            # Parse and write stdout to gui
#             for line in process:
                
#                 # line = line.decode(errors='replace').rstrip()

#                 # if (sys.version_info) < (3, 5):
#                 #     line = line.decode(errors='replace').rstrip()

#                 # else:
#                 #     line = line.decode(errors='backslashreplace').rstrip()

# #                 line = line.decode(errors='replace' if (sys.version_info) < (
# #                   3, 5) else 'backslashreplace').rstrip()
                

#                 output.print(line)

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

    print('...GUI ended.')

# # This function does the actual "running" of the command.  
# # Also watches for any output. If found output is printed
# def runCommand(cmd, timeout=None, window=None):
#     process = subprocess.Popen(
#         cmd, 
#         shell=True, 
#         stdout=subprocess.PIPE, 
#         stderr=subprocess.STDOUT)

#     output = ''

#     for line in process.stdout:
#         line = line.decode(errors='replace' if (sys.version_info) < (
#             3, 5) else 'backslashreplace').rstrip()
#         output += line
#         print(line)

#         if window:
#             window.Refresh()  # if window else None        # yes, a 1-line if, so shoot me

#     retval = process.wait(timeout)
    
#     return (retval, output)


run()
