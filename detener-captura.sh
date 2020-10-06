#!/bin/bash
cd /root/Development/repositorio/analisis-datos-back 
echo 'Deteniendo ' >> captura.log
echo date >> captura.log
date >> captura.apagar.log
kill $(cat captura.pid)
