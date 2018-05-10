#!/usr/bin/python

# MIT License
#
# Copyright (c) 2017 David Krebs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, getopt, os
import util, falo, defects4j

def show_help():
  print """Usage: <script> -p <project> -b <bug> [OPTIONS]
Valid options are:
-p <project>	Specify a defects4j project you want to test [Lang|Math|...]
-b <bug>	Pass the bug number it should test [1...]
-w <path>	Workspace: Path where the result files and the checked out source files are written
-s <skips>	Skip certain tasks, comma separated. Valid tasks to skip:
		run: run the tests
		falo: do fault localization
		after: only keep interesting graphs (failing test runs)
		(enhance: enhance the result graphs with real faulty method)
-t <test>	Only run the given testcase. Specified as class::method
-r		Run only relevant testcases (where the modified class is at least loaded)
-f		Only run the failing testcase(s)
-h		Print this help text
"""


def main(argv):
  skip = []
  workdir = os.getcwd()
  proj = None
  bug = None
  onlyFailing = False
  onlyRelevant = False
  onlyTest = None
  mem = None
  try:
    opts, args = getopt.getopt(argv,"hp:b:w:s:t:m:fr")
  except getopt.GetoptError as e:
    print "Error in your arguments: ", e
    show_help()
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      show_help()
      sys.exit()
    elif opt == '-p':
      proj = arg
    elif opt == '-b':
      bug = arg
    elif opt == '-t':
      onlyTest = arg
    elif opt == '-f':
      onlyFailing = True
    elif opt == '-r':
      onlyFailing = True
    elif opt == '-w':
      workdir = arg
    elif opt == '-s':
      skip = arg.split(',')
    elif opt == '-m':
      mem = arg
  if proj == None or bug == None:
    print "Please specify a project and bug number\n"
    show_help()
    sys.exit(2)

  if not 'run' in skip:
    util.clean(workdir)
    if not defects4j.from_cache(workdir, proj, bug):
      defects4j.checkout(workdir, proj, bug)
      defects4j.run(workdir, proj, bug, onlyFailing, onlyRelevant, onlyTest)
      defects4j.cache(workdir, proj, bug)
  if not 'falo' in skip:
    falo.run(workdir, proj, bug, mem)
  if not 'after' in skip:
    falo.keep_interesting_graphs(workdir, proj, bug)
#  if not 'enhance' in skip:
#    falo.enhance_results(workdir, proj, bug)
#    falo.enhance_graphs(workdir, proj, bug)

if __name__ == "__main__":
  main(sys.argv[1:])
