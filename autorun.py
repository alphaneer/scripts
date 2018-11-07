import os,re,time,sys
def waiting(n):
	vj=os.popen('qstat|grep '+n+'|awk \'{print $5}\'','r').read().strip()
	if 'w' in vj:
		print 'sleepin 2s'
		time.sleep(2)
		waiting(n)
	else:
		#print vj
		return True

runsh='''export PATH=/ALBNAS09/rhm/software/Lachesis/bin:/ALBNAS09/rhm/software/anaconda/bin:$PATH
export LD_LIBRARY_PATH=/ALBNAS09/rhm/software/Lachesis/lib:$LD_LIBRARY_PATH
source /ALBNAS09/rhm/software/bashrc
Lachesis  test.ini
'''
testini='''
SPECIES = species
OUTPUT_DIR = auto_output%s.%s.0

DRAFT_ASSEMBLY_FASTA = %s
SAM_DIR = %s
SAM_FILES = breaked_filt.bam
RE_SITE_SEQ = %s

USE_REFERENCE = 0
SIM_BIN_SIZE = 0
REF_ASSEMBLY_FASTA = ''
BLAST_FILE_HEAD = ''

DO_CLUSTERING = 1
DO_ORDERING   = 1
DO_REPORTING  = 1

OVERWRITE_GLM = 1
OVERWRITE_CLMS = 1

CLUSTER_N = %s
CLUSTER_CONTIGS_WITH_CENS = -1
CLUSTER_MIN_RE_SITES = %s
CLUSTER_MAX_LINK_DENSITY = %s
CLUSTER_NONINFORMATIVE_RATIO = 0
CLUSTER_DRAW_HEATMAP = 1
CLUSTER_DRAW_DOTPLOT = 1

ORDER_MIN_N_RES_IN_TRUNK = 0
ORDER_MIN_N_RES_IN_SHREDS = 0
ORDER_DRAW_DOTPLOTS = 1
REPORT_EXCLUDED_GROUPS = -1
REPORT_QUALITY_FILTER = 1
REPORT_DRAW_HEATMAP = 1
'''

#fa='/ALBNAS09/rhm/hic-work/25.donglingcao/03.break/asm.cleaned.fasta'
fa=sys.argv[1]
#sam_dir='/ALBNAS09/rhm/hic-work/25.donglingcao/03.break'
sam_dir=sys.argv[2]
#motif='AAGCTT'
motif=sys.argv[3]
#clusterN='10'
clusterN=sys.argv[4]
#qs='qsub -cwd -l vf=1G,p=1 -q plant.q -P aliyun -V '
qs=sys.argv[5]
with open('../breakfile/resites','r') as r:
	res=r.readlines()

qs1=qs.replace('^',' ')
rs=(int(res[0].strip('\n'))-int(res[1].strip('\n')))/50.0


for RE_SITES in range(50):
	for i in range(2,10):
		resite=int(int(res[1].strip('\n'))+(rs*RE_SITES))
		wd='test/auto_output%s.%s.0' % (str(resite),str(i))
		os.system('mkdir -p '+wd)
		#print wd
		testn = testini % (str(resite),str(i),fa,sam_dir,motif,clusterN,str(resite),str(i))
		with open(wd+'/test.ini','w') as w:
			w.write(testn)
		with open(wd+'/run.sh','w') as w:
			w.write(runsh)
		cmd='cd '+wd+';'+qs1 + ' run.sh'
		print cmd
		os.system(cmd)
		
