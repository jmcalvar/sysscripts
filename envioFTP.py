#!/usr/bin/python
'''Script para enviar ficheros por ftp cuando no tenemos cliente ftp'''
import ftplib, os

DIR = "ficheros"

listaf = os.listdir(DIR)
os.chdir(DIR)

def envioFTP(fichero):
  session = ftplib.FTP('direccionftp','usuario','pass')
  file = open(fichero,'rb')                  # fichero a enviar
  session.storbinary('STOR '+fichero, file)     # envio de fichero
  file.close()                                    # cerramos el fichero y la con
exion
  session.quit()

for fich in listaf:
  envioFTP(fich)
