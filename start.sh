#!/bin/sh
# You need to install the tilix terminal for this script to function
# Stores file location to restart script
fileLoc=$(readlink -f "$0")

echo "Starting Python and React Server"
tilix --command ./startPython.sh --title Python_Server
sleep 3

# gets the PID of the python server
pythonServerJob=$(ps ax | grep server.py)
pythonServerPID=$(echo $pythonServerJob | cut -d ' ' -f 1)

# gets the PID of the react server
reactServerJob=$(ps ax | grep react-scripts/scripts/start.js)
reactServerPID=$(echo $reactServerJob | cut -d ' ' -f 1)

echo "Type restart or r to restart all servers"
echo "Type stop to close all servers and terminal"
INPUT=""

while [ "$INPUT" != "stop" ]
do
    read INPUT
    if [ "$INPUT" = "restart" ] || [ "$INPUT" = "r" ] ; then
        echo "Restarting servers"
        kill $pythonServerPID
        kill $reactServerPID
        exec "$fileLoc"
    fi
done
kill $pythonServerPID
kill $reactServerPID