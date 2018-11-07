import os
import datetime



if __name__=='__main__':
	e1 = datetime.datetime.now()
	bed='/ALBNAS09/rhm/hic-work/09.juhua/00.data/break/alignment.bed'
	cn='/ALBNAS09/rhm/hic-work/09.juhua/00.data/break/contig_names.txt'
	cname = [ c.strip('\n') for c in open(cn,'r').readlines()]
	beddata=open(bed,'r')
	nb=open('/ALBNAS09/rhm/hic-work/09.juhua/00.data/break/alignment_iteration_12.bed','w')
	for i in beddata:
		if i.split()[0] in cname:
			nb.write(i)
	
	nb.close()
	beddata.close()
	e2 = datetime.datetime.now()
	print e2 - e1



