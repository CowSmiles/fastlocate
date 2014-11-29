#! /usr/bin/env python
################################################################################
#     File Name           :     lvim.py
#     Created By          :     Hugh Gao
#     Creation Date       :     [2014-11-28 16:48]
#     Last Modified       :     [2014-11-29 15:30]
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
parser.add_argument('keywords', nargs="+", action='store', help='keywords')
args = parser.parse_args()

if args.file:
    locate = 'locate -A -i %s' % ' '.join(args.keywords)
else:
    locate = 'locate -A -i --regex /%s$ %s' % (args.keywords[0],
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
        print('Please select the file to edit: ', file=sys.stderr, end='')
        result = input()
        if result.isnumeric() and len(files) >= int(result):
            print(files[int(result) - 1], end='')
            break
        else:
            print("Please input the correct integer: ", file=sys.stderr,
                  end='')
            result = input()
