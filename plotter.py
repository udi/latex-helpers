#!/usr/bin/python
"""
Plots the latency CDF of a set of files

./plot_latency.py "--legend=RE,Non RE"  ~/one_1.4.0/re_reports_redundancy_50_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/reports_redundancy_50_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt --xlabel="Latency (minutes)" --ylabel="CDF" --output=fig/latency_50_disaster_40.pdf
./plot_latency.py "--legend=70%,50%,20%,20% Non-RE"  ~/one_1.4.0/re_reports_redundancy_70_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_50_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_20_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/reports_redundancy_20_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt --xlabel="Latency (minutes)" --ylabel="CDF" --output=fig/latency_20_disaster_40.pdf
./plot_latency.py "--legend=60%,40%,20%,60% Non-RE"  ~/one_1.4.0/re_reports_redundancy_60_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_40_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_20_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/reports_redundancy_60_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt --xlabel="Latency (minutes)" --ylabel="CDF" --output=fig/latency_disaster_40_new.pdf
./plot_latency.py --legend="FN=10%,FN=20%,FN=30%,Non-RE"  ~/one_1.4.0/re_reports_redundancy_40_4hour_disaster_40_fp1_fn10/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_40_4hour_disaster_40_fp1_fn20/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_40_4hour_disaster_40_fp1_fn30/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/reports_redundancy_40_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt --xlabel="Latency (minutes)" --ylabel="CDF" --output=fig/latency_20_disaster_40_with_fps.pdf

./plot_latency.py "--legend=70%,60%,50%,40%,30%,20%"  ~/Develop/intel/theone/one_1.4.0/re_reports_redundancy_70_4hour/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/Develop/intel/theone/one_1.4.0/re_reports_redundancy_60_4hour/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/Develop/intel/theone/one_1.4.0/re_reports_redundancy_50_4hour/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/Develop/intel/theone/one_1.4.0/re_reports_redundancy_40_4hour/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/Develop/intel/theone/one_1.4.0/re_reports_redundancy_30_4hour/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/Develop/intel/theone/one_1.4.0/re_reports_redundancy_20_4hour/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt --xlabel="Latency (seconds)" --ylabel="CDF"
./plot_latency.py "--legend=70%,50%,20%"  ~/one_1.4.0/re_reports_redundancy_70_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_50_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_20_4hour_disaster_40/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt --xlabel="Latency (minutes)" --ylabel="CDF" --output=fig/latency_vs_redundancy_disaster_40.pdf
./plot_latency.py "--legend=70%,50%,20%"  ~/one_1.4.0/re_reports_redundancy_70_4hour_disaster_20/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_50_4hour_disaster_20/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt ~/one_1.4.0/re_reports_redundancy_20_4hour_disaster_20/SingleNode_Pittsburgh_REDeliveredMessagesReport.txt --xlabel="Latency (seconds)" --ylabel="CDF" --output=fig/latency_vs_redundancy_disaster_20.pdf

# plot the peer overlap graphs

python plot_file_xy.py --header --errbar --x_pos="#All Items" --y_pos="Rmse test,avg,Rmse item,avg,Rmse user,avg" --ylabel="RMSE" --xlabel="Number of items" --legend="Rmse test,MF,Rmse item,<Items>,Rmse user,<Users>" data/Results_All_01.csv
python plot_file_xy.py --header --errbar --x_pos="#All Items" --y_pos="Rmse test,avg,Rmse item,avg,Rmse user,avg" --ylabel="RMSE" --xlabel="Number of items" --legend="Rmse test,MF,Rmse item,<Items>,Rmse user,<Users>" --file_label=", NL=500;, NL=1500" data/Results_All_01.csv data/Results_All_01.csv

python plot_file_xy.py --cdf ~/Dropbox/Udi/TAU/Develop/songs/data/overlap.txt --y_value_position=3 --err_value_position=4 --ylabel="Percent of users" --xlabel="Average number of overlapping files"
python plot_file_xy.py --cdf "~/Dropbox/Udi/TAU/Develop/songs/data/overlap.txt::2:" "~/Dropbox/Udi/TAU/Develop/songs/data/overlap.txt::5:" --normy=1 --ylabel="Percent of users" --xlabel="Percent of overlap" --legend="Maximal,Zero"

"""
import sys
from optparse import OptionParser
import itertools
import statistics
from matplotlib.ticker import FormatStrFormatter, MultipleLocator, NullLocator,ScalarFormatter
import numpy
import matplotlib
import pylab
import cdf_plot

