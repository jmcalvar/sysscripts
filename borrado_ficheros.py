#!/usr/bin/env python

import zipfile, os

ficherozip="BORRADO_VIDEO.ZIP"

zip_ref = zipfile.ZipFile(ficherozip, 'r')
zip_ref.extractall("./")
zip_ref.close()

os.rename("BORRADO VIDEO", "BORRADO_VIDEO")

lista_ficheros_proceso=[]

for root, dirs, files in os.walk("BORRADO_VIDEO"):
  for name in files:
     lista_ficheros_proceso.append((os.path.join(root, name)))

#f=open(ficheros.txt,"rw")
for i in lista_ficheros_proceso:
  with open(i) as f:
    with open("ficheros.txt", "a") as f1:
      for line in f:
        line = line.rstrip()
        f1.write(line+'\n')

os.chdir("/backup/video")
with open("/home/jmcalvar/borrados/ficheros.txt") as aborrar:
  with open("/home/jmcalvar/borrados/log_borrado", "a") as logborrado:
    for line in aborrar:
      fields=line.strip().split()
      try:
        os.remove(str(fields[0])+".mp4")
        #print str(fields[0])+".mp4"
        logborrado.write("borrado fichero " + str(fields[0])+".mp4\n")
      except:
        logborrado.write("error borrando fichero " + str(fields[0])+".mp4\n")
