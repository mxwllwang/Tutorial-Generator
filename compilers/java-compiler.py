import sys
import os
import shutil

directory = './compilers' # ?
package = './sample-files' # location of java file
file = 'test.java' # name of java file

# the variables are set for other purposes, it should be self-explaining
from subprocess import call
f = open(directory + '/' + 'console.log', "w")
fe =  open(directory + '/' + 'errorconsole.log', "w")

print('Current working directory: ', os.getcwd())
print('Directory ', directory)
classpath = './sample-files' # currently using this
srcPathList = './sample-files'


print("java",  "-jar", "./lib/ecj-4.20.jar", "-source", "1.8", "-target", "1.8", "-encoding", "utf8", "-cp", classpath, "-log", os.path.join(directory, "log.xml"),  "-d",  directory, file)
tool = call(["java",  "-jar", "./lib/ecj-4.20.jar", "-source", "1.8", "-target", "1.8", "-encoding", "utf8", "-cp", classpath, "-log", os.path.join(directory, "log.xml"),  "-d",  directory, file]
, stdout=f, stderr=fe, cwd=os.getcwd())

import xml.etree.ElementTree as ET
tree = ET.parse('./log.xml')
# tree = ET.parse(directory + "/log.xml")
root = tree.getroot()
m = dict()
all = []

status = 'ok'

for src in root.findall('.//problems/..'):
    problemsInSrc = dict()
    print(src.get('path'))
    problemsInSrc['src'] = SEPARATOR + SEPARATOR.join(src.get('path').split('/')[6:])

    problems = []
    for problem in src.find('problems'):
        prob = dict()
        if problem.get('severity') == 'ERROR':
            status = 'compileerror'

        prob['line'] = problem.get('line')
        prob['msg'] = problem.find('message').get('value')
        prob['context'] = problem.find('source_context').get('value')
        prob['type'] = problem.get('severity')
        problems.append(prob)

    problemsInSrc['problems'] = problems

    all.append(problemsInSrc)

m['status'] = status
m['src'] = all
