# -*- coding: utf-8 -*-


import re
import sys
import subprocess
import platform
import random
import string


class Tester:

    def __init__(self, userfilename, inputs, correct_outputs, input_variables, 
                 resultcode, checkcode, func = None):

        self.errors = 0

        self.userfilename = userfilename
        self.testerfilename = "__testcode__"

        self.lines = open(self.userfilename, encoding="utf8").readlines()
        self.firstline = 0
        self.lastline  = len(self.lines)-1

        self.inout = list(zip(inputs, correct_outputs))
        
        self.input_variables = input_variables
        self.resultcode = resultcode
        self.checkcode = checkcode
        self.func = func

    def addDecoratorCode(self, f):
        f.write("# start decorator code\n")
        f.write('''
class MyT(tuple):
    def __eq__(self,other):
        return (other == self[0]) if len(self) > 0 else Flase

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
                    result = MyT((result, recursive, admin_info))
                    result.__setattr__('recursive', recursive)
                    result.__setattr__('admin_info', admin_info)
            finally:
                if counter != 1:
                    recursive = True
                counter -= 1
            return result
        return wrapper
        
    return real_decorator
    
def check_recursive(result, expected):
    return hasattr(result, 'recursive') and result.recursive == expected

def chec_function(result, expected):
    return hasattr(result, 'admin_info') and result.admin_info == expected

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
        
        for i in range(self.firstline, self.lastline+1):

            l = self.lines[i]

            input_command = False
            
            
            # Get the list of input variable names in order to join them
            # within regular expression below
            unzip = lambda v: zip(*v)
            v = list(list(unzip(self.input_variables))[0])
            print(v)
            
            # for future maybe
            #v = self.input_variables.keys()

            regexp = '('+'|'.join(v)+").*input.*"
            print(regexp)
            match = re.match(regexp, l)
            if re.search("^\s*#", l):
                continue
            if match:
                match_name = (match.group(0).split('=')[0]).strip()
                print(f"match_name: {match_name}")
                k = v.index(match_name)
                print(f"k: {k}")
                print(f"inout: {inout}")
                print(f"inout[0][0]: {inout[0][0]}")
                indatum = inout[0][k]
                f.write('input = lambda s: str({})\n'.format(indatum))
                f.write(l +"\n")
            
            elif re.match(".*input.*", l):
                rd = ''.join(random.choice(string.digits) for x in range(1000))
                # rd = ''.join(random.choice(string.printable) for x in range(1000))
                f.write('input = lambda s: str("{}")\n'.format(rd))
                f.write(l +"\n")
            
            elif re.match(".*exit.*", l):
                continue
            
            elif self.func and re.match('def\s*' + self.func[0] + '.*', l):
                f.write("@__decorator__('{}')\n".format(self.func[0]))
                f.write(l +"\n")
            else:
                f.write(l +"\n")

        f.write("# end user code\n")
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
            s.append("elif not (check_function(output, '{}')):".format(self.func[0]))
            s.append('    print("ERROR on input {input}\\nThe result should be calculated by calling function \'' + self.func[0] + '\'")')
            s.append('    sys.exit(1)')
            if self.func[1] != None:
                s.append("elif not (check_recursive(output, {})):".format(self.func[1]))
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

    # If there is no command line argument the user file name
    # is that of tester with the word "tester" replaced by "user".
    userfilename = __file__.replace("tester", "user")

    if len(sys.argv) > 1:
        userfilename = sys.argv[1]

    inputs = [
    '0',
    '10',
    '30',
    ]
    correct_outputs = [
    "1",
    "3628800",
    "265252859812191058636308480000000"
    ]

    # names of input variables
    input_variables = [
        ('N','int')
    ]

    #func = None            # no function needed
    #func = ('name', True)  # there should be a recursive function 'name'
    #func = ('name', False) # there should be a non recursive function 'name'
    #func = ('name', None)  # there should be a function 'name' (either recursive or not)
    
    func = ('myfact', True)

    # how to get result
    resultcode = ['output=result']
    
    # How to verify that result is correct
    checkcode='''
def check(output,correct_output):
    True
    return output == correct_output
'''

    tester = Tester(userfilename, inputs, correct_outputs, 
                    input_variables, resultcode, checkcode, func)

    tester.runTests()
    
    if tester.allCorrect():
        print( "****** The program has run correctly in all cases.")
        sys.exit(0)
    else:
        print(f"****** The program has run in error in {tester.errors} cases.")
        print(f"Your grade is {(len(correct_outputs)-tester.errors)*10/tester.errors}.")
        sys.exit(tester.errors)


if __name__ == '__main__':
    main()
