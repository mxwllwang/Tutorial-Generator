import sys
import os
import shutil

directory = './compilers' # ?
classpath = './sample-files' # currently using this
file = 'test.java' # name of java file
filepath = classpath + '/' + file

# Input: file, which is expected to be in ./sample-files
# Output: a dict containing information about all the errors
def java_compile(file):

    # the variables are set for other purposes, it should be self-explaining
    from subprocess import call
    f = open(directory + '/' + 'console.log', "w")
    fe =  open(directory + '/' + 'errorconsole.log', "w")

    print('\tCurrent working directory: ', os.getcwd())
    print('\tDirectory ', directory)

    # Try simplified version
    print("java", "-jar", "./lib/ecj-4.20.jar", "-log", os.path.join(directory, "log.xml"), filepath)
    tool = call(["java", "-jar", "./lib/ecj-4.20.jar", "-log", os.path.join(directory, "log.xml"), filepath], stdout=f, stderr=fe, cwd=os.getcwd())

    # tool = call(["java",  "-jar", "./lib/ecj-4.20.jar", "-source", "1.8", "-target", "1.8", "-encoding", "utf8", "-cp", classpath, "-log", os.path.join(directory, "log.xml"),  "-d",  directory, file]
    # , stdout=f, stderr=fe, cwd=os.getcwd())

    import xml.etree.ElementTree as ET
    tree = ET.parse('./compilers/log.xml')
    # tree = ET.parse(directory + "/log.xml")
    root = tree.getroot()
    m = dict()
    all = []

    status = 'ok'

    SEPARATOR = 'SEPARATOR'

    for src in root.findall('.//problems/..'):
        problemsInSrc = dict()
        print('\tSrc path ', src.get('path'))
        problemsInSrc['src'] = SEPARATOR + SEPARATOR.join(src.get('path').split('/')[6:])

        problems = []
        for problem in src.find('problems'):
            prob = dict()
            if problem.get('severity') == 'ERROR': # Confirm that its a compiler error
                status = 'compileerror'

            prob['line'] = problem.get('line')
            prob['msg'] = problem.find('message').get('value')
            prob['context'] = problem.find('source_context').get('value')
            prob['type'] = problem.get('severity')
            print('\t', problem)
            print('\t', prob)
            problems.append(prob)

        problemsInSrc['problems'] = problems
        print('\tproblemsInSrc ', problemsInSrc)

        all.append(problemsInSrc)

    m['status'] = status
    m['src'] = all

    print('\tm ', m)
    
    return m

