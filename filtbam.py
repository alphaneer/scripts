#!/usr/bin/env python
import os, re, sys,threading


def asd(reads):
    data = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'a': 't', 't': 'a', 'c': 'g', 'g': 'c', 'N': 'N', 'n': 'n',
            '#': '#'}
    r = ''
    for i in reads:
        r += data[i]
    return r


def get_head(path_in):
    gethead = os.popen('samtools view -H ' + path_in, 'r')
    head = gethead.readlines()
    header_id = {}
    for i in range(len(head)):
        ids = head[i].strip().split()[1].split(':')[1]
        header_id[str(i)] = ids
        header_id[ids] = i
    gethead.close()
    return header_id


def flag_value(f, r, m):
    '''
    1	PAIRED        .. paired-end (or multiple-segment) sequencing technology
    2	PROPER_PAIR   .. each segment properly aligned according to the aligner
    4	UNMAP         .. segment unmapped
    8	MUNMAP        .. next segment in the template unmapped
    16	REVERSE       .. SEQ is reverse complemented
    32	MREVERSE      .. SEQ of the next segment in the template is reversed
    64	READ1         .. the first segment in the template
    128	READ2         .. the last segment in the template
    256	SECONDARY     .. secondary alignment
    512	QCFAIL        .. not passing quality controls
    1024	DUP           .. PCR or optical duplicate
    2048	SUPPLEMENTARY .. supplementary alignment
    '''
    flags = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    fg = []
    for i in flags:
        if i & int(f):
            fg.append(i)
    if 16 in fg and 32 not in fg:
        if r == '-' and m == '-':
            f = int(f) + 32 - 16
        if r == '-' and m == '+':
            f = int(f) - 16
        if r == '+' and m == '-':
            f = int(f) + 32
    elif 16 not in fg and 32 in fg:
        if r == '-':
            f = int(f) + 16
        if m == '-':
            f = int(f) - 32
    elif 16 in fg and 32 in fg:
        if r == '-':
            f = int(f) - 16
        if m == '-':
            f = int(f) - 32
    elif 16 not in fg and 32 not in fg:
        if r == '-':
            f = int(f) + 16
        if m == '-':
            f = int(f) + 32

    return str(f)


def bins(bline, reads):
    bins1 = 150
    num = re.findall(r'\d+', bline)
    te = re.findall(r'\D+', bline)
    if reads == '-':
        num.reverse()
        te.reverse()
    am = ''
    for i in range(len(num)):
        if te[i] == 'I':
            bins1 = bins1 - int(num[i])
        if te[i] == 'D':
            bins1 = bins1 + int(num[i])
        am1 = num[i] + te[i]
        am += am1
    return bins1, am


def dist(mate, reads, start1, start2, fv, bins1):
    if mate[0] == reads[0]:
        distance = start2 - start1
        if 64 & int(fv):
            if 16 & int(fv) and not 32 & int(fv):
                distance -= bins1
            elif 32 & int(fv) and not 16 & int(fv):
                distance += bins1
            elif 16 & int(fv) and 32 & int(fv):
                pass
        else:
            if 16 & int(fv) and not 32 & int(fv):
                distance -= bins1
            elif 32 & int(fv) and not 16 & int(fv):
                distance += bins1
            elif 16 & int(fv) and 32 & int(fv):
                pass
    else:
        distance = 0
    return distance


