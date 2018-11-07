#!/bin/bash
echo "#########################################################################"
echo  File Name: plotter.sh
echo  Author: rehemanyidiresi
echo  mail: rehemanyidiresi@novogene.com
echo  Created Time: `ls -l|grep plotter.sh |awk '{print $6,$7,$8}'`
echo "#########################################################################"
source /ALBNAS09/rhm/software/bashrc
fasta=$1
bam=$2
enmz=$3
window=$4
chr=$5
#enmz='A^AGCTT'

fasta_name=`echo $fasta|awk -F '/' '{print $NF}'`
samtools view $bam| awk 'BEGIN{name = "";reads = "";}{if(/^@/){ print}else{ if($1==name){print reads;print $0;name=""}else{name=$1;reads=$0}}}' |perl /ALBNAS09/rhm/software/scripts/bam2pairs.pl - merged_allValidPairs &

samtools faidx $fasta

cut -f 1,2 $fasta".fai" > $fasta_name".sizes"

python /ALBNAS09/rhm/software/scripts/digest_genome.py -r $enmz -o $fasta_name".bed" $fasta
wait
cat merged_allValidPairs| /ALBNAS09/rhm/software/scripts/build_matrix   --matrix-format complete   --binsize $window   --chrsizes $fasta_name".sizes"  --ifile /dev/stdin    --oprefix merged

#/ALBNAS09/rhm/software/scripts/ice --results_filename merged_iced.matrix --filter_low_counts_perc 0.02     --filter_high_counts_perc 0     --max_iter 100 --eps 0.1     --remove-all-zeros-loci    --output-bias 1    --verbose 1 merged.matrix
#colors
#  -hmc , --heatmapColor
#Colors for heatmap: Greys(0), Reds(1),
#YellowToBlue(2), YellowToRed(3-default), Hot(4),
#BlueToRed(5)

#HiCPlotter.py  -f merged_iced.matrix  -bed merged_abs.bed  -tri 1  -wg 1  -ext png  -n test  -o test  -chr Chr5  -hmc 1
HiCPlotter.py  -f merged.matrix  -bed merged_abs.bed  -tri 1  -wg 1  -ext png  -n test  -o test  -chr $chr  -hmc 1
