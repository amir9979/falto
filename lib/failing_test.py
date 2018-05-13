from util import cmd
import re
import os

# Return all failing tests in that version
def get_with_lines(workdir, proj, bug):
  def transform(x):
    print "transform " + x
    return translate_method(workdir, proj, bug, x)
  return list(set(map(transform, get_raw(workdir, proj, bug))))


def get_raw(workdir, proj, bug):
  output = cmd("{0}/defects4j/framework/bin/defects4j info -p {1} -b {2}".format(workdir, proj, bug))
  tests = re.findall("""Root cause in triggering tests:
(.*)
--------------------------------------------------------------------------------
List of modified sources:""", output, re.DOTALL)[0].split('\n')
  tests = filter(lambda x: x.startswith(' - '), tests)
  return map(lambda x: x.replace(' - ', ''), tests)


def get_line(workdir, test):
#  with open(workdir + '/result/cg/lines.csv') as myFile:
  with open(workdir + '/result/lines.csv') as myFile:
    for num, line in enumerate(myFile, 1):
#      m = re.match("{0};([0-9]+)".format(test), line)
      m = re.match("{0}; ([0-9]+)".format(test), line)
      if m:
        return m.group(1)
  return None


def translate_method(workdir, proj, bug, test):
  clazz, _, method = test.partition('::')
  line = get_line(workdir, test)
  if line != None:
    return clazz + "#" + line

  print "Could not find line of " + test
  srcdir = "{0}/data/{1}/{2}b/src/test/".format(workdir, proj, bug)
  if os.path.isdir(srcdir + "java/"):
    srcdir = srcdir + "java/"

  clazzname = clazz.rsplit('.', 1)[-1]
  regex = ".*public class {0} extends (.+)".format(clazzname) + " {"
  with open(srcdir + clazz.replace('.', '/') + '.java') as myFile:
    for line in myFile:
      if "extends" in line:
        print "Check line " + line
      m = re.match(regex, line)
      if m:
        if "TestCase" != m.group(1):
          print "Try parent class " + m.group(1)
          # TODO might not be in the same package
          line = get_line(workdir, clazz.rsplit('.', 1)[0] + '.' + m.group(1) + "::" + method)
          if line != None:
            return clazz + "#" + line
  if test.startswith("org.apache.commons.lang.LocaleUtilsTest::") and proj == "Lang" and bug == "57":
    return translate_method(workdir, proj, bug, "org.apache.commons.lang.LocaleUtilsTest::setUp")

  raise ValueError('Could not find test ' + test)
