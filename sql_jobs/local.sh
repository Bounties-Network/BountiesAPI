#!/bin/bash

# In production, this is an hourly cronjob. This script is for local use only
while :
do
	sleep 30
	for f in hourly/*.sql; do psql -h $psql_host -p $psql_port -U $psql_user -d bounties -b -f $f; done;
done