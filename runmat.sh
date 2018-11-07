#!/bin/bash
echo "#########################################################################"
echo  File Name: runmat.sh
echo  Author: rehemanyidiresi
echo  mail: rehemanyidiresi@novogene.com
echo  Created Time: `ls -l|grep runmat.sh |awk '{print $6,$7,$8}'`
echo "#########################################################################"
source /ALBNAS09/rhm/software/bashrc


#fai='asm.cleaned.fasta.review.assembly.FINAL.fasta.fai'
#hic='asm.cleaned.fasta.review.assembly_20.hic'
#bin='500000'

fai=$1
hic=$2
bin=$3

grep H ${fai}|awk -v bin=$bin 'BEGIN{print 0}{a+=$2;scale=int(a/2100000000)+1;print int(a/bin/scale)+0.5}' >>heatmap.chrom_breaks.txt
grep H ${fai}|cut -f1 > id.txt

total=`grep H ${fai}|awk -v bin=${bin} '{a+=$2}END{scale=int(a/2100000000)+1;print a/scale/bin}'`
#bash /ALBNAS09/rhm/software/3d-dna//visualize/run-asm-visualizer1.sh -p true -q 20 -r $bin -i gaodan_bionano.fasta.review.assembly.cprops gaodan_bionano.fasta.review.assembly.asm gaodan_bionano.fasta.review.assembly.mnd
/usr/bin/java -jar /ALBNAS09/rhm/software/3d-dna/visualize/juicebox_tools.jar dump observed KR $hic assembly assembly BP $bin "combined_"$bin".txt" 
awk -v bin=$bin '{OFS="\t";if($1!=$2){print $1/bin,$2/bin,$3"\n"$2/bin,$1/bin,$3}else{print $1/bin,$2/bin,$3}}' "combined_"$bin".txt" | awk -v total=${total} '{if($1< total && $2< total) print}' - |sort -k 1n -k 2n - > heatmap.t
echo "X    Y   Z" > head
cat head heatmap.t > heatmap.txt

cat heatmap.chrom_breaks.txt
/ALBNAS09/rhm/software/scripts/heatmap.MWAH.R
rm heatmap.chrom_breaks.txt id.txt head heatmap.t combined_${bin}.txt
