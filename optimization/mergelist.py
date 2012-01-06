#!/usr/bin/env python

import os, sys

fset = set()

def output_relpath(x):
  return output(os.path.relpath(x, sys.argv[1]))

def output(x):
  if x not in fset:
    print x

for f in sys.stdin:
  f = f.strip().lstrip('/').split(os.sep)
  for i in xrange(1,len(f)+1):
    fp = os.sep.join(f[:i])  
    output(fp)
    fset.add(fp)

for dirpath, dirs, files in os.walk(sys.argv[1]):
  for d in dirs:
    output_relpath(os.path.join(dirpath, d))
  for f in files:
    output_relpath(os.path.join(dirpath, f))