options = None

class FixedOrderFormatter(ScalarFormatter):
    """Formats axis ticks using scientific notation with a constant order of 
    magnitude"""
    def __init__(self, order_of_mag=0, useOffset=True, useMathText=False):
        self._order_of_mag = order_of_mag
        ScalarFormatter.__init__(self, useOffset=useOffset, 
                                 useMathText=useMathText)

    def _set_orderOfMagnitude(self, range):
        """Over-riding this to avoid having orderOfMagnitude reset elsewhere"""
        self.orderOfMagnitude = self._order_of_mag

def read_values( file ):
    print "Reading file %s..."%file
    f=open(file,"r")
    xvalues = []
    yvalues = []
    errvalues = []
    values = {}  # mapping "x" values to a set of "y" values { x : { y : [...] , y: [...] },... }
    header = None
    
    try:
        for line in f.readlines():
            line = line.strip()
            
            # see if needs a header line
            if options.header and header is None:
                    header=line.split(options.delimiter)
                    # map the name of the header to the index in the array
                    header = dict(itertools.izip(header,xrange(len(header))))
                    print header
                    continue
            
            # skip comments
            if line.startswith("#"):
                continue
            
            l = line.split(",")
            
            # first, read the x-value
            if header and options.x_pos in header:
                x = float(l[ header[options.x_pos] ] )
            else:
                x = float(l[ int(options.x_pos)] )
                    
            if options.normx:
                x=x/float(l[options.normx])
            
            if x not in values:
                values[x] = {}
                print "x:",x
                    
            # now, match the x-value to the needed y-values
            if options.y_pos:
                cols = options.y_pos.split(",")
                # for each y-value we expect two values - the location and the action..for now, we do not really care about the action
                for i in xrange( 0,len(cols),2 ):
                    if header and cols[i] in header:
                        pos = header[cols[i]]
                        
                    else:
                        pos = int(cols[i]) 
                        
                    y = float(l[ pos ] )
                    
                    if not options.miny or y>=options.miny:
                        if options.normy:
                            y=y/float(l[options.normy])
                    
                    # ok, now we have the y value - let's add it to the right place
                        
                    if cols[i] not in values[x]:
                        values[x][cols[i]] = []
                        
                    # add the value to the right place
                    values[x][cols[i]].append( y )
                    
    except:
        print "bad line."
            
    print "done."

    # now, let's see what we can do with the oprations. For each y operation we need to perform that on the list of matching values
    # overall, each "y" element should have a single number so we can plot them 
    cols = options.y_pos.split(",")
    for i in xrange( 0,len(cols),2 ):
        if header and cols[i] in header:
            pos = header[cols[i]]
        else:
            pos = int(cols[i]) 
            
        op = cols[i+1]
        
        for x in sorted(values.keys()):
            old_values = values[x][cols[i]]
            average, median, standard_deviation, minimum, maximum, confidence = statistics.stats( numpy.array(old_values) )
            if op=="avg":
                new_value = average
                values[x][cols[i]+"_std"] = standard_deviation
                values[x][cols[i]+"_ci"] = confidence
            elif op=="normal":
                new_value = old_values[0]
            elif op=="max":
                new_value = maximum
            elif op=="min":
                new_value = minimum
                
            # set the new (single) value for that given x and y_pos
            values[x][cols[i]] = new_value
    
    return values

def export_fig( x, y, l=None, output=None, fontsize=18, loc="best" ):
    #pylab.xlim( [options.minx,options.maxx] )
    
    for ax in [pylab.gca().xaxis,pylab.gca().yaxis]:
        for label in ax.get_ticklabels():
            label.set_fontsize(fontsize)
            
    if l is not None:
        pylab.rcParams.update( {"legend.fontsize":18} )
        if len(l)>0:
            pylab.legend( l, numpoints=1, loc=loc )
        else:
            pylab.legend( numpoints=1, loc=loc )
    
    
    pylab.subplots_adjust(left=None, bottom=0.13, right=None, top=None,wspace=None, hspace=None)    
    
    pylab.xlabel( x, fontsize=fontsize )
    pylab.ylabel( y, fontsize=fontsize )
    
    pylab.grid()
    
    #pylab.gca().set_xscale('log')
    """
    sf = FixedOrderFormatter(3,useMathText=True)
    sf.set_powerlimits((2,2))
    pylab.gca().xaxis.set_major_formatter(sf)
    """
    
    #extent = pylab.gca().get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    
    if output is None:
        pylab.show()
    else:
        pylab.savefig( output, bbox="tight",dpi=600)#,bbox_inches=extent.expanded(1.35, 1.6) )

