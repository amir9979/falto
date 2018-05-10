import os
import failing_test
import shutil
from util import cmd
from distutils.dir_util import copy_tree
import errno

def from_cache(workdir, proj, bug):
  dir = "{0}/cache/{1}/{2}/".format(workdir, proj, bug)
  if not os.path.exists(dir):
    return False
  copy_tree(dir, "{0}/result/".format(workdir))
  return True

def cache(workdir, proj, bug):
  dir = "{0}/cache/{1}/{2}/".format(workdir, proj, bug)
  if os.path.exists(dir):
    shutil.rmtree(dir, ignore_errors=True)
    os.makedirs(dir)
  shutil.copytree("{0}/result/".format(workdir), dir)

# Checkout the given project and bug number
def checkout(workdir, proj, bug):
  dir = "{0}/data/{1}/{2}b".format(workdir, proj, bug)
  if not os.path.exists(dir):
    os.makedirs(dir)
    cmd("{0}/data/defects4j/framework/bin/defects4j checkout -p {1} -v {2}b -w {3}".format(workdir,proj,bug,dir))
  else:
    print "Skip checkout because {0} already exists".format(dir)


# Run the tests
def run(workdir, proj, bug, onlyFailing, onlyRelevant, onlyTest):
  cmd("{0}/data/defects4j/framework/bin/defects4j compile -w {0}/data/{1}/{2}b".format(workdir,proj,bug))
  try:
    os.makedirs("{0}/result/".format(workdir))
  except OSError as e:
    if e.errno != errno.EEXIST:
        raise

  if onlyFailing:
    for t in failing_test.get_raw(workdir, proj, bug):
      cmd("{0}/data/defects4j/framework/bin/defects4j test -w {0}/data/{1}/{2}b -t {3}".format(workdir,proj,bug,t))
  elif onlyRelevant:
    cmd("{0}/data/defects4j/framework/bin/defects4j test -w {0}/data/{1}/{2}b -f".format(workdir,proj,bug))
  elif onlyTest:
    cmd("{0}/data/defects4j/framework/bin/defects4j test -w {0}/data/{1}/{2}b -t {3}".format(workdir,proj,bug,onlyTest))
  else:
    cmd("{0}/data/defects4j/framework/bin/defects4j test -w {0}/data/{1}/{2}b".format(workdir,proj,bug))

  with open("result/error.log") as log:
    for line in log:
      if "[ERROR]" in line:
        raise ValueError("Error in log: " + line)