def fixer(bline1, bline2, reads1, mate1, reads2, mate2):
    bin1, am1 = bins(bline1[5], reads1[-1])
    bin2, am2 = bins(bline2[5], reads2[-1])
    bam1 = bline1[0] + '\t'
    bam2 = bline2[0] + '\t'
    # if reads[-1]=='-' and mate[-1]=='-':
    fv1 = flag_value(bline1[1], reads1[-1], mate1[-1])
    print bline1[0], bline1[1], reads1[-1], mate1[-1], bline1[5]
    fv2 = flag_value(bline2[1], reads2[-1], mate2[-1])
    print bline2[0], bline2[1], reads2[-1], mate2[-1], bline2[5]
    bam1 += fv1 + '\t'  # flags
    bam2 += fv2 + '\t'
    bam1 += reads1[0] + '\t'  # read id
    bam2 += reads2[0] + '\t'
    if reads1[-1] == '-':  # start
        start11 = int(reads1[1]) + int(reads1[-2]) - int(bline1[3]) - bin1 + 1
    else:
        start11 = int(reads1[1]) + int(bline1[3]) - 1
    bam1 += str(start11) + '\t'

    if reads2[-1] == '-':  # start
        start12 = int(reads2[1]) + int(reads2[-2]) - int(bline2[3]) - bin2 + 1
    else:
        start12 = int(reads2[1]) + int(bline2[3]) - 1
    bam2 += str(start12) + '\t'

    bam1 += bline1[4] + '\t'  # q
    bam2 += bline2[4] + '\t'

    bam1 += am1 + '\t'
    bam2 += am2 + '\t'

    if mate1[0] == reads1[0]:  # mate
        bam1 += '=\t'
    else:
        bam1 += mate1[0] + '\t'

    if mate2[0] == reads2[0]:  # mate
        bam2 += '=\t'
    else:
        bam2 += mate2[0] + '\t'
    if mate1[-1] == '-':
        start21 = int(mate1[1]) + int(mate1[-2]) - int(bline1[7]) + 1 - 150
        if ('I' or 'D') in bline2[5]:
            start21 = start21 + (150 - bin2) - 1
    else:
        start21 = int(mate1[1]) + int(bline1[7]) - 1
    bam1 += str(start21) + '\t'

    if mate2[-1] == '-':
        start22 = int(mate2[1]) + int(mate2[-2]) - int(bline2[7]) + 1 - 150
        if ('I' or 'D') in bline1[5]:
            start22 = start22 + (150 - bin1) - 1
    else:
        start22 = int(mate2[1]) + int(bline2[7]) - 1
    bam2 += str(start22) + '\t'

    distance1 = dist(mate1[0], reads1[0], start11, start21, fv1, bin1)
    distance2 = dist(mate2[0], reads2[0], start12, start22, fv2, bin2)
    if ('I' or 'D') in bline1[5]:
        distance2 = -distance1
    if ('I' or 'D') in bline2[5]:
        distance1 = -distance2
    if '=' in bam1:
        bam1 += str(distance1) + '\t'
    else:
        bam1 += '0\t'
    if '=' in bam2:
        bam2 += str(distance2) + '\t'
    else:
        bam2 += '0\t'
    if reads1[-1] == '-':
        bam1 += asd(bline1[9][::-1]) + '\t'
        bam1 += bline1[10][::-1] + '\n'
    elif reads1[-1] == '+':
        bam1 += bline1[9] + '\t'
        bam1 += bline1[10] + '\n'

    if reads2[-1] == '-':
        bam2 += asd(bline2[9][::-1]) + '\t'
        bam2 += bline2[10][::-1] + '\n'
    elif reads2[-1] == '+':
        bam2 += bline2[9] + '\t'
        bam2 += bline2[10] + '\n'

    return bam1 + bam2


if __name__ == '__main__':

#    agp = 'ScafInChr.lst.agp'
    agp = sys.argv[2]
    with open(agp, 'r') as r:
        a = r.readlines()

    agpdic = {}

    contig2scaff = {}

    for i in a:
        line = i.strip().split()
        if line[4] != 'W': continue
        contig2scaff[line[5]] = line[0]
        agpdic[line[5]] = line
    '''@SQ	SN:Lachesis_group0__251_contigs__length_426336593	LN:426336593'''
    headers = ''
    for i in os.popen('awk \'{print $1}\' ' + agp + ' |grep La|sort -u'):
        ii = i.strip().split('_')[-1]
        h = '@SQ\tSN:' + i.strip() + '\tLN:' + ii + '\n'
        headers += h
    path_in = sys.argv[1]
    #path_in = '/Users/rhm/Documents/hic-images/juhua/803/ori1000.bam'
    new = open('new.bam', 'w')
    new.write(headers)

    bfile = os.popen('samtools view ' + path_in, 'r')
    # try:
    p1 = bfile.readline()
    p2 = bfile.readline()
    while p2 != '':
        reads1 = p1.strip().split()
        reads2 = p2.strip().split()
        if reads1[0] == reads2[0]:
            if (reads1[2] in agpdic.keys() and reads1[6] in agpdic.keys()) and (
                    reads2[2] in agpdic.keys() and reads2[6] in agpdic.keys()):
                new_bline = fixer(reads1, reads2, agpdic[reads1[2]], agpdic[reads1[6]], agpdic[reads2[2]],
                                  agpdic[reads2[6]])
                new.write(new_bline)
            p1 = bfile.readline()
            p2 = bfile.readline()
        else:
            p1 = p2
            p2 = bfile.readline()
    # except:
    #     pass
    new.close()
    bfile.close()
    os.system('sort -k4n,1 new.bam -o new.bam')
