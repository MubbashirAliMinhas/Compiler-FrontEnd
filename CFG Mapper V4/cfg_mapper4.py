from selection_set import gen_selection_set
from first_follow import cfg_ds
from reconstruct_cfg import null

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

selection_set = gen_selection_set()

# for key, value in selection_set.items():
#     print(key, value)

# for key, value in cfg_ds.items():
#     print(key, value)

def tab(amount=1):
    return '    ' * amount

with open ('cfg_src.py', 'w') as py_file:
    py_file.write(init_code)
    # i = 0
    for key, value in cfg_ds.items():
        key = key.strip('<>')
        py_file.write(f'{tab()}def {key}(self):\n')
        k = 0
        for x in range(len(value)):
            rules = value[x]
            tabs = tab(2)
            el = ''
            if x != 0:
                el = 'el'
            for y in range(len(rules)):
                item = rules[y]
                if item[0] == '<':
                    item = item.strip('<>')
                    if y == 0:
                        py_file.write(f'{tabs}{el}if self.match_all({selection_set[key][k]}):\n')
                        tabs += tab()
                        py_file.write(f'{tabs}if self.{item}():\n')
                        tabs += tab()
                        k += 1
                    else:
                        py_file.write(f'{tabs}if self.{item}():\n')
                        tabs += tab()
                elif item == null:
                    py_file.write(f'{tabs}elif self.match_all({selection_set[key][k]}):\n')
                    tabs += tab()
                    k += 1
                else:
                    if x == 0 or y:
                        py_file.write(f"{tabs}if self.terminal_check('{item}'):\n")
                        tabs += tab()
                    else:
                        py_file.write(f"{tabs}{el}if self.terminal_check('{item}'):\n")
                        tabs += tab()
                        
            py_file.write(f'{tabs}return True\n')
        py_file.write(f'{tab(2)}return False\n\n')
        # i += 1
        # if i == 5:
        #     break
