#!/usr/bin/env python
#-*- coding:utf8 -*-
import os,sys
print ("File Name : jbploter.py")
# Power by RehemanYidiresi2018-11-07 10:44:50
print ("Modified by RehemanYidiresi : "+os.popen("ls -l|grep jbploter.py |awk '{print $6,$7,$8}'").read())

#fai='gaodan_bionano.fasta.review.assembly.FINAL.fasta.fai'
#hic='gaodan_bionano.fasta.review.assembly.assembly_20.hic'
#bin='5000000'

fai = sys.argv[1]
hic = sys.argv[2]
bin = sys.argv[3]

os.system("/usr/bin/java -jar /ALBNAS09/rhm/software/3d-dna/visualize/juicebox_tools.jar dump observed KR %s assembly assembly BP %s combined_%s.txt"%(hic,bin,bin))

faidata=open(fai,'r').readlines()
totlength = sum([int(i.split()[1]) for i in faidata])
scale = int(totlength/2100000000)+1
os.system('grep Hic_asm %s|cut -f1 > id.txt'%fai)
total = int(os.popen("grep Hic_asm %s|awk -v bin=%s -v scale=%s '{a+=($2/(scale*1.0)/bin)}END{print int(a)}'"%(fai,bin,scale)).read().strip())
chrom_breaks = []
chrom_breaks.append(0)
breaks_points = 0
for f in faidata:
    if 'Hic_asm_' in f:
        breaks_points += int(f.split()[1])
        chrom_breaks.append(breaks_points/int(bin)/2)
print chrom_breaks
heatmap = open("combined_%s.txt"%(bin),'r').readlines()
heatmap1 = []
heatmap1_chrom_breaks = []
heatmap1_chrom_breaks.append(0.5)
head = 'X\tY\tZ\n'
heatmap1_txt=open('heatmap.txt','w')
heatmap1_txt.write(head)
for h in heatmap:
    line = h.strip().split()
    x = int(line[0])/int(bin)
    y = int(line[1])/int(bin)
    z = float(line[2])
    if x != y:
        if x <= total and y <= total:
            if x not in chrom_breaks and y not in chrom_breaks:
                heatmap1.append([x,y,z])
                #st=str(x)+'\t'+str(y)+'\t'+str(z)+'\n'+str(y)+'\t'+str(x)+'\t'+str(z)+'\n'
                #heatmap1_txt.write(st)
heatmap2 = []
heatmap2 = heatmap1[:]
a = 0
for i in chrom_breaks[1:]:
    heatmap3 = []
    for h in heatmap2:
        if h[0] > (i-a):
            x = h[0] - 1
        else:
            x = h[0]
        if h[1] > (i-a):
            y = h[1] - 1
        else:
            y = h[1]
        heatmap3.append([x,y,h[2]])
    heatmap1_chrom_breaks.append(i-a-0.5)
    a+=1
    heatmap2 = heatmap3[:]
with open('heatmap.chrom_breaks.txt','w') as w:
    for i in heatmap1_chrom_breaks:
        w.write(str(i)+'\n')
for j in heatmap2:
    x=j[0]
    y=j[1]
    z=j[2]
    ss=str(x)+'\t'+str(y)+'\t'+str(z)+'\n'+str(y)+'\t'+str(x)+'\t'+str(z)+'\n'
    heatmap1_txt.write(ss)
heatmap1_txt.close()
print totlength,total,len(heatmap),heatmap[1].split()
os.system('/ALBNAS09/rhm/software/scripts/heatmap.MWAH.R')
os.system('mv HiC_heatmap.jpg HiC_heatmap%s.jpg'%str(int(bin)*2))
os.system('mv heatmap.txt heatmap%s.txt'%str(int(bin)*2))
os.system('mv heatmap.chrom_breaks.txt heatmap.chrom_breaks%s.txt'%str(int(bin)*2))

