import os,sys
#bam='/ALBNAS09/rhm/hic-work/09.juhua/00.data/break/breaked_filt.bam'
#fasta='/ALBNAS09/rhm/hic-work/09.juhua/00.data/break/asm.cleaned.fasta'
bam=sys.argv[1]
fasta=sys.argv[2]

with os.popen('samtools view -H '+bam+'|cut -f2|awk -F \':\' \'{print $2}\'','r') as b:
	bamid=b.readlines()
os.system('samtools faidx '+fasta)
with open(fasta+'.fai','r') as f:
	fai=f.readlines()

inbam=open('inbam.fa','w')
notbam=open('notinbam.fa','w')

for i in fai:
	cname=i.strip().split()[0]
	with os.popen('samtools faidx '+fasta+' \"'+cname+'\"','r') as c:
		contig=c.read()
	if cname+'\n' in bamid:
		inbam.write(contig)
		print '%s is in bam.'%cname
	else:
		notbam.write(contig)
		print '%s is not in bam.'%cname

inbam.close()
notbam.close()


