#!/bin/bash
echo "#########################################################################"
echo  File Name: runfa.sh
echo  Author: rehemanyidiresi
echo  mail: rehemanyidiresi@novogene.com
echo  Created Time: `ls -l|grep runfa.sh |awk '{print $6,$7,$8}'`
echo "#########################################################################"
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
bash ${soft}/visualize/run-asm-visualizer1.sh -p true -i $ass".cprops" $ass".asm" $ass".mnd") &

wait
