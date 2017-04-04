"""Script para envio de ficheros desde el servidor de storage a caixabank
para su tratamiento"""


# Importamos los modulos necesarios
# Como el script esta en desarrollo, algunos modulos
# no son necesarios todavia aunque estan incluidos

import sqlite3 as lite
import sys
import glob
import os
import time
from datetime import datetime,timedelta
from shutil import copyfile
import shutil
import archivar

# Directorio donde se encuentran los videos
ORIGEN="/backup/video/"

# Directorio donde vamos  a copiar los videos para su compresion
DESTINO="nuevo"

# Prefijo obligatorio que tiene que tener el zip
NOMBREENVIO="BOP20001"

# Fecha Actual
FECHAHOY=datetime.now()

# El delta que utilizamos para coger los ficheros de ayer
dias=timedelta(days=1)

# Operacion para encontrar la fecha de ayer
FECHAAYER=FECHAHOY-dias

# Formato de fecha que va a tener en el fichero
FECHAFICH=FECHAAYER.strftime("%m%d%y")

# Nombre que se le va a dar al zip
NOMBREPAQUETE="BOB20001.P00001.F"+FECHAFICH

# Prefijo el fichero
NOMBREFICH="BOB20001."



def InsertarBBDD(fichero, ficheronuevo ):
  con = lite.connect('envios.db')
 con = lite.connect('envios.db')
  with con:
    cur = con.cursor()
    sql = "INSERT INTO Registro (Fich, FichN, Mydate) VALUES (?, ?, ?)"
    cur.execute(sql, (fichero,ficheronuevo,str(datetime.now())))





def buscar5Ficheros():
  """Funcion de busqueda de ficheros y declaracion de una lista"""
  lista=[]
  files=glob.glob(ORIGEN+"*.mp4")
  files.sort(key=os.path.getmtime)
  return files


def CopiarFicheros():
 """Funcion para copiar los ficheros con el nuevo nombre en el directorio
 e incluirlos en el zip correspondiente"""
 lista5=[]
 lista=buscar5Ficheros()
 if lista:
   lista5=lista[-5:]
   if not os.path.exists(NOMBREPAQUETE):
     os.makedirs(NOMBREPAQUETE)
     index=0
     for i in lista5:
       index += 1
       shutil.copyfile(i,str(NOMBREPAQUETE)+"/"+str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")
       InsertarBBDD(i,str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")

   shutil.make_archive(NOMBREPAQUETE, 'zip',NOMBREPAQUETE)
 else:
   print "no hay ficheros"
def FicherosFiltrados():
  # Si esta variable es NO, se incluye todo
  # Si esta variable es "SI", se filtra lo que metemos en la listsa
  FILTRAR="NO"
  index=0
  # Creamos una lista con todos los ficheros
  lista=buscar5Ficheros()

  # Creamos una lista vacia
  lista_filtrada=[]

  # lista de 5 en caso necesario
  lista5=lista[-5:]
  if not os.path.exists(NOMBREPAQUETE):
    os.makedirs(NOMBREPAQUETE)

  NOMBRENUEVO=str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4"
  # Como filtro tenemos el dia de ayer
  FILTRO=str(FECHAAYER.year)+str(FECHAAYER.month)+str(FECHAAYER.day)
  for i in lista5:
    fech_epoc=os.path.getmtime(i)
    fecha=datetime.fromtimestamp(fech_epoc)
    sinfiltro=str(fecha.year)+str(fecha.month)+str(fecha.day)

    # Si el hay ficheros de ayer se incluyen en la lista
    if sinfiltro == FILTRO:
      lista_filtrada.append(i)
      index += 1
      shutil.copyfile(i,str(NOMBREPAQUETE)+"/"+str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")
      InsertarBBDD(i,str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")
    # Si no coincide el filtro ahora elegimos si metemos todo o no
    elif FILTRAR == "SI":
      print "no guardo nada"
      break
    else:
      # Metemos todo efectivamente
      #lista_filtrada.append(i)
      #InsertarBBDD(i,i)
      # Hasta aqui si metemos todo lo anterior
      index += 1
      shutil.copyfile(i,str(NOMBREPAQUETE)+"/"+str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")
      InsertarBBDD(i,str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")

    shutil.make_archive(NOMBREPAQUETE, 'zip',NOMBREPAQUETE)


  return  lista

#a=CopiarFicheros()
a = FicherosFiltrados()
