# -*- coding: utf-8 -*-


####   ΜΗ ΠΕΙΡΑΖΕΤΕ ΑΥΤΟ ΤΟ ΑΡΧΕΙΟ ####

####
#### Πρόγραμμα ελέγχου του προγράμματος που γράφουν οι φοιτητές. Μη πειράζετε αυτό το πρόγραμμα.
#### Γράφετε το πρόγραμμά σας στο αρχείο E04-07-user.py και μόνο εκεί.
####

import re
import sys
import subprocess
import ast
import platform
import random
import string


class Tester:

    def __init__(self, userfilename, inputs, correct_outputs, input_variables, 
                 resultcode, checkcode, func = None):

        self.errors = 0

        self.userfilename = userfilename
        self.testerfilename = "__testcode__"

        # self.lines = open(self.userfilename, encoding="utf8").readlines()
        self.usercode = open(self.userfilename, 'r', encoding='utf8').read()
        # self.firstline = 0
        # self.lastline  = len(self.lines)-1

        self.inout = list(zip(inputs, correct_outputs))
        
        self.input_variables = input_variables
        self.resultcode = resultcode
        self.checkcode = checkcode
        self.func = func

    def addDecoratorCode(self, f):
        f.write("# start decorator code\n")
        f.write('''class ObjectProxy:
    __slots__ = ('__wrapped__', '__recursive__', '__admin__') 
    def __init__(self, wrapped, recursive, admin):
        object.__setattr__(self, '__wrapped__', wrapped)
        object.__setattr__(self, '__recursive__', recursive)
        object.__setattr__(self, '__admin__', admin)
        try:
            object.__setattr__(self, '__qualname__', wrapped.__qualname__)
        except AttributeError:
            pass
    @property
    def __name__(self):
        return self.__wrapped__.__name__
    @__name__.setter
    def __name__(self, value):
        self.__wrapped__.__name__ = value
    @property
    def __class__(self):
        return self.__wrapped__.__class__
    @__class__.setter
    def __class__(self, value):
        self.__wrapped__.__class__ = value
    @property
    def __annotations__(self):
        return self.__wrapped__.__annotations__
    @__annotations__.setter
    def __annotations__(self, value):
        self.__wrapped__.__annotations__ = value
    def __dir__(self):
        return dir(self.__wrapped__)
    def __str__(self):
        return str(self.__wrapped__)
    if sys.version_info[0] == 3:
        def __bytes__(self):
            return bytes(self.__wrapped__)
    def __repr__(self):
        return '<{} at 0x{:x} for {} at 0x{:x}>'.format(
                type(self).__name__, id(self),
                type(self.__wrapped__).__name__,
                id(self.__wrapped__))
    def __reversed__(self):
        return reversed(self.__wrapped__)
    if sys.version_info[0] == 3:
        def __round__(self):
            return round(self.__wrapped__)
    def __lt__(self, other):
        return self.__wrapped__ < other
    def __le__(self, other):
        return self.__wrapped__ <= other
    def __eq__(self, other):
        return self.__wrapped__ == other
    def __ne__(self, other):
        return self.__wrapped__ != other
    def __gt__(self, other):
        return self.__wrapped__ > other
    def __ge__(self, other):
        return self.__wrapped__ >= other
    def __hash__(self):
        return hash(self.__wrapped__)
    def __nonzero__(self):
        return bool(self.__wrapped__)
    def __bool__(self):
        return bool(self.__wrapped__)
    def __setattr__(self, name, value):
        if name.startswith('_self_'):
            object.__setattr__(self, name, value)
        elif name == '__wrapped__':
            object.__setattr__(self, name, value)
            try:
                object.__delattr__(self, '__qualname__')
            except AttributeError:
                pass
            try:
                object.__setattr__(self, '__qualname__', value.__qualname__)
            except AttributeError:
                pass
        elif name == '__qualname__':
            setattr(self.__wrapped__, name, value)
            object.__setattr__(self, name, value)
        elif hasattr(type(self), name):
            object.__setattr__(self, name, value)
        else:
            setattr(self.__wrapped__, name, value)
    def __getattr__(self, name):
        if name == '__wrapped__':
            raise ValueError('wrapper has not been initialised')
        return getattr(self.__wrapped__, name)
    def __delattr__(self, name):
        if name.startswith('_self_'):
            object.__delattr__(self, name)
        elif name == '__wrapped__':
            raise TypeError('__wrapped__ must be an object')
        elif name == '__qualname__':
            object.__delattr__(self, name)
            delattr(self.__wrapped__, name)
        elif hasattr(type(self), name):
            object.__delattr__(self, name)
        else:
            delattr(self.__wrapped__, name)
    def __add__(self, other):
        return self.__wrapped__ + other
    def __sub__(self, other):
        return self.__wrapped__ - other
    def __mul__(self, other):
        return self.__wrapped__ * other
    def __div__(self, other):
        return operator.div(self.__wrapped__, other)
    def __truediv__(self, other):
        return operator.truediv(self.__wrapped__, other)
    def __floordiv__(self, other):
        return self.__wrapped__ // other
    def __mod__(self, other):
        return self.__wrapped__ % other
    def __divmod__(self, other):
        return divmod(self.__wrapped__, other)
    def __pow__(self, other, *args):
        return pow(self.__wrapped__, other, *args)
    def __lshift__(self, other):
        return self.__wrapped__ << other
    def __rshift__(self, other):
        return self.__wrapped__ >> other
    def __and__(self, other):
        return self.__wrapped__ & other
    def __xor__(self, other):
        return self.__wrapped__ ^ other
    def __or__(self, other):
        return self.__wrapped__ | other
    def __radd__(self, other):
        return other + self.__wrapped__
    def __rsub__(self, other):
        return other - self.__wrapped__
    def __rmul__(self, other):
        return other * self.__wrapped__
    def __rdiv__(self, other):
        return operator.div(other, self.__wrapped__)
    def __rtruediv__(self, other):
        return operator.truediv(other, self.__wrapped__)
    def __rfloordiv__(self, other):
        return other // self.__wrapped__
    def __rmod__(self, other):
        return other % self.__wrapped__
    def __rdivmod__(self, other):
        return divmod(other, self.__wrapped__)
    def __rpow__(self, other, *args):
        return pow(other, self.__wrapped__, *args)
    def __rlshift__(self, other):
        return other << self.__wrapped__
    def __rrshift__(self, other):
        return other >> self.__wrapped__
    def __rand__(self, other):
        return other & self.__wrapped__
    def __rxor__(self, other):
        return other ^ self.__wrapped__
    def __ror__(self, other):
        return other | self.__wrapped__
    def __iadd__(self, other):
        self.__wrapped__ += other
        return self
    def __isub__(self, other):
        self.__wrapped__ -= other
        return self
    def __imul__(self, other):
        self.__wrapped__ *= other
        return self
    def __idiv__(self, other):
        self.__wrapped__ = operator.idiv(self.__wrapped__, other)
        return self
    def __itruediv__(self, other):
        self.__wrapped__ = operator.itruediv(self.__wrapped__, other)
        return self
    def __ifloordiv__(self, other):
        self.__wrapped__ //= other
        return self
    def __imod__(self, other):
        self.__wrapped__ %= other
        return self
    def __ipow__(self, other):
        self.__wrapped__ **= other
        return self
    def __ilshift__(self, other):
        self.__wrapped__ <<= other
        return self
    def __irshift__(self, other):
        self.__wrapped__ >>= other
        return self
    def __iand__(self, other):
        self.__wrapped__ &= other
        return self
    def __ixor__(self, other):
        self.__wrapped__ ^= other
        return self
    def __ior__(self, other):
        self.__wrapped__ |= other
        return self
    def __neg__(self):
        return -self.__wrapped__
    def __pos__(self):
        return +self.__wrapped__
    def __abs__(self):
        return abs(self.__wrapped__)
    def __invert__(self):
        return ~self.__wrapped__
    def __int__(self):
        return int(self.__wrapped__)
    def __long__(self):
        return long(self.__wrapped__)
    def __float__(self):
        return float(self.__wrapped__)
    def __complex__(self):
        return complex(self.__wrapped__)
    def __oct__(self):
        return oct(self.__wrapped__)
    def __hex__(self):
        return hex(self.__wrapped__)
    def __index__(self):
        return operator.index(self.__wrapped__)
    def __len__(self):
        return len(self.__wrapped__)
    def __contains__(self, value):
        return value in self.__wrapped__
    def __getitem__(self, key):
        return self.__wrapped__[key]
    def __setitem__(self, key, value):
        self.__wrapped__[key] = value
    def __delitem__(self, key):
        del self.__wrapped__[key]
    def __getslice__(self, i, j):
        return self.__wrapped__[i:j]
    def __setslice__(self, i, j, value):
        self.__wrapped__[i:j] = value
    def __delslice__(self, i, j):
        del self.__wrapped__[i:j]
    def __enter__(self):
        return self.__wrapped__.__enter__()
    def __exit__(self, *args, **kwargs):
        return self.__wrapped__.__exit__(*args, **kwargs)
    def __iter__(self):
        return iter(self.__wrapped__)
    def __copy__(self):
        raise NotImplementedError('object proxy must define __copy__()')
    def __deepcopy__(self, memo):
        raise NotImplementedError('object proxy must define __deepcopy__()')
    def __reduce__(self):
        raise NotImplementedError('object proxy must define __reduce_ex__()')
    def __reduce_ex__(self, protocol):
        raise NotImplementedError('object proxy must define __reduce_ex__()')
# Main decorator
import functools
def __decorator__(admin_info):
    def real_decorator(func):
        counter = 0
        recursive = False
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal counter
            nonlocal recursive
            try:
                counter += 1
                result = func(*args, **kwargs)
                if counter == 1: #non recursive call, decorate with admin info
                    result = ObjectProxy(result, recursive, admin_info)
            finally:
                if counter != 1:
                    recursive = True
                counter -= 1
            return result
        return wrapper
    return real_decorator
def __check_recursive__(result, expected):
    return hasattr(result, '__recursive__') and result.__recursive__ == expected
def __check_function__(result, expected):
    return hasattr(result, '__admin__') and result.__admin__ == expected
''')
        f.write("# end decorator code\n")

    def makeTestProgram(self, fname, inout):

        f = open(fname, 'w+', encoding="utf8")

        f.write("# -*- coding: utf-8 -*-\n")
        f.write("#### Checking file: {uf}\n".format(uf=self.userfilename))
        f.write("import sys\n")
        f.write("import platform\n")
        f.write("if platform.system() == 'Linux':\n")
        f.write("    import resource\n")
        f.write("    memory_limit = 100*2**20\n")
        f.write("    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, 2*memory_limit))\n")

        self.addDecoratorCode(f)
        f.write("# start user code\n")

        # Get import statements from usercode
        # and insert them in test code file
        code_tree = ast.parse(self.usercode)
        for node in ast.walk(code_tree):
            if isinstance(node, ast.Import) or \
                isinstance(node, ast.ImportFrom) or \
                isinstance(node, ast.alias):

                S = ast.get_source_segment(self.usercode, node)
                if S:
                    f.write(S)
                    f.write('\n')

        # Get functions definitions and insert them into file
        # Also get function names
        function_names = []
        for node in ast.walk(code_tree):
            if isinstance(node, ast.FunctionDef):
                function_names.append(node.name)
                S = ast.get_source_segment(self.usercode, node)
                if S:
                    f.write(f"@__decorator__('{node.name}')\n")
                    f.write(S)
                    f.write('\n')


        
