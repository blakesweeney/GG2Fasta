#!/usr/bin/env python

import re
from sets import Set
import argparse

import simplejson as json


class SplitAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        fields = values.split(',')
        curr = getattr(namespace, self.dest) or []
        curr.extend(fields)
        setattr(namespace, self.dest, curr)

parser = argparse.ArgumentParser(description='Convert GG format to fasta')
parser.add_argument('gg_file', metavar='GG', type=file,
                    help='Green Genes file to parse')
parser.add_argument('--fields', action=SplitAction,
                    help='Feilds to output in the fasta file')

args = parser.parse_args()
fields = Set(args.fields)
fields.add('aligned_seq')
entry_pattern = re.compile('([\w_]+)=(.*)$')

record = {}
for line in args.gg_file:
    line.rstrip()
    match = entry_pattern.match(line)
    if match:
      key = match.group(1)
      if key in fields:
          record[key] = match.group(2)
    if line == 'END\n':
      sequence = record['aligned_seq']
      del record['aligned_seq']
      print('> %s' % json.dumps(record))
      print(sequence)
      record = {}
