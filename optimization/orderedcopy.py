#!/usr/bin/env python

'''Small Python-Script that copies files, directories and device-nodes from src-folder to destination, in the order provided on stdin.'''

import os, sys, shutil, stat, errno
from os import path

srcdir = sys.argv[1]
dstdir = sys.argv[2]

def copystat(st, dst):
    """Copy all stat info (mode bits, atime, mtime, flags) from src to dst"""
    if not stat.S_ISLNK(st.st_mode):
      mode = stat.S_IMODE(st.st_mode)
      os.utime(dst, (st.st_atime, st.st_mtime))
      os.chmod(dst, mode)

for f in sys.stdin:
  f = f.strip()
  sf = path.join(srcdir, f)
  df = path.join(dstdir, f)

  print "%s => %s" % (sf, df)

  try:
    srcstat = os.lstat(sf)
  except OSError:
    continue

  if stat.S_ISLNK(srcstat.st_mode):
    os.symlink(os.readlink(sf), df)    
  elif stat.S_ISDIR(srcstat.st_mode):
    try:
      os.mkdir(df)
    except OSError, e:
      if e.errno == 17:
          pass
      else:
          raise
  elif stat.S_ISCHR(srcstat.st_mode) \
     | stat.S_ISBLK(srcstat.st_mode) \
     | stat.S_ISFIFO(srcstat.st_mode) \
     | stat.S_ISSOCK(srcstat.st_mode):
    os.mknod(df, srcstat.st_mode, srcstat.st_rdev)
  elif stat.S_ISREG(srcstat.st_mode):
    shutil.copyfile(sf,df)
  else:
    print >> sys.stderr, "Warning: unsupported filetype: %s" % sf
    continue
  os.lchown(df, srcstat.st_uid, srcstat.st_gid)
  copystat(srcstat, df)

