import os
import sys


def reader(filepath):
    with open(filepath, 'r') as r:
        agps = []
        for agp in r.readlines():
            agps.append(agp.split())
        return agps

def asd(reads):
    data={'A':'T','T':'A','C':'G','G':'C','a':'t','t':'a','c':'g','g':'c','N':'N','n':'n'}
    r=''
    for i in reads:
        r+=data[i]
    return r

def agp2fasta(cont, agp_file):
    contigs = {}
    back = ''
    for c in open(cont, 'r'):
        #print c[0]
        if c[0] == '>':
            back = c[1:].strip('\n')
            contigs[back] = ''
        else:
            contigs[back] = c
    backId = ''
    flag2 = ''

    fasta = open('new_hic_genome.fa', 'w')
    with open(agp_file, 'r') as a:
        agps = a.readlines()
    print len(agps)
    agp = agps[0].strip('\n').split()
    backId = agp[0]
    fasta.write('>'+backId+'\n')

    for ag in agps:
        a = ag.strip('\n').split()
        if a[0] == backId:
            if a[4] == 'W':
                if a[-1] == '+':
                    fasta.write(contigs[a[5]].strip('\n'))
                elif a[-1] == '-':
                    reads=asd(contigs[a[5]].strip('\n')[::-1])
                    fasta.write(reads)
            else:
                n = 'N'*(int(a[5]))
                fasta.write(n)
        else:
            backId = a[0]
            fasta.write('\n>'+backId+'\n')
            if a[4] == 'W':
                if a[-1] == '+':
                    fasta.write(contigs[a[5]].strip('\n'))
                elif a[-1] == '-':
                    reads=asd(contigs[a[5]].strip('\n')[::-1])
                    fasta.write(reads)
            else:
                n = 'N'*(int(a[5]))
                fasta.write(n)
            print backId, 'ok'
    fasta.close()

def fix(a, b):
    # a='fragScaff_scaffold_0_pilon	356328	363002	4	N	6675	fragment	yes'
    # b='Lachesis_group0__27_contigs__length_50693588	5863142	5863241	2	U	100	contig	no	na'
    a1 = a
    b1 = b
    c = b1[0]+'\t1\t'+a1[5]+'\t0\tN\t'+a1[5]+'\tfragment\tyes'
    return c.split()


def comparison(raw, hic):
    new_agps = []
    unmapped = []
    rs = [[i[4], i[7]] for i in raw]
    hs = [[j[4], j[7]] for j in hic]
    for i in range(len(hs)):
        if hs[i][0] == 'W':
            new_agps.append(hic[i])
            try:
                key1 = rs.index(hs[i])
                if i+1 < len(hs) and hs[i+1][0] == 'U':
                    key2 = rs.index(hs[i+2])
                else:
                    key2 = rs.index(hs[i+1])
                if key1-key2 == -2:
                    new_agps.append(fix(raw[key1+1], hic[i+1]))
                elif key1-key2 == 2:
                    new_agps.append(fix(raw[key1-1], hic[i+1]))
                else:
                    new_agps.append(hic[i+1])
            except:
                if i+1 == len(hs):
                    new_agps.append(hic[i-1])
                else:
                    new_agps.append(hic[i+1])
    for i in range(len(rs)):
        if rs[i][0] == 'W':
            try:
                hs.index(rs[i])
            except:
                unmapped.append(raw[i])
                try:
                    if rs[i+1][0] != 'W':
                        unmapped.append(raw[i+1])
                except:
                    pass
    return new_agps+unmapped


def agp_size(agp):
    agp_start = 1
    agp_end = 0
    number = 1
    agp1 = []
    back = agp[0][0]
    flag1=0
    oldcontig=set()
    agp2=[]
    q=0
    while flag1<len(agp):
        if agp[flag1][4]=='W' and agp[flag1][5] not in oldcontig:
            oldcontig.add(agp[flag1][5])
            agp2.append(agp[flag1])
            flag1+=1
            q=1
        try:
            if q==1 and agp[flag1][4]!='W':
                agp2.append(agp[flag1])
                flag1+=1
                q==0
            if q!=1 and agp[flag1][4]!='W' or agp[flag1][5] in oldcontig:
                flag1+=1
        except:
            flag1+=1
        print len(agp2)
    agp3=[]
    b=agp2[0][0]
    for i in range(len(agp2)):
        if agp2[i][0]==b:
            if agp2[i][4]=='W':
                agp3.append(agp2[i])
            elif i<len(agp2)-1 and agp2[i+1][4]=='W':
                if agp2[i+1][0]==b:
                    agp3.append(agp2[i])
                else:
                    b=agp2[i+1][0]
            if i<len(agp2)-1:
                if agp2[i+1][0]!=b:
                    b=agp2[i+1][0]
    for a in agp3:

        if back == a[0]:
            if a[4] == 'W':
                agp_start = agp_end+1
                agp_end = agp_start+int(a[-2])
                a1 = a[0]+'\t'+str(agp_start)+'\t'+str(agp_end)+'\t'+str(number) + \
                    '\t'+a[4]+'\t'+a[5]+'\t'+a[6]+'\t'+a[7]+'\t'+a[8]+'\n'

                agp1.append(a1)
            else:

                agp_start += agp_end
                agp_end += int(a[5])
                # fragScaff_scaffold_0_pilon	352884	352884	2	N	1	fragment	yes
                a1 = a[0]+'\t'+str(agp_start)+'\t'+str(agp_end)+'\t' + \
                    str(number)+'\t'+a[4]+'\t'+a[5]+'\t'+a[6]+'\t'+a[7]+'\n'

                agp1.append(a1)
        else:
            back = a[0]
            agp_start = 1
            agp_end = agp_start+int(a[-2])
            a1 = a[0]+'\t'+str(agp_start)+'\t'+str(agp_end)+'\t'+str(number) + \
                '\t'+a[4]+'\t'+a[5]+'\t'+a[6]+'\t'+a[7]+'\t'+a[8]+'\n'
            agp1.append(a1)

        number += 1
    return agp1


def hicto10x(filepath_raw, filepath_hic):

    agps_raw = reader(filepath_raw)
    # print agps_raw.next()

    agps_hic = reader(filepath_hic)
    # print agps_hic.next()
    new_agps = comparison(agps_raw, agps_hic)
    # print new_agps
    agp = agp_size(new_agps)
    with open(os.getcwd()+'/hic_add_10X.agp','w') as w:
        for i in agp:
            w.write(i)
    # print agp[0]
def main():
   # try:
     hicto10x(sys.argv[2], sys.argv[3])
     agp2fasta(sys.argv[1], os.getcwd()+'/hic_add_10X.agp')
  #  except:
 #       print 'hicAdd10X.py contig.fa raw.agp hic.agp'

if __name__ == '__main__':
    # filepath_raw = os.getcwd()+'/genome.agp'
    # filepath_hic = os.getcwd()+'/ScafInChr.lst.agp']
	main()
