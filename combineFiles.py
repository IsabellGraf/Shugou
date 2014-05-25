import os
import sys
import re


def read_text_from_include(line):
    match = re.search("^#:include *(.*.kv)", line)
    filename = match.group(1)
    return open(filename, 'r').read()


def main(combine):
    if combine:
        if not os.path.isfile('shugou_original.kv'):
            os.rename('shugou.kv', 'shugou_original.kv')
        infile = open('shugou_original.kv', 'r')
        outfile = open('shugou.kv', 'w')
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
            os.rename('shugou_original.kv', 'shugou.kv')
            print("Original file restored.")
        except:
            print("No backup file.\
                  Maybe the original file has been restored already?")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Missing necessary argument. Use \n\
        'combine' to concatenate the include files into shugou.kv \n\
        'clean' to restore the original shugou.kv file")
    else:
        if (sys.argv[1] == 'Combine' or
                sys.argv[1] == 'combine' or
                sys.argv[1] == 'True'):
            main(True)
        elif (sys.argv[1] == 'Clean' or
                sys.argv[1] == 'clean' or sys.argv[1] == 'False'):
            main(False)
        else:
            print("Can not understand the argument.\
            Call this file again with no arguments to see possible arguments.")
