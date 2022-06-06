import sys
import subprocess

# This script installs the necesarry libraries for the program to run

# Implement pip as a subprocess:
def main():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'dronekit'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'pyserial'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'pynmea2'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'scipy'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'matplotlib'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'datetime'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'numpy'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'requests'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'pandas'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'bokeh'])    
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'requests'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'selenium'])    

if __name__ == '__main__':
    main()
