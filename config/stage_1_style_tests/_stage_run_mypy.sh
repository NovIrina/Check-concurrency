#!/bin/bash

set -x

echo -e '\n'
echo 'Running mypy check...'

source venv/bin/activate

FAILED=0
LABS=$(cat config/labs.txt)

mypy config core_utils

if [[ $? -ne 0 ]]; then
  echo "Mypy check failed for common folders."
  FAILED=1
else
  echo "Mypy check passed for common folders."
fi

for LAB_NAME in $LABS; do
  echo "Running mypy for lab ${LAB_NAME}"
  TARGET_SCORE=$(bash config/get_mark.sh ${LAB_NAME})

  if [[ ${TARGET_SCORE} -gt 7 ]]; then
    echo "Running mypy checks for marks 8 and 10"
    mypy ${LAB_NAME}
  else
    continue
  fi

  if [[ $? -ne 0 ]]; then
    echo "Mypy check failed for lab ${LAB_NAME}."
    FAILED=1
  else
    echo "Mypy check passed for lab ${LAB_NAME}."
  fi
done

if [[ ${FAILED} -eq 1 ]]; then
  echo "Mypy check failed."
  exit ${FAILED}
fi

echo "Mypy check passed."
