import os,sys

name=sys.argv[1]
data={}

bam=os.popen('samtools view '+name,'r')
for line in bam:
    l=line.strip().split()
    if l[0] not in data.keys():
        data[l[0]]=1
        print line,
    else:
        if data[l[0]] < 2:
            print line,
            data[l[0]]=2


bam.close()
