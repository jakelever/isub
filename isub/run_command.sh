#!/bin/bash
set -ex

JOB_ID=$1
DIRECTORY=$2
COMMAND=$3
LOG_OUT=$4

cd $DIRECTORY

now=$(date)
echo "JOB STARTED AT $now" > $LOG_OUT
echo >> $LOG_OUT

bash -c "$COMMAND" &>> $LOG_OUT

now=$(date)
echo >> $LOG_OUT
echo "JOB COMPLETE AT $now" >> $LOG_OUT

