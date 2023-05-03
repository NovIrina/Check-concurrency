#!/bin/bash

set -ex

echo -e '\n'
echo 'Running flake8 check...'

source venv/bin/activate
export PYTHONPATH="$(pwd):${PYTHONPATH}"

python -m flake8 --config ./config/stage_1_style_tests/.flake8 config core_utils seminars

FAILED=0
LABS=$(cat config/labs.txt)

for LAB_NAME in $LABS; do
  echo "Running flake8 for lab ${LAB_NAME}"
  TARGET_SCORE=$(bash config/get_mark.sh ${LAB_NAME})

  if [[ ${TARGET_SCORE} -gt 5 ]]; then
    echo "Running flake8 checks for marks 6, 8 and 10"
    python -m flake8 --config ./config/stage_1_style_tests/.flake8 ${LAB_NAME}
  fi

  if [[ $? -ne 0 ]]; then
    echo "Flake8 check failed for lab ${LAB_NAME}."
    FAILED=1
  else
    echo "Flake8 check passed for lab ${LAB_NAME}."
  fi
done

if [[ ${FAILED} -eq 1 ]]; then
  echo "Flake8 check failed."
  exit ${FAILED}
fi

echo "Flake8 check passed."
