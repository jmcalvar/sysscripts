#!/usr/bin/env python

'''Script para rotar los logs, ya que estos logs son especificos y cambian
el formato del nombre de fichero'''

__author__ = "Jose Manuel Calvar"
__version__ = "1.0"
__contact__ = ""

# Necesitamos el modulo os para pocer utilizar el walk
# gzip para comprimir, shutil y glob para realizar operaciones de sistema operativ
# datetime y time para operar con fechas y horas

import os, gzip, shutil, glob, datetime, time

# Escribimos las variables temporales con la fecha de ayer y de hace cuatro  meses
today=datetime.date.today()
yesterday=today - datetime.timedelta(days=1)

formatted=yesterday.strftime("%Y-%m-%d")

now = time.time()

# El directorio donde se almacenanlogs

dir="/var/remotelog"

# Definimos la funcion de rotado

def Rotacion(fichero):
  with open(fichero, 'rb') as f_in, gzip.open(fichero+'.gz', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)
    os.remove(fichero)

def BorradoAntiguos(fichero):
  if os.stat(fichero).st_ctime < now - 120*86400:
    os.remove(fichero)


for root,files,dir in os.walk(dir):
  os.chdir(root)
  for log in  glob.glob("*"+formatted):
    Rotacion(log)
  for comprimido in glob.glob("*"):
    BorradoAntiguos(comprimido)
