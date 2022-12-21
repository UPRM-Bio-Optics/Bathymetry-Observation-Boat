import subprocess
import sys


# This script installs the necesarry libraries for the program to run
# Implement pip as a subprocess:
def main():
    """
    Run This Python Script install all the dependencies on any OS
    """
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
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'pysimplegui'])  
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'seabreeze[pyseabreeze]'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        '-U', 'kaleido'])
if __name__ == '__main__':
    main()