def plot_files( files ):
    
    # and now plot
    pylab.figure()
    
    colors = "bgrkmcy"
    markers = "sod^v*<>"
    if options.nolines:
        lines = "         "
    else:
        lines = [ "-", "--", ":", "-.", "-","--",":" ]
    i=0
    legend_text = []
    file_labels = None
    if options.file_label:
            file_labels=options.file_label.split(";")
        
    current_file_index = 0
    for file in files:
        print "processing %s..."%file

        values=read_values( file )
        
        #print values
        # need to build nice vectors for each of the y-values
        x=numpy.array( sorted( values.keys() ) )
        legend=options.legend.strip().split(",")
        for j in xrange( 0,len(legend),2 ):
            #print legend[j]
            y=[]
            err=[]
            legend_text.append( legend[j+1] )
            for xx in x:
                y.append( values[xx][legend[j]] )
                std_label = legend[j]+"_ci"
                if std_label in values[xx]:
                    err.append( values[xx][std_label] )
                
            y=numpy.array(y)
            err=numpy.array(err)
            
            additional_text=""
            if file_labels:
                additional_text = file_labels[current_file_index]
            if options.cdf:
                cdf_plot.cdf_plot( y, linestyle=lines[i], marker=markers[i],color=colors[i], label=legend_text[i]+additional_text, linewidth=2 )
            elif options.errbars:
                pylab.errorbar( x,y, [err,err], linestyle=lines[i], marker=markers[i],color=colors[i], label=legend_text[i]+additional_text, linewidth=2 )
            else:
                pylab.plot( x,y , linestyle=lines[i], color=colors[i], marker=markers[i],label=legend_text[i]+additional_text, linewidth=2 )
            
            i+=1
        
        current_file_index+=1
        
    #print legend_text
    export_fig( options.xlabel, options.ylabel, [])
    

def main():
        global options
        parser = OptionParser(usage="usage: %prog [options] file1[,file2,...]")
        parser.add_option("-o", "--output", default=None, dest="output",help="write plot to FILE", metavar="FILE")
        parser.add_option("--header", default=False,action="store_true",help="Whether to use the first line as a header")
        #parser.add_option("--minx", default=0, type="int", help="Minimal value for x-axis (default=160)")
        #parser.add_option("--maxx", default=162, type="int", help="Maximal value for x-axis (default=160)")
        parser.add_option("--fontsize", default=20, type="int", help="Font size (default=20)")
        parser.add_option("--normx", default=None, type="int", help="Normalize x by dividing it")
        parser.add_option("--normy", default=None, type="int", help="Normalize y by dividing it")
        parser.add_option("--miny", default=None, type="float", help="Set a minimal value of y to be considered")
        parser.add_option("--normx_value", default=None, type="float", help="Normalize x by dividing it")
        parser.add_option("--normy_value", default=None, type="float", help="Normalize y by dividing it")
        parser.add_option("--auto_x", default=False, action="store_true", help="X-values from xrange")
        parser.add_option("--x_pos", default=None, type="string", help="Position of the x-value in the input files (zero-based, default=0)")
        parser.add_option("--y_pos", default=None, type="string", help="Position of the y-values in the input files (zero-based, default=1)")
        parser.add_option("--err_value_position", default=None, type="int", help="Position of the err-value in the input files (zero-based, default=1)")
        parser.add_option("--delimiter", default=",", type="string", help="The delimiter (default ',')")
        parser.add_option("--legend", default=None, type="string", help="The legend")
        parser.add_option("--file_label", default=None, type="string", help="The file labels (will be appended to the legend per file)")
        parser.add_option("--xlabel", default=None, type="string", help="The x-axis label")
        parser.add_option("--ylabel", default=None, type="string", help="The y-axis label")
        parser.add_option("--errbars", default=False, action="store_true", help="Plot error bars")
        parser.add_option("--cdf", default=False, action="store_true", help="Plot cdf instead of scatter")
        parser.add_option("--sort", default=False, action="store_true", help="Sort y-values (default False)")
        parser.add_option("--nolines", default=False, action="store_true", help="Don't plot lines")
        
        
        
        (options, args) = parser.parse_args()
        
        if len(args)>0:
            plot_files( args )
        else:
            parser.print_help()
        
    
if __name__ == "__main__":
    main()