#         for i in range(self.firstline, self.lastline+1):
#
#             l = self.lines[i]
#
#             #input_command = False
#
#
#             # Get the list of input variable names in order to join them
#             # within regular expression below
#             unzip = lambda v: zip(*v)
#             v = list(list(unzip(self.input_variables))[0])
#
#             # for future maybe
#             #v = self.input_variables.keys()
#
#             regexp = '('+'|'.join(v)+").*input.*"
#             match = re.match(regexp, l)
#             if re.search("^\s*#", l):
#                 continue
#             if match:
#                 match_name = (match.group(0).split('=')[0]).strip()
#                 k = v.index(match_name)
#                 indatum = inout[0][k]
#                 #f.write('input = lambda s: str({})\n'.format(indatum))
#                 f.write(f'''
# def input(*args, **kargs):
#     return str({indatum})
#
# ''')
#                 f.write(l +"\n")
#
#             elif re.match(".*input.*", l):
#                 rd = ''.join(random.choice(string.digits) for x in range(1000))
#                 # rd = ''.join(random.choice(string.printable) for x in range(1000))
#                 f.write('input = lambda s: str("{}")\n'.format(rd))
#                 f.write(l +"\n")
#
#             elif re.match(".*exit.*", l):
#                 continue
#
#             elif self.func and re.match('def\s*' + self.func[0] + '.*', l):
#                 f.write("@__decorator__('{}')\n".format(self.func[0]))
#                 f.write(l +"\n")
#             else:
#                 f.write(l +"\n")

        f.write("# end user code\n")
        # f.write(f"{str(inout[0][0])}, {str(inout[0][1])}")
        if function_names:
            f.write(f"result = {function_names[0]}({inout[0][0]}, {inout[0][1]})")
            f.write('\n')
        s = self.timeOutCode(self.resultcode)
        s = s + self.testCode(self.checkcode)
        additional_code = '\n'.join(s)
        f.write(additional_code.format(input=inout[0], correct_output=inout[1]))

        return fname

    def testCode(self, checkcode):

        s = []
        s.append(checkcode)
        s.append("if not check(output,{correct_output}):")
        ### s.append("if not ({check}):".format(check=checkcode))
        s.append('    print("ERROR on input {input}\\nOutput produced is \", output, \"\\nShould be {correct_output}\")')
        s.append('    sys.exit(1)')
        if self.func:
            s.append("elif not (__check_function__(output, '{}')):".format(self.func[0]))
            s.append('    print("ERROR on input {input}\\nThe result should be calculated by calling function \'' + self.func[0] + '\'")')
            s.append('    sys.exit(1)')
            if self.func[1] != None:
                s.append("elif not (__check_recursive__(output, {})):".format(self.func[1]))
                s.append('    print("ERROR on input {input}\\nFunction \'' + self.func[0] + '\' should ' + ("" if self.func[1] else "not ") + 'be recursive")')
                s.append('    sys.exit(1)')
        s.append("else:")
        s.append('    print("OK")')
        s.append('    sys.exit(0)')
        return s
    
    def timeOutCode(self, resultcode):

        # mycode is a list of strings
        
        s = []
        s.append("import signal")
        s.append("def _signal_handler(signum, frame):")
        s.append("    raise Exception('Timed out!')")
        s.append("\n")
        # Signal alarm is disabled because it works only on linux. 
        # It must be replaced by a threading/timer technique
        #s.append("if hasattr(signal, 'SIGALARM'):")
        s.append("if False:") 
        s.append("    signal.signal(signal.SIGALARM, _signal_handler)")
        s.append("    signal.alarm(3) # 3 seconds")
        s.append("    try:")
        for c in resultcode:
            s.append("        {resultcode}".format(resultcode=c))
        s.append("    except Exception as msg:")
        s.append("        print('Timed out!!')")
        s.append("else:")
        for c in resultcode:
            s.append("    {resultcode}".format(resultcode=c))

        return s

    
    def runTests(self):

        operating_system = platform.system()
        if operating_system == "Windows":
            python_command = "python"
        elif operating_system == "Linux":
            python_command = "python3"
        else:
            python_command = "python3"

        for i in range(len(self.inout)):

            print(' ')
            print("-------------------Case No %d------------------" % i)

            filename = self.makeTestProgram(self.testerfilename + str(i) + ".py", self.inout[i])
            #exit_status = subprocess.call([python_command, filename])
            exit_status = subprocess.call([sys.executable, filename])

            if exit_status == 0:
                print("---Case No %d: OK" % i)
            else:
                self.errors += 1
                print("---Case No %d: ERROR" % i)

            print(" ")

    def allCorrect(self):

        return not ( self.errors>0 )

