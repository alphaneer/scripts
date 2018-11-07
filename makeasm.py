import os,sys

def reader(name):
    with open(name,'r') as r:
        a=r.readlines()
    return a
def assmbylt(name,cprops,contignames):
    c = contignames
    group0 =[ x.strip().split()[1:3] for x in os.popen('grep -v \# '+name,'r').readlines()]
    if len(group0)==0:
        return None,c
    else:
        asm=''
        for j in group0:
            c.remove(j[0])
            if j[1]=='0':
                asm+=cprops[j[0]]+' '
            else:
                asm+='-'+cprops[j[0]]+' '
        return asm,c
path=sys.argv[2]
names=os.popen('ls '+path+'|grep gr|sort -k 1.6n,1').readlines()
with open(sys.argv[1],'r') as r:
    a=r.readlines()
cprops={}
for i in a:
    ii= i.strip().split()
    cprops[ii[0]]=ii[1]

contignames=[x.strip().split()[0] for x in a]
for n in names:
    name=path+n.strip()
    asm,contignames = assmbylt(name,cprops,contignames)
    if asm is None:continue
    print asm.strip()
for i in contignames:
    print cprops[i]


