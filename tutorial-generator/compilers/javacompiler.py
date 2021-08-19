import sys
import os
import shutil
from compilers.compiler_error import CompilerError

compilerpath = '../lib/ecj-4.20.jar'

# Input:
#   filepath - working-folder for specific user
#   directory - place to put console, errorconsole, log.xml    
# Output: a dict containing information about all the errors
def java_compile(filename, directory):
    
    logpath = os.path.join(directory, 'log.xml')
    filepath = os.path.join(directory, filename)
    
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
    # jar file option -log
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

            # Raw problem ID
            prob['id'] = problem.get('problemID')
            # Location of problem
            prob['line'] = problem.get('line')
            prob['charStart'] = problem.get('charStart')
            prob['charEnd'] = problem.get('charEnd')
            # Actual problematic code
            prob['context'] = problem.find('source_context').get('value')
            # Generated error message
            prob['msg'] = problem.find('message').get('value')
            prob['type'] = problem.get('severity')
            # Arguments to the error. Parses through each and adds to list
            arguments = []
            for argument in problem.find('arguments'):
                arguments.append(argument.get('value'))
            prob['arguments'] = arguments

            # Finished parsing information from xml
            error = CompilerError(prob)
            problems.append(error)

        all_problems += problems

    print(all_problems)
    return all_problems
