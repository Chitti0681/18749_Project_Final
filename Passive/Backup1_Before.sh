#!/bin/bash

osascript -e 'tell app "Terminal" 
    do script " cd /Users/chitti/Desktop/18749_project/18749/Desktop/18749_project/ && python3 server_passive.py 1 10114 10.0.0.189 1 10119 10122 10117 12345 "
end tell'
