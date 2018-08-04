#!/bin/bash

# This script is a simple wrapper to simplify using BountiesAPI with a local blockchain
# - Link the local-chain/docker-compose.override.yml file into the current directory
# - Start docker-compose, which will automatically use the override file
# - Trap ctrl+c so the symbolic link is cleaned up afterwards

# NOTE: 
# If "docker-compose.override.yml" shows up in your git status, it is probably
# because something went wrong with the clean up. Feel free to remove the file,
# as it is supposed to only live in the local-chain folder

trap ctrl_c INT

function ctrl_c() {
  rm docker-compose.override.yml
  docker-compose down --remove-orphans
}

ln -s local-chain/docker-compose.override.yml docker-compose.override.yml
docker-compose up --remove-orphans
