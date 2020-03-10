#!/bin/bash
if [ -z "$1" ]
then
    url="http://localhost:8081"
else
    url="$1"
fi
while [ : ]
do
    CPU_LOAD=$(awk '{u=$2+$4; t=$2+$4+$5; if (NR==1){u1=u; t1=t;} else print ($2+$4-u1) * 100 / (t-t1); }' <(grep 'cpu ' /proc/stat) <(sleep 1;grep 'cpu ' /proc/stat));
    curl -d "load=$CPU_LOAD" -X POST $url/data
    sleep 1
done