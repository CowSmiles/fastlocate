#! /usr/bin/env python
################################################################################
#     File Name           :     lvim.py
#     Created By          :     Hugh Gao
#     Creation Date       :     [2014-11-28 16:48]
#     Last Modified       :     [2014-12-04 13:46]
#     Description         :     Using linux locate command to find the result
#     and vim it.
################################################################################
import shlex
from subprocess import Popen, PIPE
import os.path
import argparse
import sys


parser = argparse.ArgumentParser(description='locate the file using locate'
                                 ' command in linux.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--dir', action='store_true',
                   help='to find directory.')
group.add_argument('-f', '--file', action='store_true',
                   help='to find file.')
parser.add_argument('-l', '--limit', type=int, default=15, action='store',
                   help='the maximum number of the results.')
parser.add_argument('-i', '--ignore', action='append',
                    help='ignore the paths containing the given word.')
parser.add_argument('keywords', nargs="+", action='store', help='keywords')
args = parser.parse_args()

locate = 'locate -b -e -i %s' % args.keywords[0]
commands = shlex.split(locate)
files = []


with Popen(commands, stdout=PIPE) as proc:
    for line in iter(proc.stdout.readline, b''):
        file_finded = line.decode('utf-8').strip()
        contain_fuc = lambda x: x.lower() in file_finded.lower()
        # filter extra keywords
        if len(args.keywords) > 1:
            if not all(map(contain_fuc, args.keywords)):
                continue
        if args.ignore and any(map(contain_fuc, args.ignore)):
            continue
        if args.file and os.path.isfile(file_finded):
            files.append(file_finded)
        elif args.dir and os.path.isdir(file_finded):
            files.append(file_finded)
if len(files) == 0:
    print('No result', file=sys.stderr, end='')
    exit
elif len(files) == 1:
    print(files[0], end='')
else:
    for i, f in enumerate(files, 1):
        if i == args.limit + 1:
            break
        print("%s) %s" % (i, f), file=sys.stderr)
    while True:
        if args.file:
            print('Please select the file to edit(default=1, "q" for quit): ',
                  file=sys.stderr, end='')
        elif args.dir:
            print('Please select the directory(default=1, "q" for quit): ',
                  file=sys.stderr, end='')
        result = input()
        if result.isnumeric() and len(files) >= int(result):
            print(files[int(result) - 1], end='')
            break
        elif result == '':
            print(files[0], end='')
            break
        elif result == 'q':
            exit()
