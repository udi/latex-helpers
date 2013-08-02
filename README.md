latex-helpers
=============

Python scripts for various things to improve latex processing

useless_files.py - helps find figures that were not used in the final manuscript. This is used when you want to upload your latex sources (and images) into some compilation system, such as IEEE-Explore, and do not want to include all the figures you drag along in your ./fig folder. This script compares the files that you have in your image folders with the ones that exist in you .tex files, and lets you know which ones are probably not used. I tried to include support for \ignore but it is not generic enough (yet).

plotter.py - a matplotlib helper that can help export plots in a uniform way. The main function is export_fig and this exports the figures in a nice, clean way, that is consistent and has large enough fonts so that it is easily viewed in a 2-col paper.

cdf_plot.py - a very useful cdf plotting function. Works exactly as the one in matlab, so it is very easy to use. Just pass a vector and it outputs the (empirical) cdf of the values. It passes additional parameters to pylab.plot, so you can also control the looks&feel of it. Another very useful addition is the parameter "values" that lets you specify markers on the plot for a give y-axis value (e.g., mark the median, or mark the 30% point). This helps refer in the paper to the specific point.


