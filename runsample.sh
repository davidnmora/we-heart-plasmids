#!/usr/bin/env bash
PROJ_PATH=. #/usr/class/cs161/project

if [ $# -ne 1 ]; then
  echo "Usage: ./runsample.sh PYTHONSOURCEFILE"
  exit
fi

echo "Running python file $1. Timing results:"
time python $1 < ${PROJ_PATH}/sample.in | python ${PROJ_PATH}/judge.py ${PROJ_PATH}/sample.out
