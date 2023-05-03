set -ex

which python

python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv

source venv/bin/activate

which python

python -m pip install -r requirements.txt
python -m pip install -r requirements_qa.txt

#python -m spacy download ru_core_news_sm # get language model for lab_6 syntax pipeline

curl -L -o mystem.tar.gz https://github.com/fipl-hse/2021-2-level-ctlr/releases/download/mystem_drop/mystem-3.1-linux-64bit.tar.gz
#curl -L -o mystem.tar.gz http://download.cdn.yandex.net/mystem/mystem-3.1-linux-64bit.tar.gz

tar -xf mystem.tar.gz

ls -la

mkdir -p ~/.local/bin
mv mystem ~/.local/bin

ls -la ~/.local/bin

export PYTHONPATH
