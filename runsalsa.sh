#!/bin/bash
#########################################################################
# File Name: runsalsa.sh
# Author: rehemanyidiresi
# mail: rehemanyidiresi@novogene.com
# Created Time: Tue 11 Sep 2018 10:10:10 AM CST
#########################################################################

bam=$1
fasta=$2
enzyme=$3

bamToBed -i $bam |sort -k 4 -o alignment.bed 

samtools faidx $fasta

python /ALBNAS09/rhm/software/SALSA/run_pipeline.py \
    -a $fasta \
    -l $fasta".fai" \
    -b alignment.bed \
    -e $enzyme \
    -o scaffolds \
    -m yes
