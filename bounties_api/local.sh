#!/bin/bash
while :
do
	sleep 30
	python3 ./manage.py get_token_values
	sleep 300
done
