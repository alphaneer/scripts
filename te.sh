#!/bin/bash
#########################################################################
# File Name: te.sh
# Author: rehemanyidiresi
# mail: rehemanyidiresi@novogene.com
# Created Time: Wed 24 Oct 2018 03:19:45 PM CST
#########################################################################

fa1=$1
fa2=$2

samtools faidx $fa1 &
samtools faidx $fa2 &
wait
for i in `cat ${fa1}.fai|cut -f1`
do
    samtools faidx $fa1 $i > ${i}_1 &
    samtools faidx $fa2 $i > ${i}_2 &
    wait
    diff ${i}_1 ${i}_2 >> diff.txt
    rm ${i}_1 ${i}_2
done
