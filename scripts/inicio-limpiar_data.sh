#!/bin/bash
cd /root/Development/repositorio/analisis-datos-back/scripts
date >> limpieza_de_data.log
kill $(cat limpieza_data.pid)
kill $(cat captura_con_filtros.pid)
python3 limpieza_de_data.py >> limpieza_de_data.log & echo $! > limpieza_data.pid
