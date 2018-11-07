#! /usr/bin/env python
import os, sys
import platform

if platform.platform().split('-')[0] == 'Linux' or platform.platform().split('-')[0] == 'Windows':
    import matplotlib

    matplotlib.use('Agg')

import scipy.sparse as sps
from numpy import *
import numpy as np
import collections

import demo02


def read_sparseHiCdata(filename, bedFile, startBin=0, endBin=0, smooth_noise=0.5):
    chromosomes, matrixs, numtoid = {}, {}, {}
    try:
        bed = open(bedFile, 'r')
    except IOError:
        print >> sys.stderr, 'cannot open', bedFile
        raise SystemExit

    for line in bed.readlines():
        tags = line.strip().split("\t")
        if tags[0] == 'chrM': continue
        if tags[0] not in chromosomes.keys():
            matrixs[tags[0]] = []
            chromosomes[tags[0]] = []
            chromosomes[tags[0]].append(int(tags[3]))
            numtoid[tags[3]] = tags[0]
        else:
            chromosomes[tags[0]].append(int(tags[3]))
            numtoid[tags[3]] = tags[0]
    clast, start, end = {}, {}, {}
    for chromosome in chromosomes.keys():
        clast[chromosome] = chromosomes[chromosome][-1] - 1
        start[chromosome] = chromosomes[chromosome][0] + startBin
        end[chromosome] = chromosomes[chromosome][0] + endBin

    try:
        matrixFile = open(filename, 'r')
    except IOError:
        print >> sys.stderr, 'cannot open', filename
        raise SystemExit
    lines = collections.OrderedDict()
    for line in matrixFile.xreadlines():
        tags = line.strip().split("\t")
        if numtoid[tags[0]] == numtoid[tags[1]]:
            if numtoid[tags[0]] not in lines.keys():
                lines[numtoid[tags[0]]] = []
                lines[numtoid[tags[0]]].append(tags)
            else:
                lines[numtoid[tags[0]]].append(tags)

    for l in lines.keys():
        if end[l] == chromosomes[l][0]:
            end[l] = clast[l]
        if end[l] > clast[l]:
            end[l] = clast[l]
        if start[l] > clast[l]:
            start[l] = chromosomes[l][0]

        length = end[l] - start[l] + 1
        print length
        if length < 2: continue
        mtx = sps.dok_matrix((length, length), dtype=np.int)
        for tags in lines[l]:
            # print l, start[l], end[l], clast[l], int(tags[0]) - start[l], int(tags[1]) - start[l], int(
            #     round(float(tags[2]))), tags
            if int(tags[0]) <= end[l] and int(tags[0]) >= start[l]:
                if int(tags[1]) <= end[l] and int(tags[1]) >= start[l]:
                    mtx[int(tags[0]) - start[l], int(tags[1]) - start[l]] = int(round(float(tags[2])))
                    mtx[int(tags[1]) - start[l], int(tags[0]) - start[l]] = int(round(float(tags[2])))

        matrix = mtx.todense()
        matrix[matrix < smooth_noise] = 0
        matrixs[l] = matrix.tolist()
        demo02.main(matrix.tolist(), l)
        print '#####'


if __name__ == '__main__':
    mfile = '/Users/rhm/Documents/hic-images/haidamai/720/merged_500000.matrix'
    bfile = '/Users/rhm/Documents/hic-images/haidamai/720/merged_500000_ord.bed'
    # main()
    # bed = open(bfile, 'r')
    contigs = [
        '000014F|arrow|pilon',
        '000041F|arrow|pilon',
        '000017F|arrow|pilon',
        '000049F|arrow|pilon',
        '000066F|arrow|pilon',
        '000063F|arrow|pilon',
        '000013F|arrow|pilon',
        '000044F|arrow|pilon',
        '000015F|arrow|pilon',
        '000094F|arrow|pilon',
        '000007F|arrow|pilon',
        '000051F|arrow|pilon',
        '000057F|arrow|pilon',
        '000047F|arrow|pilon',
        '000146F|arrow|pilon',
        '000128F|arrow|pilon',
        '000123F|arrow|pilon',
        '000208F|arrow|pilon',
        '000053F|arrow|pilon',
        '000072F|arrow|pilon',
        '000073F|arrow|pilon',
        '000113F|arrow|pilon',
        '000201F|arrow|pilon',
        '000183F|arrow|pilon',
        '000129F|arrow|pilon',
        '000325F|arrow|pilon',
        '000040F|arrow|pilon',
        '000126F|arrow|pilon',
        '000289F|arrow|pilon',
        '000383F|arrow|pilon',
        '000542F|arrow|pilon',
        '000573F|arrow|pilon',
        '000224F|arrow|pilon',
        '000262F|arrow|pilon',
        '000120F|arrow|pilon',
        '000482F|arrow|pilon',
        '000418F|arrow|pilon',
        '000627F|arrow|pilon',
        '000704F|arrow|pilon',
        '000628F|arrow|pilon',
        '000498F|arrow|pilon',
        '000400F|arrow|pilon',
        '000335F|arrow|pilon',
        '000530F|arrow|pilon',
        '000489F|arrow|pilon',
        '000457F|arrow|pilon',
        '000727F|arrow|pilon',
        '000642F|arrow|pilon']

    # mat.txt 000300F | arrow | pilon mat.bed 0 0 1 0.5 5 8 False False False 0
    # matrix = read_sparseHiCdata(mfile, '000017F|arrow|pilon', bfile)000000F|arrow|pilon
    # matrix1 = read_sparseHiCdata(mfile, '000206F|arrow|pilon', bfile, 2307, 2319)
    # matrix = read_sparseHiCdata(mfile, '000206F|arrow|pilon', bfile, 0, 0)
    # read_sparseHiCdata(mfile, bfile)
    read_sparseHiCdata(sys.argv[1], sys.argv[2])
    # print matrix
