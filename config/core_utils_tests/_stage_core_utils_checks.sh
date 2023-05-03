set -x

source venv/bin/activate

export PYTHONPATH=$(pwd):$PYTHONPATH
python config/skip_check.py --pr_name "$1" --pr_author "$2" --lab_path "lab_5_scrapper"
if [ $? -eq 0 ]; then
  echo 'skip check due to special conditions...' && exit 0
fi

python -m pytest -m "core_utils"

ret=$?
if [ "$ret" = 5 ]; then
  echo "No tests collected.  Exiting with 0 (instead of 5)."
  exit 0
fi

echo "Core utils checks result (should be 0): $ret"

exit "$ret"

