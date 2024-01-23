REMOTE FUNCTIONALITY FOR B.O.B


The B.O.B Computer can be equipped with a 4G LTE Hat in order to communicate with the B.O.B during missions, monitor data, battery health, etc. If you decide to use 
this configuration, this folder contains some useful tools to communicate with the B.O.B via SSH.



It is recommended you become familiar with the Linux terminal before using the B.O.B (or alternatively, use the dashboard)

On your main control device (your laptop, phone, etc. It must be able to run Python.)

Run the script client.py, and wait for the B.O.B to connect. The B.O.B should search for a client on startup. 


Once connected, you will be prompted for the password (RPI default is raspberry)

After inputting the password, you now have an SSH connection ready.


If you choose to use the dashboard, simply press connect to await the B.O.B, then you should be able to see the data being transmitted. 





NOTE:

The B.O.B can be used offline if you so configure it, but monitoring the data and condition real-time is best. 
Th
