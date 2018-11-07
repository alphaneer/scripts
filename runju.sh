#!/bin/bash
echo "#########################################################################"
echo  File Name: runju.sh
echo  Author: rehemanyidiresi
echo  mail: rehemanyidiresi@novogene.com
echo  Created Time: `ls -l|grep runju.sh |awk '{print $6,$7,$8}'`
echo "#########################################################################"
source /ALBNAS09/rhm/software/bashrc
scripts=/ALBNAS09/rhm/software/juicer/scripts


fa=$1
bam=$2
hic_path=$3

touch merged_abnorm.sam merged_unmapped.sam merged_norm.txt

samtools view $bam |awk 'BEGIN{name = "";reads = "";}{if(/^@/){ print}else{ if($1==name){print reads;print $0;name=""}else{name=$1;reads=$0}}}' \
    |awk 'BEGIN{OFS="\t";flag=0}{if(flag==0){gsub($1,$1"/1");print $0;flag=1}else{gsub($1,$1"/2");print $0;flag=0}}' \
    |awk -v "fname1"=merged_norm.txt -v "fname2"=merged_abnorm.sam -v "fname3"=merged_unmapped.sam -f ${scripts}/common/chimeric_blacklist.awk -

awk '{printf("%s %s %s %d %s %s %s %d", $1, $2, $3, 0, $4, $5, $6, 1); for (i=7; i<=NF; i++) {printf(" %s",$i);}printf("\n");}' merged_norm.txt > merged.frag.txt

sort -T ./ -k2,2d -k6,6d -k4,4n -k8,8n -k1,1n -k5,5n -k3,3n merged.frag.txt > merged.sort.txt

touch dups.txt optdups.txt merged_nodups.txt

awk -f ${scripts}/common/dups.awk -v name=./ merged.sort.txt

python /ALBNAS09/rhm/software/scripts/makecprops.py $fa".fai" > $fa".cprops"
python /ALBNAS09/rhm/software/scripts/makeasm.py $fa".cprops" $hic_path"/" > $fa".asm"
bash /ALBNAS09/rhm/software/3d-dna/visualize/run-asm-visualizer.sh -p true $fa".cprops" $fa".asm" merged_nodups.txt
