#!/bin/bash

cd /storage/mvm/data
listdir=`ls -1`
for i in $listdir
do
   echo Working in $i 
   cd $i
   zip -r ${i}.zip . -x '*.zip'
   cd ..
done
