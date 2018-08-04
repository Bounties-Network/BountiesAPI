#!/bin/bash

echo "Running 'docker-compose down --remove-orphans'"
docker-compose down --remove-orphans
echo "Running 'docker network prune -f'"
docker network prune -f
