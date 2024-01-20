init_code = """from token_reader import TokenReader

class CFG:
    def __init__(self):
        self.tokens = TokenReader()

    def validate(self):
        self.tokens.next_line()
        if self.lang():
            if self.tokens.class_part == '$':
                return True
        return False

    def terminal_check(self, token):
        if self.tokens.class_part == token:
            self.tokens.next_line()
            return True
    
    def match_all(self, token_list):
        for token in token_list:
            if self.tokens.class_part == token:
                return True
        return False

"""

from cfg import selection
selection_set = selection()

def tab(amount=1):
    return '    ' * amount

with open('cfg.txt', 'r') as file, open ('cfg_src.py', 'w') as py_file:
    py_file.write(init_code)
    j = 0
    while True:
        line = file.readline()
        if line == '':
            break
        i = 1
        fn_name = ''
        tabs = tab()
        while line[i] != '>':
            fn_name += line[i]
            i += 1
        py_file.write(f'{tabs}def {fn_name}(self):\n')
        tabs += tab()
        el = ''
        i += 5
        k = 0
        non_terminal_state = True
        while i < len(line) and line[i] != '\n':
            else_state = False
            if line[i] == '<':
                i += 1
                fn_call = ''
                while line[i] != '>':
                    fn_call += line[i]
                    i += 1
                i += 1
                if non_terminal_state:
                    string_list = selection_set[fn_name][k]
                    non_terminal_state = False
                    k += 1
                    py_file.write(f'{tabs}{el}if self.match_all({string_list}):\n')
                    tabs += tab(1)
                    py_file.write(f'{tabs}if self.{fn_call}():\n')
                else:
                    py_file.write(f'{tabs}{el}if self.{fn_call}():\n')
                tabs += tab()
                el = ''
            elif line[i] == '|':
                non_terminal_state = True
                i += 1
                py_file.write(f'{tabs}return True\n')
                tabs = tab(2)
                el = 'el'
            elif line[i] == 'Ï':
                string_list = selection_set[fn_name][k]
                i += 2
                tabs = tab(2)
                py_file.write(f'{tabs}elif self.match_all({string_list}):\n')
                py_file.write(f'{tab()}{tabs}return True\n')
                py_file.write(f'{tabs}return False\n\n')
                else_state = True
            else:
                non_terminal_state = False
                token = ''
                while i < len(line) and line[i] != ' ' and line[i] != '<' and line[i] != '|' and line[i] != '\n':
                    token += line[i]
                    i += 1
                if i < len(line) and line[i] == ' ':
                    i += 1
                if token == 'or':
                    token = '||'
                py_file.write(f"{tabs}{el}if self.terminal_check('{token}'):\n")
                py_file.write(f"{tabs}{tab()}self.tokens.next_line()\n")
                tabs += tab()
                el = ''
        if not else_state:
            py_file.write(f'{tabs}return True\n')
            py_file.write(f'{tab(2)}return False\n\n')
        else:
            py_file.write('\n')
