#!/bin/bash

i=0
while :
do
    if ls /var/log/containers/*production_bountiesapi*.log 1> /dev/null 2>&1; then
        for f in /var/log/containers/*production_bountiesapi*.log; do aws s3 cp $f "s3://bountiesapilog/$(date +%Y/%m/%d/%H)/$i-$(basename $f)"; :> $f; echo "$f"; done;
        i=$((i+1));
    fi
    sleep 3600;
done
