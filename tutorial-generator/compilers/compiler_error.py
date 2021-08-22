import sys
import re

# Represents one error message
class CompilerError:

    IgnoreCategoriesMask = 0xFFFFFF
    
    def __init__(self, problem):
        self.id = problem['id']
        self.line = problem['line']
        self.message = problem['msg']
        self.context = problem['context']
        self.type = problem['type']
        self.start = problem['charStart']
        self.end = problem['charEnd']
        self.args = problem['arguments']

    # Debugging purposes: print to console and return text representation of error message
    def get_error(self):
        error ='[' + str(self.get_id()) + '] On line ' + self.line + ', from ' + self.start + ' to ' + self.end + ' (' + self.context + ') :: ' + self.message + ' (' + self.type + ')' 
        print (error)
        return error

    # return parsed ID
    def get_id(self): # Return true ID of problem, without consideration of category
        return CompilerError.IgnoreCategoriesMask & int(self.id)

    def get_line(self):
        return self.line

    def get_message(self):
        return self.message

    def get_context(self):
        return self.context

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_args(self):
        return self.args

    # Get tutorial with filled in arguments from general tutorial template
    # Tutorial key: $x$ Parameter, $cxt$ Context, $start$ Start, $end$ End, $ln$ Line
    # Example tutorial: Insert {0} at {end}
    def get_tutorial(self, tutorial):
        # Match special indicators
        tutorial = tutorial.\
            replace("$cxt$", self.context).\
            replace("$start$", self.start).\
            replace("$end$", self.end).\
            replace("$ln$", self.line)
        # Match error arguments
        pattern = re.compile('\$([0-9]+)\$') # TODO: Currently matches numbers such as $234$
        for indicator in re.findall(pattern, tutorial):
            print("indicator", indicator)
            # arg_number = int(indicator.replace("$", ""))
            tutorial = tutorial.replace('$' + indicator + '$', self.args[int(indicator)])
        return tutorial
        
        
    
