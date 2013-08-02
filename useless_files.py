# This script detects useless files that do not appear in the latex code
# python useless_files.py latex1.tex latex2.tex -R

import sys
import argparse
import os
import operator

def read_folder( args ):
	all_files = []
	exts = args.image_types.split(",")
	print "exts:",exts
	# reads the folder's files based on the arguments
	for root, dirs, files in os.walk(args.images):

		if args.use_ext:
			include_files = [file for file in files if os.path.splitext(file)[1] in exts ]
		else:
			include_files = [os.path.splitext(file)[0] for file in files if os.path.splitext(file)[1] in exts ]
		#print include_files
		if args.full_path:
			include_files = [os.path.join(root,file) for file in include_files]
			
		all_files.extend( include_files )
		
		# if no need for recursive, then exit immediately
		if not args.recursive:
			break
	
	#print "looking for files: ",all_files
	
	return all_files
		

def closed_single_line(line):
	return True if line.count("{") - line.count("}")<=0 else False

def process_file( args, counter, latex_file, all_files ):
	
	with open( latex_file ) as f:
		within_ignore = 0
		for line in f.readlines():
			if line.startswith("%"):
				# skip comments
				continue

			if line.find("\ignore{")>=0 or line.find("\ignore {")>=0:
				if closed_single_line(line):
					# we have ignore, but the line is nicely closed
					print "closed ignore", line
					continue
				else:
					within_ignore += 1
					print "ignore ", line
			else:
				if within_ignore>0:
					if line.find("{")>=0:
						within_ignore += 1
					if line.find("}")>=0:
						within_ignore -= 1
						if within_ignore <= 0:
							print "out of ignore", within_ignore
			for file in all_files:
				# if finds the file name within the line
				if within_ignore==0 and file in line:
					counter[file] += 1
			

def main(args):
	all_files = read_folder( args )
	
	# build a counter
	counter = {}
	for file in all_files:
		counter[file] = 0

	# process all files
	for latex_file in args.files:
		print "processing %s"%latex_file
		process_file( args, counter, latex_file, all_files )
		
	# print the counter
	print "{:<70} {:<10} {:<10}".format("File","#Appr","Suspected")
	for file in sorted(counter.iteritems(), key=operator.itemgetter(1)):
		suspected = "N"
		if file[1]==0:
			suspected = "T"
		
		print "{:<70} {:<10} {:<10}".format(file[0], file[1],suspected)

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Finds useless images in the folders, that do not appear to be used in the latex files provided')
	parser.add_argument("files", metavar='N', type=str, nargs='+', help="The latex files")
	parser.add_argument("--images",help="The path in which to read images from", type=str, default="./")
	parser.add_argument("-R", "--recursive",help="Recursive read all the images", action="store_true", default=False)
	parser.add_argument("--full-path",help="Whether to use the full paths when looking for file names", action="store_true", default=False)
	parser.add_argument("--use-ext",help="Whether to use the file extention when looking for it in the latex", action="store_true", default=False)
	parser.add_argument("--image-types",help="The type of files to look for (default .eps,.jpg,.pdf,.png).", type=str, default=".eps,.jpg,.pdf,.png")
	args = parser.parse_args()
	main(args)
	
	