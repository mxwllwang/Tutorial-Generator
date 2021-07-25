import sys

# Represents one error message
class CompilerError:
    
    def __init__(self, problem):
        self.line = problem['line']
        self.message = problem['msg']
        self.context = problem['context']
        self.type = problem['type']

    def print_error():
        print('On line ', self.line, ', ', self.message, ': ', self.context, ' (', self.type, ')') 
        



    
