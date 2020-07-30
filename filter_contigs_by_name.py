#!/usr/bin/env python

'''Script for filtering contigs by contig name'''

import sys, re, argparse, os
from Bio import SeqIO

__version__='0.1'
__author__='Ola Brynildsrud'

def parse_args():
	'''Parse arguments'''
	parser = argparse.ArgumentParser(
		description='Filter contigs by name')
	parser.add_argument('--fasta', help='Name of FASTA file to be filtered', required=True)
	parser.add_argument('--filter', help='File with contigs to be filtered out', required=True)
	parser.add_argument('--version',
		help='Installed version',
		action='version',
		version="%(prog)s " + str(__version__)
		)
	args = parser.parse_args()
	return args

def handle_filter_file(myfile):
	'''Converts filter file to list'''
	filterlist = []
	with open(myfile,'rU') as filterfile:
		lines = filterfile.readlines()
		for line in lines:
			filterlist.append(line.lstrip('>').rstrip('\n'))
	return filterlist

def main():
	'''Main function'''
	args = parse_args()
	with open(args.fasta,'rU') as myfile:
		filterme = list(SeqIO.parse(myfile, format="fasta"))
		#print(filterme.__dict__)
		filterlist = handle_filter_file(args.filter)
		samplename = re.search(r'^(\w+)\.(fa|fas|fasta)', args.fasta)[1]
		print(filterlist)
		trimmedlist = []
		with open(samplename + '_filt.fasta', 'w') as outfile:
			for contig in filterme:
				if contig.id not in filterlist:
					trimmedlist.append(contig)
			SeqIO.write(trimmedlist, outfile, 'fasta')

if __name__ == '__main__':
	main()