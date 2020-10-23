#!/bin/bash
cd /root/Development/repositorio/analisis-datos-back/scripts
date >> captura_con_filtros.log
kill $(cat captura_con_filtros.pid)
kill $(cat limpieza_data.pid)
python3 captura_con_filtros.py >> captura_con_filtros.log & echo $! > captura_con_filtros.pid
