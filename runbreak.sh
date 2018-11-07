#!/bin/bash
echo "#########################################################################"
echo  File Name: runbreak.sh
echo  Author: rehemanyidiresi
echo  mail: rehemanyidiresi@novogene.com
echo  Created Time: `ls -l|grep runbreak.sh |awk '{print $6,$7,$8}'`
echo "#########################################################################"

fasta=$1
bam=$2


bamToBed -i $bam > alignment.bed
sort -k 4 -o alignment.bed alignment.bed
samtools faidx $fasta
awk '{print $1}' ${fasta}.fai > contig_names.txt
python /ALBNAS09/rhm/software/scripts/grepFile.py contig_names.txt alignment.bed
sort -k 4 -o alignment_iteration_1.bed alignment_iteration_1.bed
/ALBNAS09/rhm/software/scripts/break_contigs_start -a alignment_iteration_1.bed -l ${fasta}.fai > input_breaks
python /ALBNAS09/rhm/software/scripts/correct.py $fasta input_breaks alignment_iteration_1.bed .
perl /ALBNAS09/rhm/software/scripts/breakBam.pl --bam $bam --break input_breaks | samtools view -@ 10 -bS -T asm.cleaned.fasta - > breaked.bam
samtools view breaked.bam|grep -v \*|awk 'BEGIN{name = "";reads = "";}{if(/^@/){ print}else{ if($1==name){print reads;print $0;name=""}else{name=$1;reads=$0}}}'|samtools view -@ 10 -bT asm.cleaned.fasta - > breaked_filt.bam

samtools view -H breaked_filt.bam|cut -f2|awk -F ':' '{print $2}' > asm.cleaned.fasta.names
bwa index asm.cleaned.fasta
