#!/bin/bash
#########################################################################
# File Name: RE_site.sh
# Author: rehemanyidiresi
# mail: rehemanyidiresi@novogene.com
# Created Time: Thu 19 Jul 2018 03:16:00 PM CST
#########################################################################
counts=$1
fai=$2
paste $counts $fai|cut -f 1,2,4|sort -k 2nr|awk '{a+=$3;print $1"\t"$2"\t"a}'|sort -k 2n|awk '{if(NR==1)b=$3;print $1"\t"$2"\t"$3/b}'|sort -k 2nr |awk '$3>0.85&&$3<0.98{print $2}' |awk '{if(NR==1)print $0;a=$0}END{print $0}' > resites 
