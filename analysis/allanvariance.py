from numpy import *

def allanvariance(data,tlen = None):
    #create mean of chunks
    if tlen is None:
        dlen = len(data)/2
    else:
        dlen = tlen
    result = []
    for i in xrange(1,dlen):
        fp = []
        for x in return_chunk(data,i):
            fp.append(mean(x))

        fq = 0
        #get variance of chunks
        for i in xrange(len(fp)-1):
            tmp = fp[i+1] - fp[i]
            fq = fq + tmp*tmp

        result.append(fq/(2*(len(fp)-1)))

    return result

def return_chunk(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        xx = l[i:i+n]
        if len(xx) == n:
            yield l[i:i+n]
