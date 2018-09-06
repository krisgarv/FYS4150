import sys
from os.path import isfile, join

if len(sys.argv) > 1:
    in_list = sys.argv[1:]
    files = [f for f in in_list if isfile(f)]
    for filename in files:
        line_count=0
        word_count=0
        char_count=0
        with open(filename, 'r') as file:
            for line in file:
                line_count += 1
                word_count += len(line.split())
                for words in line.split():
                    char_count += len(words)
        print(line_count, word_count, char_count, filename)
else:
    print('BadUsage: State input argument(s) i.e.:')
    print('< filename >')
    print('< filename_1 ... filename_n >')
    print('< path/to/file >')
    print('< *.py > , < *.txt > , < * > , ... ')
