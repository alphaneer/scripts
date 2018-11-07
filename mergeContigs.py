#!/usr/bin/env python
#########################################################################
# File Name: mergeContigs.py
# Author: rehemanyidiresi
# mail: rehemanyidiresi@novogene.com
# Created Time: Tue 25 Sep 2018 06:16:13 PM CST
#########################################################################
import os, sys


def get_contigs(fasta,cname):
    cmd='samtools faidx '+fasta+' '+cname
    with os.popen(cmd,'r') as r:
        contig = r.read()
    return contig

def asd(reads):
    data={'A':'T','T':'A','C':'G','G':'C','a':'t','t':'a','c':'g','g':'c','N':'N','n':'n'}
    r=''
    for i in reads:
        r+=data[i]
    return r[::-1]

def parseOverHangs(overhangs,fa,ca,gaps):
    label='>Hic_asm_'
    agp = ''
    gap='N'*int(gaps)
    gsize=int(os.popen('awk \'{a+=$3}END{print a}\' '+sys.argv[2], 'r').read().strip())
    report='name\tnumber\tlength\n'
    rn=0
    stt=0
    end=0
    num=0
    overhangLength=0
    for overhang in range(len(overhangs)):
        ocont=label+str(overhang)+'\n'
        rs=0
        for oh in overhangs[overhang]:
            c=get_contigs(fa,ca[oh.strip('-')][0])
            rs+=int(ca[oh.strip('-')][1].strip())
            end=int(stt)+int(ca[oh.strip('-')][1].strip())
            num+=1
            if '-'==oh[0]:
                min="-"
            else:
                min="+"
            agp+=label.replace('>','')+str(overhang)+'\t'+str(stt+1)+'\t'+str(end)+'\t'+str(num)+'\tW\t'+ca[oh.strip('-')][0]+'\t1\t'+ca[oh.strip('-')][1].strip()+'\t'+min+'\n'
            if oh == overhangs[overhang][-1]:

                end=0
                stt=0
                num=0
            else:
                stt=int(end)
                end+=int(gaps)
                num+=1
                rs+=int(gaps)
                agp+=label.replace('>','')+str(overhang)+'\t'+str(stt+1)+'\t'+str(end)+'\t'+str(num)+'\tU\t100\tcontig\tno\tna\n'
                stt+=int(gaps)
            cng=''
            cn = c.split('\n')
            for i in range(1,len(cn)-1):
                cng+=cn[i]
            if '-' in oh:
                cg = asd(cng)
            else:
                cg=cng
            ocont+=cg+gap
        report+=label.replace('>','')+str(overhang)+'\t'+str(len(overhangs[overhang]))+'\t'+str(rs)+'\n'
        rn+=rs
        overhangLength+=len(overhangs[overhang])
        g=int(gaps)*-1
        print ocont[:g]
    report = report+'total\t'+str(overhangLength)+'\t'+str(rn)+'('+str(float('%.2f' %(rn*100/float(gsize))))+'%)'
    with open('REPORT.txt','w') as w:
        w.write(report)
    with open(fa+'.agp','w') as w:
        w.write(agp)

def writeNoOverHangs(no_overhangs,fa,ca):
    for no_overhang in no_overhangs:
        c=get_contigs(fa,ca[no_overhang[0].strip('-')][0])
        print c,


if __name__ == '__main__':
#    fa='assembly.txt.review.assembly.fasta'
#    cp='assembly.txt.review.assembly.cprops'
#    asm='assembly.txt.review.assembly.asm'
#    gaps='100'
    fa=sys.argv[1]
    cp=sys.argv[2]
    asm=sys.argv[3]
    gaps=sys.argv[4]
    os.system('samtools faidx '+fa)
    
    cprops=open(cp,'r').readlines()
    asms=open(asm,'r').readlines()
    ca={}
    for c in cprops:
        cc=c.strip().split()
        ca[cc[1]]=[cc[0],cc[2]]
    no_overhangs=[]
    overhangs=[]
    for a in asms:
        aa=a.strip().split()
        if len(aa) > 1:
            overhangs.append(aa)
        else:
            no_overhangs.append(aa)
    parseOverHangs(overhangs,fa,ca,gaps)
    writeNoOverHangs(no_overhangs,fa,ca)


