set -ex

echo -e '\n'

echo "Check requirements.txt file"

source venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH

python config/stage_1_style_tests/requirements_check.py
