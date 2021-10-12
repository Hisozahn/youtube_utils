import sys

with open(sys.argv[1]) as file:
    for line in file:
        open(line.rstrip(), 'a').close()