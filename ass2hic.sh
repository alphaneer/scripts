#!/bin/bash
echo "#########################################################################"
echo  File Name: ass2hic.sh
echo  Author: rehemanyidiresi
echo  mail: rehemanyidiresi@novogene.com
echo  Created Time: `ls -l|grep ass2hic.sh |awk '{print $6,$7,$8}'`
echo "#########################################################################"
source /ALBNAS09/rhm/software/bashrc

soft=/ALBNAS09/rhm/software/3d-dna

ass=$1
orig_mnd=$2

export TMPDIR=`pwd`
dos2unix $ass
grep \> $ass |perl -pe 's/>//g' > $ass".cprops"
grep -v \> $ass  > $ass".asm"


bash ${soft}/edit/edit-mnd-according-to-new-cprops.sh $ass".cprops" ${orig_mnd} > $ass".mnd" 
bash ${soft}/visualize/run-asm-visualizer1.sh -p true -q 20 -i $ass".cprops" $ass".asm" $ass".mnd"
