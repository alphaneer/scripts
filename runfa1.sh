#!/bin/bash
#########################################################################
# File Name: runfa.sh
# Author: rehemanyidiresi
# mail: rehemanyidiresi@novogene.com
# Created Time: Tue 25 Sep 2018 06:16:13 PM CST
#########################################################################
#set -vex
source /ALBNAS09/rhm/software/bashrc

soft=/ALBNAS09/rhm/software/3d-dna

orig_fasta=$1
ass=$2
orig_mnd=$3

dos2unix $ass
grep \> $ass |perl -pe 's/>//g' > $ass".cprops"
grep -v \> $ass  > $ass".asm"

(python /ALBNAS09/rhm/software/scripts/spfa.py $ass".cprops" ${orig_fasta} > $ass".fasta" ;
python /ALBNAS09/rhm/software/scripts/mergeContigs.py $ass".fasta" $ass".cprops" $ass".asm" 100 > $ass".FINAL.fasta") &

(bash ${soft}/edit/edit-mnd-according-to-new-cprops.sh $ass".cprops" ${orig_mnd} > $ass".mnd" ;
bash ${soft}/visualize/run-asm-visualizer1.sh -p true -z 1 -i $ass".cprops" $ass".asm" $ass".mnd") &

wait
