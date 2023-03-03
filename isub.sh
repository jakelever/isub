#!/bin/bash
set -eux

SCRIPT=$1

if [ ! -f $SCRIPT ]; then
	echo "ERROR: Must provide path to script"
	exit 1
fi

PERMISSIONS=$(stat -c %a .)
if [[ "$PERMISSIONS" != "777" ]]; then
	echo "ERROR: Current directory must have 777 permissions"
	exit 1
fi

JOB_DATE=$(date +"%Y-%m-%d-%H-%M-%S")
RAND_ID=$(cat /dev/urandom | tr -dc 'a-z' | fold -w 4 | head -n 1)
JOB_ID="$JOB_DATE-$RAND_ID"

SCRIPT_NAME=$(basename "$SCRIPT" | tr -dc 'a-zA-Z0-9' | tr '[:upper:]' '[:lower:]' | cut -f 1 -d ' ')

JOB_NAME="$SCRIPT_NAME-$JOB_ID"

echo "Created job: $JOB_NAME"

BASE=/home/jakelever/jakelevervol1claim/isub
JOB_DIR=$BASE/jobs/$JOB_ID

mkdir -p $JOB_DIR

cp $BASE/template.yml $JOB_DIR/job.yml

perl -pi -e "s|JOB_NAME|$JOB_NAME|g" $JOB_DIR/job.yml
perl -pi -e "s|JOB_ID|$JOB_ID|g" $JOB_DIR/job.yml
perl -pi -e "s|PWD|$PWD|g" $JOB_DIR/job.yml
perl -pi -e "s|SCRIPT|$SCRIPT|g" $JOB_DIR/job.yml

echo "Job YML file: $JOB_DIR/job.yml"

oc create -f $JOB_DIR/job.yml

