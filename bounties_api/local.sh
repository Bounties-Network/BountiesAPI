#!/bin/bash

# In production, this is an every 5 minute cronjob. Locally, we just run it regularly using a bash script
while :
do
	sleep 30
	python3 ./manage.py get_token_values
	sleep 300
done
