#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dir):
    """returns a list of the absolute paths
    of the special files in the given directory"""

    filenames = os.listdir(dir)
    match_list = []
    for filename in filenames:
        # Regex to match files
        match = re.search(r'.+__\w+__.+', filename)
        if match:
            match_list.append(os.path.abspath(os.path.join(dir, match.group())))
    return match_list

def copy_to(to_paths, dir):

    # get absolute paths for each file in directory
    abs_paths = get_special_paths(dir)

    if os.path.exists(to_paths):
        for p in abs_paths:
            shutil.copy(p, to_paths)
    else:
        os.makedirs(to_paths)
        for p in abs_paths:
            shutil.copy(p, to_paths)
    return

def zip_to(paths, zippath):

    # get absolute paths for each file in directory
    abs_paths = get_special_paths(paths)
    cmd = 'zip -j ' + zippath + ' ' + ' '.join(abs_paths)

    print('Command: ', cmd)

    (status, output) = subprocess.getstatusoutput(cmd)

    if status:
        sys.stderr.write(output)
        print('\n')
        sys.exit(status)

    #print(output)
#    if os.path.exists(to_paths):

#        for p in abs_paths:

#    else:
#        os.makedirs(to_paths)
#        for p in abs_paths:
#            shutil.copy(p, to_paths)

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    fromdir = args[2]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    fromdir = args[2]
    del args[0:2]

  if len(args) == 0:
    print("error: must specify one or more dirs")
    sys.exit(1)

  # +++your code here+++
  dir = args

  if todir:
      copy_to(todir, fromdir)
  elif tozip:
      zip_to(fromdir, tozip)
  else:
      for d in dir:
          paths = get_special_paths(d)
          print('\n'.join(paths))
if __name__ == "__main__":
  main()
