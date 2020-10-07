#!/bin/sh
tilix --action session-add-right --command ./startReact.sh --title React_Server
python3 server.py
