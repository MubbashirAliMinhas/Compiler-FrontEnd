from token_reader import TokenReader

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
            return True
    
    def match_all(self, token_list):
        for token in token_list:
            if self.tokens.class_part == token:
                return True
        return False

    def var_fn_assign1(self):
        if self.match_all(['[']):
            if self.array_index():
                if self.var_fn_assign2():
                    return True
        elif self.match_all(['.', 'inc_dec', '=', 'compound_assignment']):
            if self.var_fn_assign2():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.var_fn_assign3():
                    return True
        return False

    def var_fn_assign2(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.var_fn_assign4():
                return True
        elif self.terminal_check('inc_dec'):
            self.tokens.next_line()
            return True
        elif self.match_all(['=', 'compound_assignment']):
            if self.equals():
                if self.assign1():
                    return True
        return False

    def var_fn_assign3(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.var_fn_assign4():
                return True
        elif self.match_all(['[']):
            if self.array_index():
                if self.var_fn_assign2():
                    return True
        elif self.match_all([';']):
            return True
        return False


    def var_fn_assign4(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.var_fn_assign1():
                return True
        return False

    def this_super(self):
        if self.terminal_check('self'):
            self.tokens.next_line()
            if self.terminal_check('.'):
                self.tokens.next_line()
                return True
        elif self.terminal_check('grand'):
            self.tokens.next_line()
            if self.terminal_check('.'):
                self.tokens.next_line()
                if self.terminal_check('ID'):
                    self.tokens.next_line()
                    if self.terminal_check('.'):
                        self.tokens.next_line()
                        return True
        return False

    def this_super1(self):
        if self.match_all(['(']):
            if self.args():
                return True
        elif self.terminal_check('.'):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.var_fn_assign1():
                    return True
        return False

    def assign1(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.assign2():
                return True
        elif self.match_all(['self', 'grand']):
            if self.this_super():
                if self.terminal_check('ID'):
                    self.tokens.next_line()
                    if self.assign2():
                        return True
        elif self.match_all(['(', '!', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'PM', 'make']):
            if self.exp1():
                return True
        elif self.terminal_check('inc_dec'):
            self.tokens.next_line()
            if self.var():
                if self.unpacked():
                    return True
        return False

    def exp1(self):
        if self.match_all(['(']):
            if self.B():
                if self.unpacked():
                    return True
        elif self.terminal_check('!'):
            self.tokens.next_line()
            if self.F():
                if self.unpacked():
                    return True
        elif self.match_all(['int_const', 'float_const', 'char_const', 'str_const', 'bool_const']):
            if self.const():
                if self.unpacked():
                    return True
        elif self.terminal_check('PM'):
            self.tokens.next_line()
            if self.F():
                if self.unpacked():
                    return True
        elif self.match_all(['make']):
            if self.obj_dec():
                return True
        return False

    def assign2(self):
        if self.match_all(['[']):
            if self.array_index():
                if self.assign3():
                    return True
        elif self.match_all(['.', '^', 'MDM', 'PM', 'relational', '&&', '||', 'inc_dec', 'as', '=', 'compound_assignment', ';']):
            if self.assign3():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.assign4():
                    return True
        return False

    def assign3(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.assign5():
                return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ';']):
            if self.unpacked():
                return True
        elif self.terminal_check('inc_dec'):
            self.tokens.next_line()
            if self.unpacked():
                return True
        elif self.terminal_check('as'):
            self.tokens.next_line()
            if self.type():
                if self.unpacked():
                    return True
        elif self.match_all(['=', 'compound_assignment']):
            if self.equals():
                if self.assign1():
                    return True
        return False

    def assign4(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.assign5():
                return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ';']):
            if self.unpacked():
                return True
        elif self.terminal_check('as'):
            self.tokens.next_line()
            if self.type():
                if self.unpacked():
                    return True
        elif self.match_all(['[']):
            if self.array_index():
                if self.assign3():
                    return True
        return False

    def assign5(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.assign2():
                return True
        return False

    def equals(self):
        if self.terminal_check('='):
            self.tokens.next_line()
            return True
        elif self.terminal_check('compound_assignment'):
            self.tokens.next_line()
            return True
        return False

    def dec(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.dec1():
                return True
        return False

    def dec1(self):
        if self.terminal_check(':'):
            self.tokens.next_line()
            if self.type():
                if self.dec2():
                    return True
        return False

    def dec2(self):
        if self.terminal_check('='):
            self.tokens.next_line()
            if self.dec3():
                return True
        elif self.match_all([';']):
            return True
        return False


    def dec3(self):
        if self.match_all(['ID', 'self', 'grand', '(', '!', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'PM', 'make', 'inc_dec']):
            if self.assign1():
                return True
        elif self.match_all(['[']):
            if self.array_dec():
                return True
        return False

    def for_st(self):
        if self.terminal_check('for'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.decs():
                    if self.terminal_check('in'):
                        self.tokens.next_line()
                        if self.iterator():
                            if self.terminal_check(')'):
                                self.tokens.next_line()
                                if self.body():
                                    return True
        return False

    def decs(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.terminal_check(':'):
                self.tokens.next_line()
                if self.type():
                    return True
        elif self.match_all(['[', ':']):
            if self.des_dec_ref():
                return True
        return False

    def des_dec_ref(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.des_dec_ref1():
                    if self.terminal_check(']'):
                        self.tokens.next_line()
                        if self.terminal_check(':'):
                            self.tokens.next_line()
                            if self.type():
                                return True
        return False

    def des_dec_ref1(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.des_dec_ref1():
                    return True
        elif self.match_all([']']):
            return True
        return False


    def iterator(self):
        if self.match_all(['ID', 'self', 'grand', '(', '!', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'PM', 'make']):
            if self.exp():
                if self.range1():
                    return True
        return False

    def range(self):
        if self.terminal_check('range'):
            self.tokens.next_line()
            if self.exp():
                if self.terminal_check(':'):
                    self.tokens.next_line()
                    if self.exp():
                        return True
        return False

    def range1(self):
        if self.match_all(['range']):
            if self.range():
                return True
        elif self.match_all([')']):
            return True
        return False


    def des_dec_assign(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.des_this_super():
                return True
        return False

    def des_this_super(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.var_id():
                return True
        elif self.match_all(['self', 'grand']):
            if self.this_super():
                if self.var():
                    if self.des_dec_assign2():
                        return True
        return False

    def des_this_super1(self):
        if self.match_all(['ID']):
            if self.var():
                return True
        elif self.match_all(['self', 'grand']):
            if self.this_super():
                if self.var():
                    return True
        return False

    def var_id(self):
        if self.match_all(['[', '(', '.']):
            if self.var4():
                if self.des_dec_assign2():
                    return True
        elif self.match_all([',', ']']):
            if self.des_dec_assign1():
                return True
        return False

    def des_dec_assign2(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.des_this_super1():
                if self.des_dec_assign2():
                    return True
        elif self.terminal_check(']'):
            self.tokens.next_line()
            if self.terminal_check('='):
                self.tokens.next_line()
                if self.exp():
                    if self.terminal_check(';'):
                        self.tokens.next_line()
                        return True
        return False

    def des_dec_assign1(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.var_id():
                    return True
        elif self.terminal_check(']'):
            self.tokens.next_line()
            if self.des_dec_assign3():
                return True
        return False

    def des_dec_assign3(self):
        if self.terminal_check('='):
            self.tokens.next_line()
            if self.exp():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.terminal_check(':'):
            self.tokens.next_line()
            if self.type():
                if self.des_dec_assign4():
                    return True
        return False

    def des_dec_assign4(self):
        if self.terminal_check(';'):
            self.tokens.next_line()
            return True
        elif self.terminal_check('='):
            self.tokens.next_line()
            if self.exp_array():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        return False

    def var(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.var1():
                return True
        return False

    def var1(self):
        if self.match_all(['[']):
            if self.array_index():
                if self.var2():
                    return True
        elif self.match_all(['.', '^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            if self.var2():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.var4():
                    return True
        return False

    def var2(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.var():
                return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def var4(self):
        if self.match_all(['[']):
            if self.array_index():
                if self.var2():
                    return True
        elif self.match_all(['(']):
            if self.args():
                if self.terminal_check('.'):
                    self.tokens.next_line()
                    if self.var():
                        return True
        elif self.terminal_check('.'):
            self.tokens.next_line()
            if self.var():
                return True
        return False

    def var3(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.var():
                return True
        elif self.match_all(['[']):
            if self.array_index():
                if self.var2():
                    return True
        return False

    def operand(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.operand1():
                return True
        elif self.match_all(['self', 'grand']):
            if self.this_super():
                if self.terminal_check('ID'):
                    self.tokens.next_line()
                    if self.operand1():
                        return True
        elif self.match_all(['int_const', 'float_const', 'char_const', 'str_const', 'bool_const']):
            if self.const():
                return True
        elif self.terminal_check('inc_dec'):
            self.tokens.next_line()
            if self.var():
                return True
        return False

    def operand1(self):
        if self.match_all(['[']):
            if self.array_index():
                if self.operand2():
                    return True
        elif self.match_all(['.', 'inc_dec', 'as', '^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            if self.operand2():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.operand3():
                    return True
        return False

    def operand2(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.operand4():
                return True
        elif self.terminal_check('inc_dec'):
            self.tokens.next_line()
            return True
        elif self.terminal_check('as'):
            self.tokens.next_line()
            if self.type():
                return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def operand3(self):
        if self.terminal_check('.'):
            self.tokens.next_line()
            if self.operand4():
                return True
        elif self.match_all(['[']):
            if self.array_index():
                if self.operand2():
                    return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def operand4(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.operand1():
                return True
        return False

    def OE(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.AE():
                if self.OE1():
                    return True
        return False

    def OE1(self):
        if self.terminal_check('||'):
            self.tokens.next_line()
            if self.AE():
                if self.OE1():
                    return True
        elif self.match_all([':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def AE(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.RE():
                if self.AE1():
                    return True
        return False

    def AE1(self):
        if self.terminal_check('&&'):
            self.tokens.next_line()
            if self.RE():
                if self.AE1():
                    return True
        elif self.match_all(['||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def RE(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.E():
                if self.RE1():
                    return True
        return False

    def RE1(self):
        if self.terminal_check('relational'):
            self.tokens.next_line()
            if self.E():
                if self.RE1():
                    return True
        elif self.match_all(['&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def E(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.T():
                if self.E1():
                    return True
        return False

    def E1(self):
        if self.terminal_check('PM'):
            self.tokens.next_line()
            if self.T():
                if self.E1():
                    return True
        elif self.match_all(['relational', '&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def T(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.P():
                if self.T1():
                    return True
        return False

    def T1(self):
        if self.terminal_check('MDM'):
            self.tokens.next_line()
            if self.P():
                if self.T1():
                    return True
        elif self.match_all(['PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def P(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.F():
                if self.P1():
                    return True
        return False

    def P1(self):
        if self.terminal_check('^'):
            self.tokens.next_line()
            if self.F():
                if self.P1():
                    return True
        elif self.match_all(['MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def F(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec']):
            if self.operand():
                return True
        elif self.match_all(['(']):
            if self.B():
                return True
        elif self.terminal_check('!'):
            self.tokens.next_line()
            if self.F():
                return True
        elif self.terminal_check('PM'):
            self.tokens.next_line()
            if self.F():
                return True
        return False

    def B(self):
        if self.terminal_check('('):
            self.tokens.next_line()
            if self.exp():
                if self.terminal_check(')'):
                    self.tokens.next_line()
                    return True
        return False

    def exp(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.OE():
                return True
        elif self.match_all(['make']):
            if self.obj_dec():
                return True
        return False

    def unpacked(self):
        if self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ';']):
            if self.P1():
                if self.T1():
                    if self.E1():
                        if self.RE1():
                            if self.AE1():
                                if self.OE1():
                                    return True
        return False

    def obj_dec(self):
        if self.terminal_check('make'):
            self.tokens.next_line()
            if self.obj_dec1():
                return True
        return False

    def obj_dec1(self):
        if self.terminal_check('str'):
            self.tokens.next_line()
            if self.obj_dec2():
                return True
        elif self.terminal_check('ID'):
            self.tokens.next_line()
            if self.obj_dec2():
                return True
        elif self.terminal_check('primitive_type'):
            self.tokens.next_line()
            if self.array_ref():
                return True
        return False

    def obj_dec2(self):
        if self.match_all(['(']):
            if self.args():
                return True
        elif self.match_all(['[']):
            if self.array_ref():
                return True
        return False

    def array_ref(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.array_ref1():
                return True
        return False

    def array_ref1(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', 'make']):
            if self.exp():
                if self.terminal_check(']'):
                    self.tokens.next_line()
                    if self.array_ref2():
                        return True
        elif self.terminal_check(']'):
            self.tokens.next_line()
            if self.array_ref3():
                return True
        return False

    def array_ref2(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.array_ref_exp():
                return True
        elif self.match_all([':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def array_ref_exp(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', 'make']):
            if self.exp():
                if self.terminal_check(']'):
                    self.tokens.next_line()
                    if self.array_ref2():
                        return True
        elif self.terminal_check(']'):
            self.tokens.next_line()
            if self.array_ref4():
                return True
        return False

    def array_ref4(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.terminal_check(']'):
                self.tokens.next_line()
                if self.array_ref4():
                    return True
        elif self.match_all([':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def array_ref3(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.terminal_check(']'):
                self.tokens.next_line()
                if self.array_ref3():
                    return True
        elif self.terminal_check(':'):
            self.tokens.next_line()
            if self.array_dec():
                return True
        return False

    def array_index(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.exp():
                if self.terminal_check(']'):
                    self.tokens.next_line()
                    if self.array_index1():
                        return True
        return False

    def array_index1(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.exp():
                if self.terminal_check(']'):
                    self.tokens.next_line()
                    if self.array_index1():
                        return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range', '.', 'inc_dec', '=', 'compound_assignment', 'as']):
            return True
        return False


    def args(self):
        if self.terminal_check('('):
            self.tokens.next_line()
            if self.args1():
                return True
        return False

    def args1(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.exp():
                if self.args2():
                    return True
        elif self.terminal_check(')'):
            self.tokens.next_line()
            return True
        return False

    def args2(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.exp():
                if self.args2():
                    return True
        elif self.terminal_check(')'):
            self.tokens.next_line()
            return True
        return False

    def type(self):
        if self.terminal_check('str'):
            self.tokens.next_line()
            if self.dim():
                return True
        elif self.terminal_check('primitive_type'):
            self.tokens.next_line()
            if self.dim():
                return True
        elif self.terminal_check('ID'):
            self.tokens.next_line()
            if self.dim():
                return True
        return False

    def dim(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.terminal_check(']'):
                self.tokens.next_line()
                if self.dim():
                    return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', '=', 'in', 'range', ',', ')', '{', ';']):
            return True
        return False


    def body(self):
        if self.terminal_check(';'):
            self.tokens.next_line()
            return True
        elif self.match_all(['ID', 'const', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[']):
            if self.SST():
                return True
        elif self.terminal_check('{'):
            self.tokens.next_line()
            if self.MST():
                if self.terminal_check('}'):
                    self.tokens.next_line()
                    return True
        return False

    def array_dec(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.array_dec1():
                return True
        return False

    def array_dec1(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', '[', 'make']):
            if self.exp_array():
                if self.array_dec2():
                    return True
        elif self.terminal_check(']'):
            self.tokens.next_line()
            return True
        return False

    def array_dec2(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.exp_array():
                if self.array_dec2():
                    return True
        elif self.terminal_check(']'):
            self.tokens.next_line()
            return True
        return False

    def exp_array(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', 'make']):
            if self.exp():
                return True
        elif self.match_all(['[']):
            if self.array_dec():
                return True
        return False

    def match_st(self):
        if self.terminal_check('match'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.exp():
                    if self.terminal_check(')'):
                        self.tokens.next_line()
                        if self.match_body():
                            return True
        return False

    def match_body(self):
        if self.match_all(['case']):
            if self.case():
                return True
        elif self.match_all(['default']):
            if self.default():
                return True
        elif self.terminal_check('{'):
            self.tokens.next_line()
            if self.case_default():
                if self.terminal_check('}'):
                    self.tokens.next_line()
                    return True
        return False

    def case_pd(self):
        if self.terminal_check('case'):
            self.tokens.next_line()
            if self.exp():
                if self.terminal_check('->'):
                    self.tokens.next_line()
                    if self.body():
                        return True
        return False

    def default(self):
        if self.terminal_check('default'):
            self.tokens.next_line()
            if self.terminal_check('->'):
                self.tokens.next_line()
                if self.body():
                    return True
        return False

    def case_default(self):
        if self.match_all(['case']):
            if self.case_pd():
                if self.case_default():
                    return True
        elif self.match_all(['default']):
            if self.default():
                return True
        elif self.match_all(['}']):
            return True
        return False


    def try_st(self):
        if self.terminal_check('try'):
            self.tokens.next_line()
            if self.body():
                if self.except_multi():
                    if self.finally_pd():
                        return True
        return False

    def except_pd(self):
        if self.terminal_check('except'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.terminal_check('ID'):
                    self.tokens.next_line()
                    if self.terminal_check(':'):
                        self.tokens.next_line()
                        if self.type():
                            if self.terminal_check(')'):
                                self.tokens.next_line()
                                if self.terminal_check('{'):
                                    self.tokens.next_line()
                                    if self.MST():
                                        if self.terminal_check('}'):
                                            self.tokens.next_line()
                                            return True
        return False

    def except_multi(self):
        if self.match_all(['except']):
            if self.except_pd():
                if self.except_multi1():
                    return True
        return False

    def except_multi1(self):
        if self.match_all(['except']):
            if self.except_pd():
                if self.except_multi1():
                    return True
        elif self.match_all(['finally', 'ID', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[', '}', 'else']):
            return True
        return False


    def finally_pd(self):
        if self.terminal_check('finally'):
            self.tokens.next_line()
            if self.terminal_check('{'):
                self.tokens.next_line()
                if self.MST():
                    if self.terminal_check('}'):
                        self.tokens.next_line()
                        return True
        elif self.match_all(['ID', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[', '}', 'else']):
            return True
        return False


    def const(self):
        if self.terminal_check('int_const'):
            self.tokens.next_line()
            return True
        elif self.terminal_check('float_const'):
            self.tokens.next_line()
            return True
        elif self.terminal_check('char_const'):
            self.tokens.next_line()
            return True
        elif self.terminal_check('str_const'):
            self.tokens.next_line()
            return True
        elif self.terminal_check('bool_const'):
            self.tokens.next_line()
            return True
        return False

    def if_st(self):
        if self.terminal_check('if'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.exp():
                    if self.terminal_check(')'):
                        self.tokens.next_line()
                        if self.body():
                            if self.else_pd():
                                return True
        return False

    def else_pd(self):
        if self.terminal_check('else'):
            self.tokens.next_line()
            if self.body():
                return True
        elif self.match_all(['ID', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[', '}', 'else']):
            return True
        return False


    def while_st(self):
        if self.terminal_check('while'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.exp():
                    if self.terminal_check(')'):
                        self.tokens.next_line()
                        if self.body():
                            return True
        return False

    def func_dec(self):
        if self.terminal_check('func'):
            self.tokens.next_line()
            if self.func_dec1():
                return True
        return False

    def func_dec1(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.params():
                    if self.terminal_check('->'):
                        self.tokens.next_line()
                        if self.type_void():
                            if self.terminal_check('{'):
                                self.tokens.next_line()
                                if self.MST():
                                    if self.terminal_check('}'):
                                        self.tokens.next_line()
                                        return True
        return False

    def params(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.terminal_check(':'):
                self.tokens.next_line()
                if self.type():
                    if self.params1():
                        return True
        elif self.terminal_check(')'):
            self.tokens.next_line()
            return True
        return False

    def params1(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.terminal_check(':'):
                    self.tokens.next_line()
                    if self.type():
                        if self.params1():
                            return True
        elif self.terminal_check(')'):
            self.tokens.next_line()
            return True
        return False

    def type_void(self):
        if self.match_all(['str', 'primitive_type', 'ID']):
            if self.type():
                return True
        elif self.terminal_check('void'):
            self.tokens.next_line()
            return True
        return False

    def inc_dec_st(self):
        if self.terminal_check('inc_dec'):
            self.tokens.next_line()
            if self.var():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        return False

    def SST(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.SST1():
                return True
        elif self.terminal_check('const'):
            self.tokens.next_line()
            if self.SST2():
                return True
        elif self.terminal_check('self'):
            self.tokens.next_line()
            if self.this_super1():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.terminal_check('grand'):
            self.tokens.next_line()
            if self.terminal_check('.'):
                self.tokens.next_line()
                if self.terminal_check('ID'):
                    self.tokens.next_line()
                    if self.this_super1():
                        if self.terminal_check(';'):
                            self.tokens.next_line()
                            return True
        elif self.terminal_check('inc_dec'):
            self.tokens.next_line()
            if self.var():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.match_all(['if']):
            if self.if_st():
                return True
        elif self.match_all(['match']):
            if self.match_st():
                return True
        elif self.match_all(['while']):
            if self.while_st():
                return True
        elif self.match_all(['for']):
            if self.for_st():
                return True
        elif self.match_all(['try']):
            if self.try_st():
                return True
        elif self.match_all(['return']):
            if self.return_st():
                return True
        elif self.terminal_check('continue_break'):
            self.tokens.next_line()
            if self.terminal_check(';'):
                self.tokens.next_line()
                return True
        elif self.match_all(['[']):
            if self.des_dec_assign():
                return True
        return False

    def SST1(self):
        if self.match_all([':']):
            if self.dec1():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.match_all(['[', '.', 'inc_dec', '=', '(']):
            if self.var_fn_assign1():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        return False

    def SST2(self):
        if self.terminal_check('ID'):
            self.tokens.next_line()
            if self.dec1():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.match_all(['ID']):
            if self.des_dec_assign():
                return True
        return False

    def MST(self):
        if self.match_all(['ID', 'const', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[']):
            if self.SST():
                if self.MST():
                    return True
        elif self.match_all(['}']):
            return True
        return False


    def return_st(self):
        if self.terminal_check('return'):
            self.tokens.next_line()
            if self.return_exp():
                return True
        return False

    def return_exp(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.exp():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.terminal_check(';'):
            self.tokens.next_line()
            return True
        return False

    def class_def(self):
        if self.terminal_check('type'):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.enhance():
                    if self.terminal_check('{'):
                        self.tokens.next_line()
                        if self.class_body():
                            if self.terminal_check('}'):
                                self.tokens.next_line()
                                return True
        return False

    def enhance(self):
        if self.terminal_check('enhances'):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.enhance1():
                    return True
        elif self.match_all(['{']):
            return True
        return False


    def enhance1(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.enhance1():
                    return True
        elif self.match_all(['{']):
            return True
        return False


    def class_body(self):
        if self.match_all(['access_modifier', 'passive', 'const', 'ID', 'func', '[']):
            if self.cb_am_ps_cn():
                if self.class_body():
                    return True
        elif self.match_all(['}']):
            return True
        return False


    def cb_am_ps_cn(self):
        if self.terminal_check('access_modifier'):
            self.tokens.next_line()
            if self.cb_am_ps_cn1():
                return True
        elif self.terminal_check('passive'):
            self.tokens.next_line()
            if self.am_cn():
                if self.adecs():
                    return True
        elif self.terminal_check('const'):
            self.tokens.next_line()
            if self.am_ps():
                if self.adecs():
                    return True
        elif self.match_all(['ID', 'func', '[']):
            if self.cdecs():
                return True
        return False

    def cb_am_ps_cn1(self):
        if self.match_all(['ID', 'func', '[']):
            if self.cdecs():
                return True
        elif self.terminal_check('passive'):
            self.tokens.next_line()
            if self.cn():
                if self.adecs():
                    return True
        elif self.terminal_check('const'):
            self.tokens.next_line()
            if self.ps():
                if self.adecs():
                    return True
        return False

    def am_ps_cn(self):
        if self.terminal_check('access_modifier'):
            self.tokens.next_line()
            if self.ps_cn():
                return True
        elif self.terminal_check('passive'):
            self.tokens.next_line()
            if self.am_cn():
                return True
        elif self.terminal_check('const'):
            self.tokens.next_line()
            if self.am_ps():
                return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def ps_cn(self):
        if self.terminal_check('passive'):
            self.tokens.next_line()
            if self.cn():
                return True
        elif self.terminal_check('const'):
            self.tokens.next_line()
            if self.ps():
                return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def am_cn(self):
        if self.terminal_check('access_modifier'):
            self.tokens.next_line()
            if self.cn():
                return True
        elif self.terminal_check('const'):
            self.tokens.next_line()
            if self.am():
                return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def am_ps(self):
        if self.terminal_check('access_modifier'):
            self.tokens.next_line()
            if self.ps():
                return True
        elif self.terminal_check('passive'):
            self.tokens.next_line()
            if self.am():
                return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def cdecs(self):
        if self.match_all(['ID']):
            if self.dec():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.terminal_check('func'):
            self.tokens.next_line()
            if self.fn_init_dec():
                return True
        elif self.match_all(['[']):
            if self.des_dec():
                return True
        return False

    def fn_init_dec(self):
        if self.match_all(['ID']):
            if self.func_dec1():
                return True
        elif self.terminal_check('constructor'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.params():
                    if self.terminal_check('{'):
                        self.tokens.next_line()
                        if self.MST():
                            if self.terminal_check('}'):
                                self.tokens.next_line()
                                return True
        return False

    def des_dec(self):
        if self.terminal_check('['):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.des_dec1():
                    return True
        return False

    def des_dec1(self):
        if self.terminal_check(','):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.des_dec1():
                    return True
        elif self.terminal_check(']'):
            self.tokens.next_line()
            if self.terminal_check(':'):
                self.tokens.next_line()
                if self.type():
                    if self.des_dec_assign4():
                        return True
        return False

    def cn(self):
        if self.terminal_check('const'):
            self.tokens.next_line()
            return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def am(self):
        if self.terminal_check('access_modifier'):
            self.tokens.next_line()
            return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def ps(self):
        if self.terminal_check('passive'):
            self.tokens.next_line()
            return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def abstract_class_def(self):
        if self.terminal_check('abstract'):
            self.tokens.next_line()
            if self.terminal_check('type'):
                self.tokens.next_line()
                if self.terminal_check('ID'):
                    self.tokens.next_line()
                    if self.enhance():
                        if self.terminal_check('{'):
                            self.tokens.next_line()
                            if self.abstract_body():
                                if self.terminal_check('}'):
                                    self.tokens.next_line()
                                    return True
        return False

    def abstract_body(self):
        if self.terminal_check('abstract'):
            self.tokens.next_line()
            if self.abstract_func():
                if self.abstract_body():
                    return True
        elif self.match_all(['access_modifier', 'passive', 'const', 'ID', 'func', '[']):
            if self.am_ps_cn():
                if self.adecs():
                    if self.abstract_body():
                        return True
        elif self.match_all(['}']):
            return True
        return False


    def adecs(self):
        if self.match_all(['ID']):
            if self.dec():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.match_all(['func']):
            if self.func_dec():
                return True
        elif self.match_all(['[']):
            if self.des_dec():
                return True
        return False

    def abstract_func(self):
        if self.terminal_check('func'):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.terminal_check('('):
                    self.tokens.next_line()
                    if self.params():
                        if self.terminal_check('->'):
                            self.tokens.next_line()
                            if self.type_void():
                                if self.terminal_check(';'):
                                    self.tokens.next_line()
                                    return True
        return False

    def lang(self):
        if self.match_all(['import', 'const', 'type', 'abstract', 'ID', 'func', '[', '$']):
            if self.imports():
                if self.defs1():
                    return True
        return False

    def defs(self):
        if self.match_all(['type']):
            if self.class_def():
                return True
        elif self.match_all(['abstract']):
            if self.abstract_class_def():
                return True
        elif self.terminal_check('const'):
            self.tokens.next_line()
            if self.defs3():
                return True
        elif self.match_all(['ID']):
            if self.dec():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.match_all(['[']):
            if self.des_dec():
                return True
        return False

    def defs3(self):
        if self.match_all(['type']):
            if self.class_def():
                return True
        elif self.match_all(['ID']):
            if self.dec():
                if self.terminal_check(';'):
                    self.tokens.next_line()
                    return True
        elif self.match_all(['[']):
            if self.des_dec():
                return True
        return False

    def defs1(self):
        if self.match_all(['const', 'type', 'abstract', 'ID', '[']):
            if self.defs():
                if self.defs1():
                    return True
        elif self.terminal_check('func'):
            self.tokens.next_line()
            if self.lang1():
                return True
        elif self.match_all(['$']):
            return True
        return False


    def defs2(self):
        if self.match_all(['const', 'type', 'abstract', 'ID', '[']):
            if self.defs():
                if self.defs2():
                    return True
        elif self.match_all(['func']):
            if self.func_dec():
                if self.defs2():
                    return True
        elif self.match_all(['$']):
            return True
        return False


    def lang1(self):
        if self.match_all(['ID']):
            if self.func_dec1():
                if self.defs1():
                    return True
        elif self.match_all(['main']):
            if self.main():
                if self.defs2():
                    return True
        return False

    def main(self):
        if self.terminal_check('main'):
            self.tokens.next_line()
            if self.terminal_check('('):
                self.tokens.next_line()
                if self.terminal_check(')'):
                    self.tokens.next_line()
                    if self.terminal_check('->'):
                        self.tokens.next_line()
                        if self.terminal_check('void'):
                            self.tokens.next_line()
                            if self.terminal_check('{'):
                                self.tokens.next_line()
                                if self.MST():
                                    if self.terminal_check('}'):
                                        self.tokens.next_line()
                                        return True
        return False

    def imports(self):
        if self.match_all(['import']):
            if self.import_pd():
                if self.imports1():
                    return True
        elif self.match_all(['const', 'type', 'abstract', 'ID', 'func', '[', '$']):
            return True
        return False


    def imports1(self):
        if self.match_all(['import']):
            if self.import_pd():
                if self.imports1():
                    return True
        elif self.match_all(['const', 'type', 'abstract', 'ID', 'func', '[', '$']):
            return True
        return False


    def import_pd(self):
        if self.terminal_check('import'):
            self.tokens.next_line()
            if self.terminal_check('ID'):
                self.tokens.next_line()
                if self.terminal_check('from'):
                    self.tokens.next_line()
                    if self.terminal_check('str_const'):
                        self.tokens.next_line()
                        if self.terminal_check(';'):
                            self.tokens.next_line()
                            return True
        return False

