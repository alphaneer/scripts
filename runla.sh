#!/bin/bash
echo "#########################################################################"
echo  File Name: runla.sh
echo  Author: rehemanyidiresi
echo  mail: rehemanyidiresi@novogene.com
echo  Created Time: `ls -l|grep runla.sh |awk '{print $6,$7,$8}'`
echo "#########################################################################"
source /ALBNAS09/rhm/software/bashrc

scripts=/ALBNAS09/rhm/software/scripts

genome=$1
left=$2
right=$3
#motif=AAGCTT
motif=$4
clusterN=$5
qs="qsub -cwd -l vf=0G,p=0 -q plant.q -P aliyun -V "
path=`pwd`"/"
bwa index $genome
sh ${scripts}/work.shell $genome $left $right


#SYNTAX: make_bed_around_RE_site.pl <fasta> <motif> <range>
#fasta:  A fasta file representing a genome (reference or draft assembly.)
#motif:  A motif, typically a restriction site sequence (e.g., HindIII = AAGCTT, NcoI = CCATGG, Dpn1 = GATC).
#range:  A number representing how many bp around the sequence to include.  Recommend 500 based on Yaffe & Tanay, Nat.
mkdir breakfile
cd breakfile

sh ${scripts}/runbreak.sh $genome ${path}"01.bam/all.bam"
samtool faidx asm.cleaned.fasta &
make_bed_around_RE_site.pl asm.cleaned.fasta $motif 500 &
CountMotifsInFasta.pl asm.cleaned.fasta $motif &
wait
#samtools view -H breaked_filt.bam|cut -f2|awk -F ':' '{print $2}' > asm.cleaned.fasta.names
sh /ALBNAS09/rhm/software/scripts/RE_site.sh "asm.cleaned.fasta.counts_"`echo $motif|perl -pe 's/^//g'`".txt" "asm.cleaned.fasta.fai"


cd ..
mkdir la
cd la

python ${scripts}/autorun.py ${path}"breakfile/asm.cleaned.fasta" ${path}"breakfile/" $motif $clusterN `echo $qs|perl -pe 's/ /^/g'`
