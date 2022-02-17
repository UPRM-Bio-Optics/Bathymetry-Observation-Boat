import sys
import subprocess

# implement pip as a subprocess:
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
'time'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'numpy'])





