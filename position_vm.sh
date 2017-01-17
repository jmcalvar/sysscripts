#!/bin/bash

# Extract information which host belongs a vm without using vcenter
# se need sshpass installed previously


# We define variables we'll use later
tmpcolo="colo.tmp"
tmphost="host.tmp"
sep="________________________________________________________"

# We create an array with our servers (in our case, they are in different racks)


SERVERSCOLO=( 192.168.5.130 192.168.5.131 192.168.5.132 )
SERVERHOST=( 192.168.5.133 192.168.5.134 192.168.5.135 )

# Creation of function to ssh every server

function extraer {
  for i in ${ARRAY[@]}; do
    echo "" >> $TMP
    echo ${i} >> $TMP
    sshpass -p "ourpassword" ssh -o StrictHostKeyChecking=no root@${i} 'vim-cmd vmsvc/getallvms' >> $TMP
    done
}


# Printing info to a file and deleting temporary files

echo "COLO" >> $tmpcolo
echo $sep >> $tmpcolo
echo "" >> $tmpcolo
TMP=$tmpcolo
ARRAY=${SERVERSCOLO[@]}
extraer

echo "" >> $tmpcolo
echo "" >> $tmpcolo

echo "HOST" >> $tmphost
echo $sep >> $tmphost
echo "" >> $tmphost
TMP=$tmphost
ARRAY=${SERVERHOST[@]}
extraer

# Backup of old file

mv estado_vm_hosts.txt backup/estado_vm_hosts.txt.`date +%Y%m%d%h%m`
cat $tmpcolo $tmphost > estado_vm_hosts.txt
rm -f $tmpcolo
rm -f $tmphost

# Attach file and send by email

echo "Body Message" | mailx -s "Subject" -a "estado_vm_hosts.txt" ouremail@domain.com
