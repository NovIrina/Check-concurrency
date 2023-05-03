#!/bin/bash

set -x

echo -e '\n'
echo 'Running stubgen check...'

source venv/bin/activate
export PYTHONPATH="$(pwd):${PYTHONPATH}"

FAILED=0
LABS=$(cat config/labs.txt)

for LAB_NAME in $LABS; do
	echo "Running stubgen for lab ${LAB_NAME}"

	for filename in ${LAB_NAME}/*.py; do
	  echo "Generating stubs for ${filename}"
    python ./config/generate_stubs/run_generator.py \
          --source_code_path ${filename} \
          --target_code_path ./build/stubs/${filename}

    if [[ $? -ne 0 ]]; then
      echo "Stubgen check failed for lab: ${LAB_NAME} file: ${filename}."
      FAILED=1
    else
      echo "Stubgen check passed for lab: ${LAB_NAME} file: ${filename}."
    fi
  done
done

if [[ ${FAILED} -eq 1 ]]; then
	echo "Stubgen check failed."
	exit ${FAILED}
fi

echo "Stubgen check passed."
