#!/bin/bash

sudo rfkill block wifi

wifi = "ppp0"
while true
do
        ipAdress=$(/usr/sbin/ifconfig | grep -A2 "$wifi" | grep "inet " | awk -F' ' '{print$2}')
        if [ -z "$ipAdress" ]
        then
                echo  "no Wifi Yet... Retrying..."
        else
                sudo /usr/local/bin/ngrok tcp 22 &
                break
        fi
done
sudo /usr/bin/python3 /home/pi/NCAS-M/NCAS-UPRM/Remote/client.py &

exit 0