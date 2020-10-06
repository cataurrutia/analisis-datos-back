#!/bin/bash
cd /root/Development/repositorio/analisis-datos-back
export FLASK_APP=app.py
flask run --host=0.0.0.0  >> flask.log &
