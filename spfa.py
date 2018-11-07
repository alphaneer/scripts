import os,threading,time,sys

def get_contigs(fasta,cname):
    cmd='samtools faidx '+fasta+' '+cname
    with os.popen(cmd,'r') as r:
        contig = r.read()
    return contig

def writeNoSplitContigs(lst,fasta):
    #with open('noSplit.fasta','w') as w:
    for l in lst:
        ll=l.strip().split()[0]
        cng=''
        c = get_contigs(fasta,ll)
        cn = c.split('\n')
        for i in range(1,len(cn)):
            cng+=cn[i]
        contig='>'+ll+'\n'+cng
        #w.write(contig)
        print contig

def parseSplitedContigs(lst,fasta):

    stt=0
    end=0
    data={}
 #   with open('splited.fasta','w') as w:
    for l in lst:
        ll=l.strip().split()
        cname = ll[0].split(':::')[0]
        if cname not in data.keys():
            data[cname]=[]
            data[cname].append(l)
        else:
            data[cname].append(l)
    for cnm in data.keys():
        cng=''
        contig = get_contigs(fasta,cnm)
        cn = contig.split('\n')
        for i in range(1,len(cn)):
            cng+=cn[i]
        for l in data[cnm]:
            ll=l.strip().split()
            end=stt+int(ll[2])
                #a='err'
                #if len(cng[stt:end])==int(ll[2]):
                #a='ok'
    #            print ll[0]
    #            print stt,end,len(cng[stt:end]),ll[2],a
            newContig='>'+ll[0]+'\n'+cng[stt:end]
            print newContig
#                w.write(newContig+'\n')
            stt+=int(ll[2])

        stt=0
        end=0


if __name__ == '__main__':
#    cp='assembly.txt.review.assembly.cprops'
#    fa='juhua10xpilon_ctg.fasta'
    cp=sys.argv[1]
    fa=sys.argv[2]
    os.system('samtools faidx '+fa)
    fai=fa+'.fai'
    cprops=open(cp,'r').readlines()
    non_sp=[]
    sp=[]
    for i in cprops:
        if ':::' in i:
            sp.append(i)
        else:
            non_sp.append(i)
    parseSplitedContigs(sp,fa)
    writeNoSplitContigs(non_sp,fa)

#    os.system('cat splited.fasta noSplit.fasta > '+fa+'.raw.fasta')
