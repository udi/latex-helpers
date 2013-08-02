from numpy import *
from pylab import *


def get_closest_val( arr, val ):
    # assuming arr is sorted, and val should be found
    i=0
    while i<len(arr) and val>arr[i]:
        i+=1
        
    if i==len(arr):
        return None
        
    return i

def cdf_plot(x, *args, **kwargs):
    
    values = None
    x=array(x)
    plot_f = plot
    if "values" in kwargs:
        values = kwargs["values"]
        del kwargs["values"]
        
    if "log" in kwargs:
        v=kwargs["log"]
        if v=="x":
            plot_f = semilogx
        elif v=="y":
            plot_f = semilogy
        elif v=="both":
            plot_f = loglog
        elif v=="none":
            plot_f = plot
        del kwargs["log"]
        
        
    use_percent=False
    #CDFPLOT Display an empirical cumulative distribution function.
    #   CDFPLOT(X) plots an empirical cumulative distribution function (CDF) 
    #   of the observations in the data sample vector X. X may be a row or 
    #   column vector, and represents a random sample of observations from 
    #   some underlying distribution.
    #
    #   H = CDFPLOT(X) plots F(x), the empirical (or sample) CDF versus the
    #   observations in X. The empirical CDF, F(x), is defined as follows:
    #
    #   F(x) = (Number of observations <= x)/(Total number of observations)
    #
    #   for all values in the sample vector X. If X contains missing data
    #   indicated by NaN's (IEEE arithmetic representation for
    #   Not-a-Number), the missing observations will be ignored.
    #
    #   H is the handle of the empirical CDF curve (a Handle Graphics 'line'
    #   object). 
    #
    #   [H,STATS] = CDFPLOT(X) also returns a statistical summary structure
    #   with the following fields:
    #
    #      STATS.min    = minimum value of the vector X.
    #      STATS.max    = maximum value of the vector X.
    #      STATS.mean   = sample mean of the vector X.
    #      STATS.median = sample median (50th percentile) of the vector X.
    #      STATS.std    = sample standard deviation of the vector X.
    #
    #   In addition to qualitative visual benefits, the empirical CDF is 
    #   useful for general-purpose goodness-of-fit hypothesis testing, such 
    #   as the Kolmogorov-Smirnov tests in which the test statistic is the 
    #   largest deviation of the empirical CDF from a hypothesized theoretical 
    #   CDF.
    #
    #   See also QQPLOT, KSTEST, KSTEST2, LILLIETEST.

    # Copyright 1993-2004 The MathWorks, Inc. 
    # $Revision: 1.5.2.1 $   $ Date: 1998/01/30 13:45:34 $

    # Get sample cdf, display error message if any
    yy, xx, n = cdfcalc(x)
    
    # Create vectors for plotting
    k = len(xx)
    a=matrix(range(0,k))
    n=kron(ones((2,1)),a)
    
    n = array(n.reshape(2*(k),1,order='F').flatten().tolist()[0]).astype(int)
    #n = reshape(repmat(mslice[1:k], 2, 1), 2 * k, 1)
    
    #xCDF = hstack((-Inf, xx[n], Inf))
    #print n.size
    #print xx
    xCDF = hstack((xx[0], xx[n], xx[xx.size-1]))
    #print xCDF
    yCDF = hstack((0, 0, yy[n]))
    #print yCDF

    #
    # Now plot the sample (empirical) CDF staircase.
    #

    if values:
        values = values.split(",")
    """
    if values and len(values)==1:
        vv = values[0].split(":")
        if len(vv)>1:
            marker = vv[1]
        else:
            marker = 's'
        i=get_closest_val( xCDF, int(vv[0]) )
        if i:
            markevery = (xCDF[i], len(xCDF))
            print markevery
            #plot( xCDF[i], yCDF[i], marker,ms=10,label=None )
        else:
            markevery = None
            print "Couldn't find value ",val 
    """
    
    #hCDF = plot(xCDF, yCDF*100)
    if use_percent:
        yCDF = yCDF*100
    
    hCDF = plot_f(xCDF, yCDF,*args, **kwargs)
        
    if values:
        for val in values:
            vv=val.split(":")
            if len(vv)>1:
                marker = vv[1]
            else:
                marker = 's'
            i=get_closest_val( yCDF, float(vv[0]) )
            if i:
                plot( xCDF[i], yCDF[i], marker,ms=10, markeredgewidth=1, markerfacecolor='None' , label=None )
            else:
                print "Couldn't find value ",val 
            
    #grid()
    #show()
    

def cdfcalc(x=None, xname=None):
    #CDFCALC Calculate an empirical cumulative distribution function.
    #   [YCDF,XCDF] = CDFCALC(X) calculates an empirical cumulative
    #   distribution function (CDF) of the observations in the data sample
    #   vector X. X may be a row or column vector, and represents a random
    #   sample of observations from some underlying distribution.  On
    #   return XCDF is the set of X values at which the CDF increases.
    #   At XCDF(i), the function increases from YCDF(i) to YCDF(i+1).
    #
    #   [YCDF,XCDF,N] = CDFCALC(X) also returns N, the sample size.
    #
    #   [YCDF,XCDF,N,EMSG,EID] = CDFCALC(X) also returns an error message and
    #   error id if X is not a vector or if it contains no values other than NaN.
    #
    #   See also CDFPLOT.

    #   Copyright 1993-2004 The MathWorks, Inc.
    #   $Revision: 1.5.2.2 $  $Date: 2004/01/24 09:33:11 $

    # Sort observation data in ascending order.
    x.sort()

    #
    # Compute cumulative sum such that the sample CDF is
    # F(x) = (number of observations <= x) / (total number of observations).
    # Note that the bin edges are padded with +/- infinity for auto-scaling of
    # the x-axis.
    #
    n=x.size
    
    # Get cumulative sums
    yCDF = array([float(i)/n for i in xrange(1,n+1)])

    # Remove duplicates; only need final one with total count
    notdup = diff(x)>0
    # for some reason, the last element is missing
    notdup = hstack((notdup, True))
    xCDF = x[notdup]
    #print x
    #print notdup
    #print xCDF
    yCDF = yCDF[notdup]
    
    return yCDF,xCDF,n
    
# MAIN
if __name__ == "__main__":
    x=array([1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8, 9])
    x=array([1.5, 1.3, 3.1, 4.1, 4, 5, 4.1, 20, 20, 13, 3, 13, 13, 12, 13, 12, 11, 11, 4.1, 4, 4, 2, 3, 2, 3, 4])
    cdf_plot(x,'-')
    
