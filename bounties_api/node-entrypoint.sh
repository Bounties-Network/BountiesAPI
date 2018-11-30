#!/bin/sh

# Make sure we can ctrl+c and otherwise exit out of the loop
trap end_loop INT
trap end_loop SIGINT
trap end_loop SIGTERM
function end_loop() {
    exit 0
}

LAMBDA_NAME=$1
SCHEDULE_INTERVAL=$2
DEFAULT_INTERVAL=10

if [ "$SCHEDULE_INTERVAL" == "" ]; then
    SCHEDULE_INTERVAL=$DEFAULT_INTERVAL
    echo
    echo "No schedule argument received, using $SCHEDULE_INTERVAL"
    echo
fi

while true; do
    echo "Running $LAMBDA_NAME"
    /var/lang/bin/node --expose-gc --max-semi-space-size=150 --max-old-space-size=2707 /var/runtime/node_modules/awslambda/index.js $LAMBDA_NAME
    sleep $SCHEDULE_INTERVAL
done