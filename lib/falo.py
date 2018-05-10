import os, re
from util import cmd
import failing_test
import shutil, errno

def list_graphs(workdir):
  files = [os.path.join(dp, f) for dp, dn, fn in os.walk(workdir + "/result") for f in fn]
  files = map(os.path.splitext, files)
  files = filter(lambda x: x[1] == ".dot", files)
  return map(lambda x: x[0], files)


def keep_interesting_graphs(workdir, proj, bug):
  failing = failing_test.get_with_lines(workdir, proj, bug) + ['all'] # + ['data_1']
  print failing

  files = list_graphs(workdir)
  files = filter(lambda x: os.stat(x + ".dot") > 0, files)
  files = filter(lambda x: all([not x.endswith(t) for t in failing]), files)
  files = map(lambda x: x + ".dot", files)
  map(os.remove, files)
  os.remove('{0}/result/cg/trace.csv'.format(workdir))
  os.remove('{0}/result/cg/coverage.csv'.format(workdir))

# highlights: {node: [color], node2: [color1, color2]}
def enhance_graph(graph, highlights):
  def get_color(colors):
    num = len(colors)
    if num == 1:
      return {"real": "red", "sp1": "yellow"}[colors[0]]
    if num == 2:
      if set(["real", "sp1"]) == set(colors):
        return "orange"
    raise NameError("Can't handle colors " + str(colors));
  for key, value in highlights.iteritems():
    color = get_color(value)
    print color + " for " + str(value)
    graph.insert(0, '\t"' + key + '" [style=filled,fillcolor=' + color + '];\n')

def enhance_graphs(workdir, proj, bug):
  highlights = {}
  for filename in os.listdir("{0}/data/info/{1}/{2}".format(workdir, proj, bug)):
    with open("{0}/data/info/{1}/{2}/{3}".format(workdir, proj, bug, filename), "r") as f:
      nodes = f.readlines()
      nodes = map(lambda x: x.replace('\n', ''), nodes)
      for node in nodes:
        colors = highlights.setdefault(node, []).append(filename)

  print "Highlights: " + str(highlights)

  graph = []
  files = list_graphs(workdir)
  for x in files:
    x = x + ".dot"
    with open(x, "r") as f:
      g = f.readlines()
      graph.extend(g)
  graph = filter(lambda x: x.startswith('\t'), graph)
  graph = list(set(graph))
  enhance_graph(graph, highlights)
  graph.insert(0, 'digraph cg {')
  graph.append('}')
  with open("{0}/result/cg.dot".format(workdir), "w") as f:
    for line in graph:
        f.write(line)

def run(workdir, proj, bug, mem):
  tests = failing_test.get_with_lines(workdir, proj, bug)
  tests = ";".join(tests)

  for filename in os.listdir("{0}/data/info/{1}/{2}".format(workdir, proj, bug)):
    src = "{0}/data/info/{1}/{2}/{3}".format(workdir, proj, bug, filename)
    dest = "{0}/result/info/{1}".format(workdir, filename)
    try:
      os.makedirs("{0}/result/info".format(workdir))
    except OSError as e:
      if e.errno != errno.EEXIST:
        raise

    shutil.copy(src, dest)
  if mem == None:
    cmd("java -jar {0}/falo/falo/target/falo-0.1-jar-with-dependencies.jar '{0}' '{1}'".format(workdir, tests))
  else:
    cmd("java -Xmx{2}g -jar {0}/falo/falo/target/falo-0.1-jar-with-dependencies.jar '{0}' '{1}'".format(workdir, tests, mem))


def get_line(workdir, proj, bug, method):
  print "Get spectra line of " + method
  with open("{0}/spectra/spectra/{1}/{2}/spectra".format(workdir, proj, bug)) as myFile:
    for num, line in enumerate(myFile, 1):
      if line == (method + "\n"):
        return num
  return "error"

#
#def enhance_results(workdir, proj, bug):
#  for filename in os.listdir("{0}/result/".format(workdir)):
#    if filename.startswith("result_"):
#      result = ""
#      with open(workdir + "/result/" + filename, "r+") as myFile:
#        for num, line in enumerate(myFile, 1):
#          line = line[:-1]
#          result += line
#          if not num == 1:
#            print line
#          m = re.match(".*\t(.*)", line)
#          if m:
#            result += "\t" + str(get_line(workdir, proj, bug, m.group(1)))
#        result += "\n"
#    myFile.seek(0)
#    myFile.write(result)
#    myFile.truncate()
#
#
#def score(workdir, proj, bug):
#  score = -1
#  with open("{0}/data/info/{1}/{2}/real".format(workdir, proj, bug)) as f:
#    reals = map(lambda x: x[:-1], f.readlines())
#  print reals
#  with open(workdir + "/result.txt", "r+") as myFile:
#    for num, line in enumerate(myFile, 1):
#      chunks = line.split("\t")
#      if len(chunks) < 2:
#        continue
#      method = chunks[1][:-1]
#      if method in reals:
#        score = num
#        break
#  if score == -1:
#    raise ValueError("Real fault not in results");
#  print "Score of {0} {1}: {2}".format(proj, bug, score)
#  with open(workdir + "/score", "w+") as f:
#    f.write(str(score) + "\n")
