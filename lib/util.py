import subprocess, shutil, os, errno

# Run a command and return the output
def cmd(cmd):
  try:
    return subprocess.check_output(cmd, shell=True)
  except subprocess.CalledProcessError as e:
    print "Error in command: " + str(e)
    raise e

def silentremove(filename):
  try:
    if os.path.isdir(filename):
      shutil.rmtree(filename)
    else:
      os.remove(filename)
  except OSError as e:
    if e.errno != errno.ENOENT:
      raise


# Clean the working directory
def clean(workdir):
  cmd("find {0}/result/ -mindepth 1 -maxdepth 1 -not -name '*score_*' -not -name '*result_*.txt' -print0 | xargs -r -0 rm -r --".format(workdir))


 # silentremove(os.path.join(workdir, 'result'))
 # files = os.listdir(os.path.join(workdir, 'result'))
 # for file in files:
 #   silentremove(os.path.join(workdir, 'result', file))
