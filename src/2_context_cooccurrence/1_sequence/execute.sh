#!/bin/bash

# if [ "$1" == "location" ];then
# nohup python3 handle_$1_time.py > Document_$1 &
# else
nohup python3 handle_time_location.py 36000 > Document_36000 &
# fi
