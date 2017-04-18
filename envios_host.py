import glob
import os
import time
from datetime import datetime,timedelta
from shutil import copyfile
import shutil
import paramiko
import archivar # Este modulo lo creamos nosotros para simplificar el archivado

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
  with con:
    cur = con.cursor()
    sql = "INSERT INTO Registro (Fich, FichN, Mydate) VALUES (?, ?, ?)"
    cur.execute(sql, (fichero,ficheronuevo,str(datetime.now())))

def ChequeoBBDD():
  con = lite.connect('envios.db')
  with con:
    cur = con.cursor()
    cur.execute( 'SELECT  Fich FROM Registro' )
    rows = cur.fetchall()
return rows

def CreacionDirectorio():
  """Chequeamos si existe el directorio y si no existe se crea"""
  if not os.path.exists(NOMBREPAQUETE):
    os.makedirs(NOMBREPAQUETE)

def buscarFicheros():
  """Funcion de busqueda de ficheros y declaracion de una lista"""
  lista=[]
  files=glob.glob(ORIGEN+"*.mp4")
  files.sort(key=os.path.getmtime)
  return files

def FicherosFiltrados():
  # Si esta variable es NO, se incluye todo
  # Si esta variable es "SI", se filtra lo que metemos en la listsa
  FILTRAR="SI"
  index=0
  # Creamos una lista con todos los ficheros
  lista=buscarFicheros()

  # Creamos una lista vacia
  lista_filtrada=[]

  # lista de 5 en caso necesario
  lista5=lista[-10:]

  # Chequeamos si existe el directorio y si no es asi lo creamos

  creacion = CreacionDirectorio()

  NOMBRENUEVO=str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4"
  # Como filtro tenemos el dia de ayer
  FILTRO=str(FECHAAYER.year)+str(FECHAAYER.month)+str(FECHAAYER.day)

  # Cuando dejemos de hacer demos en lugar de utilizar
  # lista5 utilizaremos lista con todo el contenido
  for i in lista5:
    fech_epoc=os.path.getmtime(i)
    fecha=datetime.fromtimestamp(fech_epoc)
    sinfiltro=str(fecha.year)+str(fecha.month)+str(fecha.day)
    print fecha
    print sinfiltro
    print FILTRO
    if FILTRAR == "NO":
      print "no guardo nada"
      break

    # Si hay ficheros de ayer los incluiremos en la lista si no hay no incluira nada
    elif sinfiltro == FILTRO:
      registros = ChequeoBBDD()
      for registro in registros:
        lista_filtrada.append(i)
        index += 1
        shutil.copyfile(i,str(NOMBREPAQUETE)+"/"+str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")
        InsertarBBDD(i,str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")


    # Si no coincide el filtro ahora elegimos si metemos todo o no
    #else:
      # Metemos todo efectivamente
      # Hasta aqui si metemos todo lo anterior
    #  index += 1
    #  shutil.copyfile(i,str(NOMBREPAQUETE)+"/"+str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")
    #  InsertarBBDD(i,str(NOMBREPAQUETE)+"_"+str(FECHAFICH)+"00000"+str(index)+".MP4")

    shutil.make_archive(NOMBREPAQUETE, 'zip',NOMBREPAQUETE)

  return  lista

def RevisionTotal():
  pass

def conexionSFTP():
  """ Para la conexion por sftp utilizamos paramiko
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  # Logicamente falta incluir la ip y el fichero pem
  client.connect(<IP Address>, port=22, username=<User Name>, key_filename=<.PEM File path)
  # Setup sftp connection and transmit this script
  #print "copying"
  sftp = client.open_sftp()
  sftp.put(<Source>, <Destination>)
  sftp.close()"""
  pass

#a = FicherosFiltrados()
print b
