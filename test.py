def asd(reads):
    data={'A':'T','T':'A','C':'G','G':'C','a':'t','t':'a','c':'g','g':'c','N':'N','n':'n'}
    r=''
    for i in reads:
        r+=data[i]
    return r[::-1]

a='AATTCCGGNNatcgn'

print a
print asd(a)


