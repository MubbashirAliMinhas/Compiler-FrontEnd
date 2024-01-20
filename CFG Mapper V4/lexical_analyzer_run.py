import re

# value part: class part
keywords = {'social': 'access_modifier', 'secure': 'access_modifier', 'secret': 'access_modifier',
            'int': 'primitive_type', 'float': 'primitive_type', 'bool': 'primitive_type', 'char': 'primitive_type',
            'continue': 'continue_break', 'break': 'continue_break', 'default': 'default',
            'str': 'str', 'if': 'if', 'else': 'else', 'match': 'match', 'case': 'case', 'while': 'while', 'for': 'for', 'func': 'func', 
            'void': 'void', 'return': 'return', 'type': 'type', 'make': 'make', 'self': 'self', 'grand': 'grand', 'enhances': 'enhances',
            'abstract': 'abstract', 'const': 'const', 'passive': 'passive', 'as': 'as', 'constructor': 'constructor',
            'try': 'try', 'except': 'except', 'finally': 'finally', 'raise': 'raise', 'null': 'null', 'main': 'main', 'in': 'in'}

operators = {'+': 'PM', '-': 'PM',
             '*': 'MDM', '/': 'MDM', 
             '%': 'MDM', '^': '^',
             '+=': 'compound_assignment', '-=': 'compound_assignment', '*=': 'compound_assignment', 
             '/=': 'compound_assignment', '%=': 'compound_assignment', '^=': 'compound_assignment', 
             '==': 'relational', '!=': 'relational', '<': 'relational', '>': 'relational', '<=': 'relational', '>=': 'relational', 
             '..': 'range', '..<': 'range', 
             '++': 'inc_dec', '--': 'inc_dec', 
             '!': '!', '||': '||', '&&': '&&', '=': '='}

punctuators = ('.', ',', ':', ';', '(', ')', '{', '}', '[', ']', '->')

is_identifier = '(_+[A-Za-z0-9]|[A-Za-z])[_A-Za-z0-9]*'
is_integer = '[0-9]+'
is_float = '[0-9]*[.][0-9]+'
is_bool = {'true': 'bool_const', 'false': 'bool_const'}

# operators
opr_set1 = '[-][=-]?'
opr_set2 = '\.\.<|\.\.'
opr_set3 = '[+][+=]?'
opr_set4 = '[*/%^=<>!]?='
opr_set5 = '[*/%^=<>!]'
opr_set6 = '&&|[|][|]'

is_operator = f'{opr_set1}|{opr_set2}|{opr_set3}|{opr_set4}|{opr_set5}|{opr_set6}'

# punctuators
punc_set1 = '->'
punc_set2 = '[.,:;(){\}\[\]]'

# not yet decided
comment = '~[^\n]*'
multi_line = '/~.*~/'

def is_char():
    A = "\\\\[\\\\'ntrb]"
    B = "[^\\\\'\n]"
    return f"'({A}|{B})'"

def is_string():
    A = '\\\\[\\\\"ntrb]'
    B = '[^\\\\"\n]'
    return f'"({A}|{B})*"'

tokens = []

class Token:
    def __init__(self, class_part, value_part, line_no):
        self.class_part = class_part
        self.value_part = value_part
        self.line_no = line_no
    
    def __repr__(self):
        return f'{self.class_part}#{self.value_part}#{self.line_no}'

