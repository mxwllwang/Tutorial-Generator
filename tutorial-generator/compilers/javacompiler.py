import sys
import os
import shutil
from compilers.compiler_error import CompilerError

directory = './compilers' # place to put console, errorconsole, log.xml
classpath = '../sample-files' # currently using this
logpath = os.path.join(directory, 'log.xml')
compilerpath = '../lib/ecj-4.20.jar'

# Input: file, which is expected to be in ./sample-files
# Output: a dict containing information about all the errors
def java_compile(file):


    filepath = os.path.join(classpath, file)

    print('\tlogpath exists:', os.path.exists(logpath))
    print('\tlogpath abspath', os.path.abspath(logpath))
    print('\tfilepath exists:', os.path.exists(filepath))
    print('\tfilepath abspath', os.path.abspath(filepath))
    
    print("\tfilepath = ", filepath)
    # the variables are set for other purposes, it should be self-explaining
    from subprocess import call
    f = open(os.path.join(directory, 'console.log'), "w")
    fe =  open(os.path.join(directory, 'errorconsole.log'), "w")

    print('\tCurrent working directory: ', os.getcwd())
    print('\tDirectory ', directory)

    # Try simplified version
    print("java", "-jar", compilerpath, "-log", logpath, filepath)
    tool = call(["java", "-jar", compilerpath, "-log", logpath, filepath], stdout=f, stderr=fe, cwd=os.getcwd())

    # tool = call(["java",  "-jar", "./lib/ecj-4.20.jar", "-source", "1.8", "-target", "1.8", "-encoding", "utf8", "-cp", classpath, "-log", os.path.join(directory, "log.xml"),  "-d",  directory, file]
    # , stdout=f, stderr=fe, cwd=os.getcwd())

    import xml.etree.ElementTree as ET
    print("\tlogpath =", logpath)
    tree = ET.parse(logpath)
    root = tree.getroot()
    m = dict()
    all_problems = []

    status = 'ok'
    SEPARATOR = '$'

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
            # print('\t', problem)
            # print('\t', prob)
            error = CompilerError(prob)
            problems.append(error)
            # problems.append(prob)
        all_problems += problems
        # problemsInSrc['problems'] = problems
        # print('\tproblemsInSrc ', problemsInSrc)

        # all.append(problemsInSrc)
    print(all_problems)
    return all_problems

    # m['status'] = status
    # m['src'] = all
    # print('\tm ', m)
    # return m

