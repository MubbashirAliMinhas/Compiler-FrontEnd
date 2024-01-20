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
            self.tokens.next_line()
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
        elif self.match_all(['.', 'compound_assignment', '=', 'inc_dec']):
            if self.var_fn_assign2():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.var_fn_assign3():
                    return True
        return False

    def var_fn_assign2(self):
        if self.terminal_check('.'):
            if self.var_fn_assign4():
                return True
        elif self.terminal_check('inc_dec'):
            return True
        elif self.match_all(['compound_assignment', '=']):
            if self.equals():
                if self.assign1():
                    return True
        return False

    def var_fn_assign3(self):
        if self.terminal_check('.'):
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
            if self.var_fn_assign1():
                return True
        return False

    def this_super(self):
        if self.terminal_check('self'):
            if self.terminal_check('.'):
                return True
        elif self.terminal_check('grand'):
            if self.terminal_check('.'):
                if self.terminal_check('ID'):
                    if self.terminal_check('.'):
                        return True
        return False

    def this_super1(self):
        if self.match_all(['(']):
            if self.args():
                return True
        elif self.terminal_check('.'):
            if self.terminal_check('ID'):
                if self.var_fn_assign1():
                    return True
        return False

    def assign1(self):
        if self.terminal_check('ID'):
            if self.assign2():
                return True
        elif self.match_all(['grand', 'self']):
            if self.this_super():
                if self.terminal_check('ID'):
                    if self.assign2():
                        return True
        elif self.match_all(['str_const', '(', 'make', 'PM', 'bool_const', '!', 'float_const', 'int_const', 'char_const']):
            if self.exp1():
                return True
        elif self.terminal_check('inc_dec'):
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
            if self.F():
                if self.unpacked():
                    return True
        elif self.match_all(['str_const', 'float_const', 'int_const', 'char_const', 'bool_const']):
            if self.const():
                if self.unpacked():
                    return True
        elif self.terminal_check('PM'):
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
        elif self.match_all(['.', '^', 'PM', '=', 'inc_dec', ';', 'relational', '&&', 'MDM', 'compound_assignment', '||', 'as']):
            if self.assign3():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.assign4():
                    return True
        return False

    def assign3(self):
        if self.terminal_check('.'):
            if self.assign5():
                return True
        elif self.match_all(['relational', '&&', 'MDM', '^', 'PM', ';', '||']):
            if self.unpacked():
                return True
        elif self.terminal_check('inc_dec'):
            if self.unpacked():
                return True
        elif self.terminal_check('as'):
            if self.type():
                if self.unpacked():
                    return True
        elif self.match_all(['compound_assignment', '=']):
            if self.equals():
                if self.assign1():
                    return True
        return False

    def assign4(self):
        if self.terminal_check('.'):
            if self.assign5():
                return True
        elif self.match_all(['relational', '&&', 'MDM', '^', 'PM', ';', '||']):
            if self.unpacked():
                return True
        elif self.terminal_check('as'):
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
            if self.assign2():
                return True
        return False

    def equals(self):
        if self.terminal_check('='):
            return True
        elif self.terminal_check('compound_assignment'):
            return True
        return False

    def dec(self):
        if self.terminal_check('ID'):
            if self.dec1():
                return True
        return False

    def dec1(self):
        if self.terminal_check(':'):
            if self.type():
                if self.dec2():
                    return True
        return False

    def dec2(self):
        if self.terminal_check('='):
            if self.dec3():
                return True
        elif self.match_all([';']):
            return True
        return False

    def dec3(self):
        if self.match_all(['str_const', '(', 'make', 'PM', 'bool_const', '!', 'inc_dec', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.assign1():
                return True
        elif self.match_all(['[']):
            if self.array_dec():
                return True
        return False

    def for_st(self):
        if self.terminal_check('for'):
            if self.terminal_check('('):
                if self.decs():
                    if self.terminal_check('in'):
                        if self.iterator():
                            if self.terminal_check(')'):
                                if self.body():
                                    return True
        return False

    def decs(self):
        if self.terminal_check('ID'):
            if self.terminal_check(':'):
                if self.type():
                    return True
        elif self.match_all(['[']):
            if self.des_dec_ref():
                return True
        return False

    def des_dec_ref(self):
        if self.terminal_check('['):
            if self.terminal_check('ID'):
                if self.des_dec_ref1():
                    if self.terminal_check(']'):
                        if self.terminal_check(':'):
                            if self.type():
                                return True
        return False

    def des_dec_ref1(self):
        if self.terminal_check(','):
            if self.terminal_check('ID'):
                if self.des_dec_ref1():
                    return True
        elif self.match_all([']']):
            return True
        return False

    def iterator(self):
        if self.match_all(['str_const', '(', 'make', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.exp():
                if self.range1():
                    return True
        return False

    def range(self):
        if self.terminal_check('range'):
            if self.exp():
                if self.terminal_check(':'):
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
            if self.des_this_super():
                return True
        return False

    def des_this_super(self):
        if self.terminal_check('ID'):
            if self.var_id():
                return True
        elif self.match_all(['grand', 'self']):
            if self.this_super():
                if self.var():
                    if self.des_dec_assign2():
                        return True
        return False

    def des_this_super1(self):
        if self.match_all(['ID']):
            if self.var():
                return True
        elif self.match_all(['grand', 'self']):
            if self.this_super():
                if self.var():
                    return True
        return False

    def var_id(self):
        if self.match_all(['.', '(', '[']):
            if self.var4():
                if self.des_dec_assign2():
                    return True
        elif self.match_all([',', ']']):
            if self.des_dec_assign1():
                return True
        return False

    def des_dec_assign2(self):
        if self.terminal_check(','):
            if self.des_this_super1():
                if self.des_dec_assign2():
                    return True
        elif self.terminal_check(']'):
            if self.terminal_check('='):
                if self.exp():
                    if self.terminal_check(';'):
                        return True
        return False

    def des_dec_assign1(self):
        if self.terminal_check(','):
            if self.terminal_check('ID'):
                if self.var_id():
                    return True
        elif self.terminal_check(']'):
            if self.des_dec_assign3():
                return True
        return False

    def des_dec_assign3(self):
        if self.terminal_check('='):
            if self.exp():
                if self.terminal_check(';'):
                    return True
        elif self.terminal_check(':'):
            if self.type():
                if self.des_dec_assign4():
                    return True
        return False

    def des_dec_assign4(self):
        if self.terminal_check(';'):
            return True
        elif self.terminal_check('='):
            if self.exp_array():
                if self.terminal_check(';'):
                    return True
        return False

    def var(self):
        if self.terminal_check('ID'):
            if self.var1():
                return True
        return False

    def var1(self):
        if self.match_all(['[']):
            if self.array_index():
                if self.var2():
                    return True
        elif self.match_all([']', '.', '^', 'PM', ';', ',', 'relational', '&&', 'MDM', '||']):
            if self.var2():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.var4():
                    return True
        return False

    def var2(self):
        if self.terminal_check('.'):
            if self.var():
                return True
        elif self.match_all([']', '^', 'PM', ';', ',', 'relational', '&&', 'MDM', '||']):
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
                    if self.var():
                        return True
        elif self.terminal_check('.'):
            if self.var():
                return True
        return False

    def operand(self):
        if self.terminal_check('ID'):
            if self.operand1():
                return True
        elif self.match_all(['grand', 'self']):
            if self.this_super():
                if self.terminal_check('ID'):
                    if self.operand1():
                        return True
        elif self.match_all(['str_const', 'float_const', 'int_const', 'char_const', 'bool_const']):
            if self.const():
                return True
        elif self.terminal_check('inc_dec'):
            if self.var():
                return True
        return False

    def operand1(self):
        if self.match_all(['[']):
            if self.array_index():
                if self.operand2():
                    return True
        elif self.match_all(['PM', ')', ',', '&&', '->', '||', 'range', ']', '.', '^', ';', 'inc_dec', ':', 'relational', 'MDM', 'as']):
            if self.operand2():
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.operand3():
                    return True
        return False

    def operand2(self):
        if self.terminal_check('.'):
            if self.operand4():
                return True
        elif self.terminal_check('inc_dec'):
            return True
        elif self.terminal_check('as'):
            if self.type():
                return True
        elif self.match_all([']', '^', 'PM', ')', ';', ':', ',', 'relational', '&&', 'MDM', '->', '||', 'range']):
            return True
        return False

    def operand3(self):
        if self.terminal_check('.'):
            if self.operand4():
                return True
        elif self.match_all(['[']):
            if self.array_index():
                if self.operand2():
                    return True
        elif self.match_all([']', '^', 'PM', ')', ';', ':', ',', 'relational', '&&', 'MDM', '->', '||', 'range']):
            return True
        return False

    def operand4(self):
        if self.terminal_check('ID'):
            if self.operand1():
                return True
        return False

    def OE(self):
        if self.match_all(['str_const', '(', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.AE():
                if self.OE1():
                    return True
        return False

    def OE1(self):
        if self.terminal_check('||'):
            if self.AE():
                if self.OE1():
                    return True
        elif self.match_all([':', ',', ']', ')', '->', ';', 'range']):
            return True
        return False

    def AE(self):
        if self.match_all(['str_const', '(', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.RE():
                if self.AE1():
                    return True
        return False

    def AE1(self):
        if self.terminal_check('&&'):
            if self.RE():
                if self.AE1():
                    return True
        elif self.match_all([']', ')', ';', ':', ',', '->', '||', 'range']):
            return True
        return False

    def RE(self):
        if self.match_all(['str_const', '(', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.E():
                if self.RE1():
                    return True
        return False

    def RE1(self):
        if self.terminal_check('relational'):
            if self.E():
                if self.RE1():
                    return True
        elif self.match_all([']', ')', ';', ':', ',', '&&', '->', '||', 'range']):
            return True
        return False

    def E(self):
        if self.match_all(['str_const', '(', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.T():
                if self.E1():
                    return True
        return False

    def E1(self):
        if self.terminal_check('PM'):
            if self.T():
                if self.E1():
                    return True
        elif self.match_all([']', ')', ';', ':', ',', 'relational', '&&', '->', '||', 'range']):
            return True
        return False

    def T(self):
        if self.match_all(['str_const', '(', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.P():
                if self.T1():
                    return True
        return False

    def T1(self):
        if self.terminal_check('MDM'):
            if self.P():
                if self.T1():
                    return True
        elif self.match_all([']', 'PM', ')', ';', ':', ',', 'relational', '&&', '->', '||', 'range']):
            return True
        return False

    def P(self):
        if self.match_all(['str_const', '(', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.F():
                if self.P1():
                    return True
        return False

    def P1(self):
        if self.terminal_check('^'):
            if self.F():
                if self.P1():
                    return True
        elif self.match_all([']', 'PM', ')', ';', ':', ',', 'relational', '&&', 'MDM', '->', '||', 'range']):
            return True
        return False

    def F(self):
        if self.match_all(['str_const', 'bool_const', 'inc_dec', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.operand():
                return True
        elif self.match_all(['(']):
            if self.B():
                return True
        elif self.terminal_check('!'):
            if self.F():
                return True
        elif self.terminal_check('PM'):
            if self.F():
                return True
        return False

    def B(self):
        if self.terminal_check('('):
            if self.exp():
                if self.terminal_check(')'):
                    return True
        return False

    def exp(self):
        if self.match_all(['str_const', '(', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.OE():
                return True
        elif self.match_all(['make']):
            if self.obj_dec():
                return True
        return False

    def unpacked(self):
        if self.match_all(['relational', '&&', 'MDM', '^', 'PM', ';', '||']):
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
            if self.obj_dec1():
                return True
        return False

    def obj_dec1(self):
        if self.terminal_check('str'):
            if self.obj_dec2():
                return True
        elif self.terminal_check('ID'):
            if self.obj_dec2():
                return True
        elif self.terminal_check('primitive_type'):
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
            if self.array_ref1():
                return True
        return False

    def array_ref1(self):
        if self.match_all(['str_const', '(', 'make', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.exp():
                if self.terminal_check(']'):
                    if self.array_ref2():
                        return True
        elif self.terminal_check(']'):
            if self.array_ref3():
                return True
        return False

    def array_ref2(self):
        if self.terminal_check('['):
            if self.array_ref_exp():
                return True
        elif self.match_all([':', ',', ']', ')', '->', ';', 'range']):
            return True
        return False

    def array_ref_exp(self):
        if self.match_all(['str_const', '(', 'make', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.exp():
                if self.terminal_check(']'):
                    if self.array_ref2():
                        return True
        elif self.terminal_check(']'):
            if self.array_ref4():
                return True
        return False

    def array_ref4(self):
        if self.terminal_check('['):
            if self.terminal_check(']'):
                if self.array_ref4():
                    return True
        elif self.match_all([':', ',', ']', ')', '->', ';', 'range']):
            return True
        return False

    def array_ref3(self):
        if self.terminal_check('['):
            if self.terminal_check(']'):
                if self.array_ref3():
                    return True
        elif self.terminal_check(':'):
            if self.array_dec():
                return True
        return False

    def array_index(self):
        if self.terminal_check('['):
            if self.exp():
                if self.terminal_check(']'):
                    if self.array_index1():
                        return True
        return False

    def array_index1(self):
        if self.terminal_check('['):
            if self.exp():
                if self.terminal_check(']'):
                    if self.array_index1():
                        return True
        elif self.match_all(['PM', ')', ',', '&&', '->', 'compound_assignment', '||', 'range', ']', '.', '^', '=', 'inc_dec', ';', ':', 'relational', 'MDM', 'as']):
            return True
        return False

    def args(self):
        if self.terminal_check('('):
            if self.args1():
                return True
        return False

    def args1(self):
        if self.match_all(['str_const', '(', 'make', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.exp():
                if self.args2():
                    return True
        elif self.terminal_check(')'):
            return True
        return False

    def args2(self):
        if self.terminal_check(','):
            if self.exp():
                if self.args2():
                    return True
        elif self.terminal_check(')'):
            return True
        return False

    def type(self):
        if self.terminal_check('str'):
            if self.dim():
                return True
        elif self.terminal_check('primitive_type'):
            if self.dim():
                return True
        elif self.terminal_check('ID'):
            if self.dim():
                return True
        return False

    def dim(self):
        if self.terminal_check('['):
            if self.terminal_check(']'):
                if self.dim():
                    return True
        elif self.match_all(['PM', ')', ',', '{', '&&', '->', '||', 'range', ']', 'in', '^', ';', '=', ':', 'relational', 'MDM']):
            return True
        return False

    def body(self):
        if self.terminal_check(';'):
            return True
        elif self.match_all(['for', 'try', 'const', 'match', '[', 'continue_break', 'inc_dec', 'grand', 'if', 'return', 'self', 'while', 'ID']):
            if self.SST():
                return True
        elif self.terminal_check('{'):
            if self.MST():
                if self.terminal_check('}'):
                    return True
        return False

    def array_dec(self):
        if self.terminal_check('['):
            if self.array_dec1():
                return True
        return False

    def array_dec1(self):
        if self.match_all(['str_const', '(', 'make', '[', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.exp_array():
                if self.array_dec2():
                    return True
        elif self.terminal_check(']'):
            return True
        return False

    def array_dec2(self):
        if self.terminal_check(','):
            if self.exp_array():
                if self.array_dec2():
                    return True
        elif self.terminal_check(']'):
            return True
        return False

    def exp_array(self):
        if self.match_all(['str_const', '(', 'make', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.exp():
                return True
        elif self.match_all(['[']):
            if self.array_dec():
                return True
        return False

    def match_st(self):
        if self.terminal_check('match'):
            if self.terminal_check('('):
                if self.exp():
                    if self.terminal_check(')'):
                        if self.match_body():
                            return True
        return False

    def match_body(self):
        if self.match_all(['case']):
            if self.case_pd():
                return True
        elif self.match_all(['default']):
            if self.default():
                return True
        elif self.terminal_check('{'):
            if self.case_default():
                if self.terminal_check('}'):
                    return True
        return False

    def case_pd(self):
        if self.terminal_check('case'):
            if self.exp():
                if self.terminal_check('->'):
                    if self.body():
                        return True
        return False

    def default(self):
        if self.terminal_check('default'):
            if self.terminal_check('->'):
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
            if self.terminal_check('{'):
                if self.MST():
                    if self.terminal_check('}'):
                        if self.except_multi():
                            if self.finally_pd():
                                return True
        return False

    def except_pd(self):
        if self.terminal_check('except'):
            if self.terminal_check('('):
                if self.terminal_check('ID'):
                    if self.terminal_check(':'):
                        if self.type():
                            if self.terminal_check(')'):
                                if self.terminal_check('{'):
                                    if self.MST():
                                        if self.terminal_check('}'):
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
        elif self.match_all(['case', '[', '}', 'default', 'if', 'self', 'while', 'for', 'ID', 'try', 'const', 'match', 'finally', 'continue_break', 'inc_dec', 'grand', 'else', 'return']):
            return True
        return False

    def finally_pd(self):
        if self.terminal_check('finally'):
            if self.terminal_check('{'):
                if self.MST():
                    if self.terminal_check('}'):
                        return True
        elif self.match_all(['case', '[', '}', 'default', 'if', 'self', 'while', 'for', 'try', 'const', 'match', 'continue_break', 'inc_dec', 'grand', 'return', 'else', 'ID']):
            return True
        return False

    def const(self):
        if self.terminal_check('int_const'):
            return True
        elif self.terminal_check('float_const'):
            return True
        elif self.terminal_check('char_const'):
            return True
        elif self.terminal_check('str_const'):
            return True
        elif self.terminal_check('bool_const'):
            return True
        return False

    def if_st(self):
        if self.terminal_check('if'):
            if self.terminal_check('('):
                if self.exp():
                    if self.terminal_check(')'):
                        if self.body():
                            if self.else_pd():
                                return True
        return False

    def else_pd(self):
        if self.terminal_check('else'):
            if self.body():
                return True
        elif self.match_all(['case', '[', '}', 'default', 'if', 'self', 'while', 'for', 'try', 'const', 'match', 'continue_break', 'inc_dec', 'grand', 'return', 'else', 'ID']):
            return True
        return False

    def while_st(self):
        if self.terminal_check('while'):
            if self.terminal_check('('):
                if self.exp():
                    if self.terminal_check(')'):
                        if self.body():
                            return True
        return False

    def func_dec(self):
        if self.terminal_check('func'):
            if self.func_dec1():
                return True
        return False

    def func_dec1(self):
        if self.terminal_check('ID'):
            if self.terminal_check('('):
                if self.params():
                    if self.terminal_check('->'):
                        if self.type_void():
                            if self.terminal_check('{'):
                                if self.MST():
                                    if self.terminal_check('}'):
                                        return True
        return False

    def params(self):
        if self.terminal_check('ID'):
            if self.terminal_check(':'):
                if self.type():
                    if self.params1():
                        return True
        elif self.terminal_check(')'):
            return True
        return False

    def params1(self):
        if self.terminal_check(','):
            if self.terminal_check('ID'):
                if self.terminal_check(':'):
                    if self.type():
                        if self.params1():
                            return True
        elif self.terminal_check(')'):
            return True
        return False

    def type_void(self):
        if self.match_all(['str', 'primitive_type', 'ID']):
            if self.type():
                return True
        elif self.terminal_check('void'):
            return True
        return False

    def SST(self):
        if self.terminal_check('ID'):
            if self.SST1():
                return True
        elif self.terminal_check('const'):
            if self.SST2():
                return True
        elif self.terminal_check('self'):
            if self.this_super1():
                if self.terminal_check(';'):
                    return True
        elif self.terminal_check('grand'):
            if self.terminal_check('.'):
                if self.terminal_check('ID'):
                    if self.this_super1():
                        if self.terminal_check(';'):
                            return True
        elif self.terminal_check('inc_dec'):
            if self.var():
                if self.terminal_check(';'):
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
            if self.terminal_check(';'):
                return True
        elif self.match_all(['[']):
            if self.des_dec_assign():
                return True
        return False

    def SST1(self):
        if self.match_all([':']):
            if self.dec1():
                if self.terminal_check(';'):
                    return True
        elif self.match_all(['compound_assignment', '(', '.', '[', '=', 'inc_dec']):
            if self.var_fn_assign1():
                if self.terminal_check(';'):
                    return True
        return False

    def SST2(self):
        if self.terminal_check('ID'):
            if self.dec1():
                if self.terminal_check(';'):
                    return True
        elif self.match_all(['[']):
            if self.des_dec_assign():
                return True
        return False

    def MST(self):
        if self.match_all(['for', 'try', 'const', 'match', '[', 'continue_break', 'inc_dec', 'grand', 'if', 'return', 'self', 'while', 'ID']):
            if self.SST():
                if self.MST():
                    return True
        elif self.match_all(['}']):
            return True
        return False

    def return_st(self):
        if self.terminal_check('return'):
            if self.return_exp():
                return True
        return False

    def return_exp(self):
        if self.match_all(['str_const', '(', 'make', 'bool_const', 'PM', 'inc_dec', '!', 'float_const', 'grand', 'int_const', 'self', 'char_const', 'ID']):
            if self.exp():
                if self.terminal_check(';'):
                    return True
        elif self.terminal_check(';'):
            return True
        return False

    def class_def(self):
        if self.terminal_check('type'):
            if self.terminal_check('ID'):
                if self.enhance():
                    if self.terminal_check('{'):
                        if self.class_body():
                            if self.terminal_check('}'):
                                return True
        return False

    def enhance(self):
        if self.terminal_check('enhances'):
            if self.terminal_check('ID'):
                if self.enhance1():
                    return True
        elif self.match_all(['{']):
            return True
        return False

    def enhance1(self):
        if self.terminal_check(','):
            if self.terminal_check('ID'):
                if self.enhance1():
                    return True
        elif self.match_all(['{']):
            return True
        return False

    def class_body(self):
        if self.match_all(['access_modifier', 'passive', 'const', 'func', '[', 'ID']):
            if self.cb_am_ps_cn():
                if self.class_body():
                    return True
        elif self.match_all(['}']):
            return True
        return False

    def cb_am_ps_cn(self):
        if self.terminal_check('access_modifier'):
            if self.cb_am_ps_cn1():
                return True
        elif self.terminal_check('passive'):
            if self.am_cn():
                if self.adecs():
                    return True
        elif self.terminal_check('const'):
            if self.am_ps():
                if self.adecs():
                    return True
        elif self.match_all(['func', '[', 'ID']):
            if self.cdecs():
                return True
        return False

    def cb_am_ps_cn1(self):
        if self.match_all(['func', '[', 'ID']):
            if self.cdecs():
                return True
        elif self.terminal_check('passive'):
            if self.cn():
                if self.adecs():
                    return True
        elif self.terminal_check('const'):
            if self.ps():
                if self.adecs():
                    return True
        return False

    def am_ps_cn(self):
        if self.terminal_check('access_modifier'):
            if self.ps_cn():
                return True
        elif self.terminal_check('passive'):
            if self.am_cn():
                return True
        elif self.terminal_check('const'):
            if self.am_ps():
                return True
        elif self.match_all(['func', '[', 'ID']):
            return True
        return False

    def ps_cn(self):
        if self.terminal_check('passive'):
            if self.cn():
                return True
        elif self.terminal_check('const'):
            if self.ps():
                return True
        elif self.match_all(['func', '[', 'ID']):
            return True
        return False

    def am_cn(self):
        if self.terminal_check('access_modifier'):
            if self.cn():
                return True
        elif self.terminal_check('const'):
            if self.am():
                return True
        elif self.match_all(['func', '[', 'ID']):
            return True
        return False

    def am_ps(self):
        if self.terminal_check('access_modifier'):
            if self.ps():
                return True
        elif self.terminal_check('passive'):
            if self.am():
                return True
        elif self.match_all(['func', '[', 'ID']):
            return True
        return False

    def cdecs(self):
        if self.match_all(['ID']):
            if self.dec():
                if self.terminal_check(';'):
                    return True
        elif self.terminal_check('func'):
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
            if self.terminal_check('('):
                if self.params():
                    if self.terminal_check('{'):
                        if self.MST():
                            if self.terminal_check('}'):
                                return True
        return False

    def des_dec(self):
        if self.terminal_check('['):
            if self.terminal_check('ID'):
                if self.des_dec1():
                    return True
        return False

    def des_dec1(self):
        if self.terminal_check(','):
            if self.terminal_check('ID'):
                if self.des_dec1():
                    return True
        elif self.terminal_check(']'):
            if self.terminal_check(':'):
                if self.type():
                    if self.des_dec_assign4():
                        return True
        return False

    def cn(self):
        if self.terminal_check('const'):
            return True
        elif self.match_all(['func', '[', 'ID']):
            return True
        return False

    def am(self):
        if self.terminal_check('access_modifier'):
            return True
        elif self.match_all(['func', '[', 'ID']):
            return True
        return False

    def ps(self):
        if self.terminal_check('passive'):
            return True
        elif self.match_all(['func', '[', 'ID']):
            return True
        return False

    def abstract_class_def(self):
        if self.terminal_check('abstract'):
            if self.terminal_check('type'):
                if self.terminal_check('ID'):
                    if self.enhance():
                        if self.terminal_check('{'):
                            if self.abstract_body():
                                if self.terminal_check('}'):
                                    return True
        return False

    def abstract_body(self):
        if self.terminal_check('abstract'):
            if self.abstract_func():
                if self.abstract_body():
                    return True
        elif self.match_all(['access_modifier', 'passive', 'const', 'func', '[', 'ID']):
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
            if self.terminal_check('ID'):
                if self.terminal_check('('):
                    if self.params():
                        if self.terminal_check('->'):
                            if self.type_void():
                                if self.terminal_check(';'):
                                    return True
        return False

    def lang(self):
        if self.match_all(['const', 'func', 'type', '[', 'abstract', 'import', 'ID', '$']):
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
            if self.defs3():
                return True
        elif self.match_all(['ID']):
            if self.dec():
                if self.terminal_check(';'):
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
                    return True
        elif self.match_all(['[']):
            if self.des_dec():
                return True
        return False

    def defs1(self):
        if self.match_all(['abstract', 'ID', 'const', '[', 'type']):
            if self.defs():
                if self.defs1():
                    return True
        elif self.terminal_check('func'):
            if self.lang1():
                return True
        elif self.match_all(['$']):
            return True
        return False

    def defs2(self):
        if self.match_all(['abstract', 'ID', 'const', '[', 'type']):
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
            if self.terminal_check('('):
                if self.terminal_check(')'):
                    if self.terminal_check('->'):
                        if self.terminal_check('void'):
                            if self.terminal_check('{'):
                                if self.MST():
                                    if self.terminal_check('}'):
                                        return True
        return False

    def imports(self):
        if self.match_all(['import']):
            if self.import_pd():
                if self.imports1():
                    return True
        elif self.match_all(['abstract', 'const', 'func', 'type', '[', 'ID', '$']):
            return True
        return False

    def imports1(self):
        if self.match_all(['import']):
            if self.import_pd():
                if self.imports1():
                    return True
        elif self.match_all(['abstract', 'const', 'func', 'type', '[', 'ID', '$']):
            return True
        return False

    def import_pd(self):
        if self.terminal_check('import'):
            if self.terminal_check('ID'):
                if self.terminal_check('from'):
                    if self.terminal_check('str_const'):
                        return True
        return False

