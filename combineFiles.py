import os
import sys

def read_text_from_include(line):
	filename = line.split(':include')[1].strip()
	return open(filename, 'r').read()

def main(combine):
	if combine:
		if not os.path.isfile('collection_original.kv'):
			os.rename('collection.kv','collection_original.kv')
		infile = open('collection_original.kv', 'r')
		outfile = open('collection.kv', 'w')	
		for line in infile:
			if '#:include' in line:
				text_from_include = read_text_from_include(line)
				outfile.write(text_from_include + '\n')
			else:
				outfile.write(line)
		infile.close()
		outfile.close()
		print("Files successfully concatenated.")
	else:
		try:
			os.rename('collection_original.kv', 'collection.kv')
			print("Original file restored.")
		except:
			print("No backup file. Maybe the original file has been restored already?")

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Missing necessary argument. Use \n 'combine' to concatenate the include files into collection.kv \n 'clean' to restore the original collection.kv file")
	else:
		if sys.argv[1] == 'Combine' or sys.argv[1] == 'combine' or sys.argv[1] == 'True':
			main(True)
		elif sys.argv[1] == 'Clean' or sys.argv[1] == 'clean' or sys.argv[1] == 'False':
			main(False)
		else:
			print("Can not understand the argument. Call this file again with no arguments to see possible arguments.")

