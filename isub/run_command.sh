#!/bin/bash
set -ex

JOB_ID=$1
DIRECTORY=$2
COMMAND=$3

cd $DIRECTORY

LOG_OUT=urm_$JOB_ID.out
LOG_ERR=urm_$JOB_ID.err

now=$(date)
echo "JOB STARTED AT $now" > $LOG_OUT
echo >> $LOG_OUT

#bash $SCRIPT 2>> $LOG_ERR 1>> $LOG_OUT
bash -c "$COMMAND" &>> $LOG_OUT

now=$(date)
echo >> $LOG_OUT
echo "JOB COMPLETE AT $now" >> $LOG_OUT

