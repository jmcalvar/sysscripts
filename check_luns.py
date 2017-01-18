#!/usr/bin/env python

import subprocess, re

proceso=subprocess.Popen(["tgtadm","-m","target","-o","show"],stdout=subprocess.PIPE)
data = proceso.communicate()[0].split("\n")

targets=[]
def cuentaTargets(datos):
  for linea in datos:
    if "Target" in linea:
      targets.append(linea)
  return len(targets)

def cuentaOnline(numero,datos):
  """Si hay menos del doble de onlines, alarma"""
  n=0
  objetivo=numero*2
  for linea in  datos:
   if "Online: Yes" in linea:
     n=n+1

  if n == objetivo:
    print "OK"
  else:
    print "NOOK"

  return True


a=cuentaTargets(data)
b=cuentaOnline(a,data)
