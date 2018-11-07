from numpy import *
import matrix2image as mi
import os

def average(lst):
    return float(sum(lst)) / len(lst)


def main(m, name):
    # print m
    M = mat(m)
    # print M
    links = []
    if len(m) < 10:
        return 0
    else:
        for i in range(1, len(m)):
            l2 = []
            link1 = l2
            for j in range(i, len(m)):
                link1 += m[j][:i]
            l1 = average(link1)
            links.append(l1)
    l = average(links)
    minlink = min(links)
    print 'minlink :', minlink
    for i in links:
        if i < l / 7:
            print 'i < l / 5 ->', i
            mi.Main(M, name)
			os.system('echo \"'+name+'\" >>break_ids')
            print l
            return 1
    return 0


if __name__ == '__main__':
    ma = [[948, 120, 51, 76, 38, 36, 25, 19, 25, 23, 17, 22],
          [120, 759, 241, 44, 34, 25, 26, 14, 24, 15, 13, 10],
          [51, 241, 861, 143, 57, 61, 36, 42, 28, 17, 17, 17],
          [76, 44, 143, 705, 145, 139, 85, 45, 38, 30, 17, 21],
          [38, 34, 57, 145, 822, 248, 132, 50, 43, 36, 41, 16],
          [36, 25, 61, 139, 248, 904, 235, 73, 46, 42, 27, 37],
          [25, 26, 36, 85, 132, 235, 813, 191, 101, 66, 31, 37],
          [19, 14, 42, 45, 50, 73, 191, 901, 192, 107, 42, 31],
          [25, 24, 28, 38, 43, 46, 101, 192, 872, 200, 53, 52],
          [23, 15, 17, 30, 36, 42, 66, 107, 200, 776, 120, 63],
          [17, 13, 17, 17, 41, 27, 31, 42, 53, 120, 818, 198],
          [22, 10, 17, 21, 16, 37, 37, 31, 52, 63, 198, 934]]
    main(ma, 'test')
