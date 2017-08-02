#!/bin/sh

i=0
max=1000

while [ $i -lt $max ]
do
    echo output: $i
    python27 client.py &
    let i=i+1
done
