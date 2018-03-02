#!/usr/bin/env bash
PROJ_PATH=. #/usr/class/cs161/project

if [ $# -ne 1 ]; then
  echo "Usage: ./runsample.sh PYTHONSOURCEFILE"
  exit
fi

echo "Running python file $1. Timing results:"
echo "If user time + system time ~60 seconds for CLCSFast.py, you should be fine."
echo "P.S. If you're running this for CLCSSlow.py, it's going to take a while."
time python $1 < ${PROJ_PATH}/sample2.in | python ${PROJ_PATH}/judge.py ${PROJ_PATH}/sample2.out

