#! /usr/bin/env python
################################################################################
#     File Name           :     lvim.py
#     Created By          :     Hugh Gao
#     Creation Date       :     [2014-11-28 16:48]
#     Last Modified       :     [2014-12-01 08:50]
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
group.add_argument('-l', '--limit', type=int, default=15, action='store',
                   help='the maximum number of the results.')
parser.add_argument('keywords', nargs="+", action='store', help='keywords')
args = parser.parse_args()

if args.file:
    locate = 'locate -A -e -i -l %s %s' % (args.limit, ' '.join(args.keywords))
else:
    locate = 'locate -A -e -i -l %s --regex /%s$ %s' % (args.limit,
                                                        args.keywords[0],
                                                        ' '.join(args.keywords))
commands = shlex.split(locate)
files = []
with Popen(commands, stdout=PIPE) as proc:
    for line in iter(proc.stdout.readline, b''):
        if not line.strip():
            break
        file_finded = line.decode('utf-8').strip()
        if args.file and os.path.isfile(file_finded):
            files.append(file_finded)
        elif args.dir and os.path.isdir(file_finded):
            files.append(file_finded)
if len(files) == 0:
    exit
elif len(files) == 1:
    print(files[0], end='')
else:
    for i, f in enumerate(files, 1):
        print("%s) %s" % (i, f), file=sys.stderr)
    while True:
        if args.file:
            print('Please select the file to edit(default=1): ',
                  file=sys.stderr, end='')
        elif args.dir:
            print('Please select the directory(default=1): ',
                  file=sys.stderr, end='')
        result = input()
        if result.isnumeric() and len(files) >= int(result):
            print(files[int(result) - 1], end='')
            break
        elif result == '':
            print(files[0], end='')
            break