def main():

    #problemName = __file__
    #userfilename = problemName + "-user.py"
    userfilename = __file__.replace("tester", "user")

    if len(sys.argv) > 1:
        userfilename = sys.argv[1]


    # The new idea is that tester is not given to the students.
    # So the code is (almost) arbitrary.
    # We need the user to create a function with specific interface.
    # So the requirement is that a user must write a function that 
    # solves a problem and the function must have 
    # a specific interface:
    #    - Number of parameters.
    #    - Type of each parameter.
    #    - The requested returned value.
    #
    # Also the function must be independent of global variables, with
    # the exception of any libraries needed (e.g. random, numpy, etc)
    #
    # The idea is that tester takes all functions to a new file
    # decorates one by one and runs the decorated function. 
    # If one of the runs gives the correct answer, then the program is
    # considered correct for the case.
    #
    # So there are no requirements for variable names or inputs etc.
    # There is only requirement for the main function interface.
    
    # An input is a list of inpur values.
    # Here we define a list of inputs.
    inputs = [
        (1,1),
        (10,20),
        (30,40)
    ]
    
    # This is a list of correct outputs wrapped by quotas.
    correct_outputs = [
    "2",
    "30",
    "70"
    ]

    ### This won't be needed anymore
    # names of input variables
    input_variables = [
        ('a', 'float'),
        ('b', 'float')
    ]

    #func = None            # no function needed
    #func = ('name', True)  # there should be a recursive function 'name'
    #func = ('name', False) # there should be a non recursive function 'name'
    #func = ('name', None)  # there should be a function 'name' (either recursive or not)
    
    func = ('myadd', None)

    # how to get result
    resultcode = ['output=result']
    
    # how to verify (False if it's OK)
    # checkcode = 'output == {correct_output}'
    checkcode='''
def check(output,correct_output):
    return output == correct_output
'''

    tester = Tester(userfilename, inputs, correct_outputs, 
                    input_variables, resultcode, checkcode, func)

    tester.runTests()

    grade = (len(inputs) - tester.errors)/len(inputs)*10
    print(f"Your grade is {grade}")
    # if tester.allCorrect():
        # print( "****** The program has run correctly in all cases.")
        # sys.exit(0)
    # else:
        # print("****** The program has run in error in some cases.")
        # sys.exit(1)


if __name__ == '__main__':
    main()
