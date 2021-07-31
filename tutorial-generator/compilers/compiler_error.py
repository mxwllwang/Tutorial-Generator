import sys

# Represents one error message
class CompilerError:
    
    def __init__(self, problem):
        self.line = problem['line']
        self.message = problem['msg']
        self.context = problem['context']
        self.type = problem['type']

    # print to console and return text representation of error message
    def get_error(self):
        error = 'On line ' + self.line + ', ' + self.message + ': ' + self.context + ' (' + self.type + ')' 
        print (error)
        return error
    
