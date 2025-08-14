#!/bin/bash
PORT=$1

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

export FLASK_APP=app.py  
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=$PORT

flask run
