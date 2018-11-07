#! /usr/bin/env python
# -*- coding:utf-8   -*-
import os,sys
import multiprocessing as mp
import threading as tg
import datetime

def mycallback(x):
	nb.writelines(x) 

def gr(cname,bedfile):
	bed = []
	for i in bedfile:
		if i.split()[0] in cname:
			bed.append(i)
	return bed

def main(cn=None,bed=None):
	e1 = datetime.datetime.now()
	if cn is None or bed is None:
		bed='/ALBNAS09/rhm/hic-work/09.juhua/00.data/break/alignment.bed'
		cn='/ALBNAS09/rhm/hic-work/09.juhua/00.data/break/contig_names.txt'
	cname = [ c.strip('\n') for c in open(cn,'r').readlines()]
	beddata=open(bed,'r')
	global nb
	nb=open('alignment_iteration_1.bed','w')
	p=mp.Pool(20)
	b1 = beddata.readlines(1)
	while len(b1)!=0:
		b2=[]
		for i in range(10000):
			if len(b1)==0:break
			b1 = beddata.readlines(1)
			b2 += b1
		p.apply_async(gr,(cname,b2,),callback=mycallback)
	p.close()
	p.join()
	e2 = datetime.datetime.now()
	print e2-e1
	beddata.close()
	nb.close()
	e3 = datetime.datetime.now()
	print e3-e2
if __name__=='__main__':
	if len(sys.argv)>1:
		main(sys.argv[1],sys.argv[2])
	else:
		main()
