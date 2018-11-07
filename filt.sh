#!/bin/bash
#########################################################################
# File Name: filt.sh
# Author: rehemanyidiresi
# mail: rehemanyidiresi@novogene.com
# Created Time: Tue 28 Aug 2018 10:03:04 AM CST
#########################################################################
bam=$1
fasta=$2
samtools view $bam |\
    parallel --pipe grep "XT:A:U" |\
    awk 'BEGIN{name = "";reads = "";}{if(/^GWNJ-/||/^ST-/||/^A/){ if($1==name){print reads;print $0;}else{name=$1;reads=$0} }else {print $0}}'|\
    samtools view -q 30 -bT $fasta - > filt1.bam
