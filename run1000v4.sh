#!/bin/sh

i=0
max=1000

while [ $i -lt $max ]
do
    echo "output: $i"
    osascript -e 'tell app "Terminal"
        do script "cd /Users/.../tdo/client
         python27 client
    end tell'
done