class BreakWord:
    def __init__(self, file):
        self.matcher = None
        self.temp = ''
        self.index = 0
        self.file = file
        self.line_no = 1

    def match_index(self, pattern):
        compile_pattern = re.compile(pattern)
        self.matcher = compile_pattern.match(self.file, self.index)
        return self.matcher
    
    def match_temp(self, pattern):
        compile_pattern = re.compile(pattern)
        self.matcher = compile_pattern.match(self.temp, 0)
        return self.matcher
    
    def dispatch_pattern(self):
        self.temp = self.file[self.matcher.start():self.matcher.end()]
        self.index = self.matcher.end()
    
    def dispatch_normal(self):
        self.temp = self.file[self.index:self.index + 1]
        self.index += 1

    def break_word(self):
        self.temp = ''
        if self.match_index(is_float):
            self.dispatch_pattern()
            if self.match_index('[_A-Za-z0-9]+'):
                self.temp += self.file[self.index:self.matcher.end()]
                self.index = self.matcher.end()
                tokens.append(Token('invalid', self.temp, self.line_no))
            else:
                tokens.append(Token('float_const', self.temp, self.line_no))
        elif self.match_index(is_integer):
            self.dispatch_pattern()
            if self.match_index('[_A-Za-z0-9]+'):
                self.temp += self.file[self.index:self.matcher.end()]
                self.index = self.matcher.end()
                tokens.append(Token('invalid', self.temp, self.line_no))
            else:
                tokens.append(Token('int_const', self.temp, self.line_no))
        elif self.match_index(is_identifier):
            self.dispatch_pattern()
            if self.temp in keywords:
                tokens.append(Token(keywords[self.temp], self.temp, self.line_no))
            elif self.temp in is_bool:
                tokens.append(Token(is_bool[self.temp], self.temp, self.line_no))
            else:
                tokens.append(Token('ID', self.temp, self.line_no))
        elif self.match_index("'"):
            self.dispatch_pattern()
            initial_index = self.index
            i = initial_index
            while i < len(self.file):
                if self.file[i] == '\n':
                    break
                elif self.file[i:i + 2] == "\\'":
                    i += 1
                elif self.file[i] == "'":
                    i += 1
                    break
                i += 1
            self.index = i
            self.temp += self.file[initial_index:self.index]
            if self.match_temp(is_char()):
                tokens.append(Token('char_const', self.temp, self.line_no))
            else:
                tokens.append(Token('invalid', self.temp, self.line_no))
        elif self.match_index('"'):
            self.dispatch_pattern()
            initial_index = self.index
            i = initial_index
            while i < len(self.file):
                if self.file[i] == '\n':
                    break
                elif self.file[i:i + 2] == '\\"':
                    i += 1
                elif self.file[i] == '"':
                    i += 1
                    break
                i += 1
            self.index = i
            self.temp += self.file[initial_index:self.index]
            if self.match_temp(is_string()):
                tokens.append(Token('str_const', self.temp, self.line_no))
            else:
                tokens.append(Token('invalid', self.temp, self.line_no))
        elif self.match_index(' +'):
            self.index = self.matcher.end()
        elif self.match_index('~[^\n]*'):
            self.index = self.matcher.end()
        elif self.match_index('/~'):
            state = True
            for i in range(self.matcher.end(), len(self.file)):
                if self.file[i] == '\n':
                    self.line_no += 1
                elif self.file[i:i + 2] == '~/':
                    self.index = i + 2
                    state = False
                    break
            if state:
                self.temp = self.file[self.index:]
                self.index = len(self.file)
                tokens.append(Token('invalid', self.temp, self.line_no))
        elif self.match_index(punc_set1):
            self.dispatch_pattern()
            tokens.append(Token(self.temp, self.temp, self.line_no))
        elif self.match_index(is_operator):
            self.dispatch_pattern()
            tokens.append(Token(operators[self.temp], self.temp, self.line_no))
        elif self.match_index(punc_set2):
            self.dispatch_normal()
            tokens.append(Token(self.temp, self.temp, self.line_no))
        elif self.match_index('\n'):
            self.line_no += 1
            self.index += 1
        else:
            self.dispatch_normal()
            tokens.append(Token('invalid', self.temp, self.line_no))
        return self.temp, self.index


with open('source_file.txt', 'r') as file:
    file = file.read()
    break_word = BreakWord(file)
    while break_word.index < len(file):
        temp, index = break_word.break_word()

with open('tokens.txt', 'w') as file:
    for i in range(len(tokens)):
        file.write(repr(tokens[i]) + '\n')
    file.write(repr(Token('$', '$', break_word.line_no)))

from cfg_src import CFG

cfg = CFG()

print(cfg.validate())