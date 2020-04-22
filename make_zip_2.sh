#!/bin/bash

cd /storage/mvm/data
listsite=`ls -1`
for i in $listsite
do
   echo Working in Site $i 
   cd $i
   listCampaign=`ls -1`
   for j in $listCampaign
   do
    zip -r ${i}_${j}.zip $j -x '*.zip'
   done
   cd ..
done
