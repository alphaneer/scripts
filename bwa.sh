#bwa index -a bwtsw $1
bwa aln -t 4  -f $2.sai  $1 $2 
bwa aln  -t 4   -f $3.sai  $1 $3 
bwa sampe   -f ${2}.pair-end.sam $1 $2.sai $3.sai $2 $3
samtools view -S -h  -q 20 ${2}.pair-end.sam  >${2}.pair-end.flit.sam

awk 'BEGIN{name = "";reads = "";}{if(/^GWNJ-/||/^ST-/){ if($1==name){print reads;print $0;}else{name=$1;reads=$0} }else {print $0}}' ${2}.pair-end.flit.sam > ${2}.pair-end.flit.pe.sam
samtools view -Sb ${2}.pair-end.flit.pe.sam > ${2}.pair-end.flit.pe.bam
