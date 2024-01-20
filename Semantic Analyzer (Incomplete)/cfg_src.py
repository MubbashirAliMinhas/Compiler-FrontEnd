from token_reader import TokenReader
from symbol_table import *
from errors import *

class CFG:
    def __init__(self):
        self.tokens = TokenReader()

    def validate(self):
        self.tokens.next_line()
        if self.lang():
            if self.tokens.class_part == '$':
                for key in MainTable.main_table:
                    print(key, MainTable.main_table[key])
                print(GlobalTable.global_table)
                print(FunctionTable.function_table)
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
            if self.var_fn_assign4():
                return True
        elif self.terminal_check('inc_dec'):
            return True
        elif self.match_all(['=', 'compound_assignment']):
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

    def assign1(self, dtype, flag):
        if self.terminal_check('ID'):
            Type.name = self.tokens.value_part_p()
            if self.assign2(dtype, flag):
                return True
        elif self.match_all(['self', 'grand']):
            if self.this_super():
                if self.terminal_check('ID'):
                    if self.assign2():
                        return True
        elif self.match_all(['(', '!', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'PM', 'make']):
            if self.exp1(dtype, flag):
                return True
        elif self.terminal_check('inc_dec'):
            if self.var():
                if self.unpacked():
                    return True
        return False

    def exp1(self, dtype, flag):
        if self.match_all(['(']):
            if self.B():
                if self.unpacked():
                    return True
        elif self.terminal_check('!'):
            if self.F():
                if self.unpacked():
                    return True
        elif self.match_all(['int_const', 'float_const', 'char_const', 'str_const', 'bool_const']):
            if self.const(dtype):
                if self.unpacked(dtype, flag):
                    return True
        elif self.terminal_check('PM'):
            if self.F():
                if self.unpacked():
                    return True
        elif self.match_all(['make']):
            if self.obj_dec(dtype, flag):
                return True
        return False

    def assign2(self, dtype, flag):
        if self.match_all(['[']):
            if self.array_index():
                if self.assign3():
                    return True
        elif self.match_all(['.', '^', 'MDM', 'PM', 'relational', '&&', '||', 'inc_dec', 'as', '=', 'compound_assignment', ';']):
            if self.assign3(dtype, flag):
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.assign4():
                    return True
        return False

    def assign3(self, dtype, flag):
        if self.terminal_check('.'):
            check_variable_nested(dtype, flag)
            Type.first_pass = False
            if self.assign5(dtype, flag):
                return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ';']):
            if self.unpacked(dtype, flag):
                return True
        elif self.terminal_check('inc_dec'):
            if self.unpacked():
                return True
        elif self.terminal_check('as'):
            if self.type():
                if self.unpacked():
                    return True
        elif self.match_all(['=', 'compound_assignment']):
            if self.equals():
                if self.assign1():
                    return True
        return False

    def assign4(self, dtype, flag):
        if self.terminal_check('.'):
            if self.assign5(dtype, flag):
                return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ';']):
            if self.unpacked(dtype, flag):
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

    def assign5(self, dtype, flag):
        if self.terminal_check('ID'):
            Type.name = self.tokens.value_part_p()
            if self.assign2(dtype, flag):
                return True
        return False

    def equals(self):
        if self.terminal_check('='):
            return True
        elif self.terminal_check('compound_assignment'):
            return True
        return False

    def dec(self, data, flag):
        if self.terminal_check('ID'):
            type(data).name = self.tokens.value_part_p()
            if MainTable.lookup(type(data).name):
                raise NameError('Variable name cannot be same as Type.')
            if self.dec1(data, flag):
                return True
        return False

    def dec1(self, data, flag):
        if self.terminal_check(':'):
            if self.type(data):
                Type.data_type = data.Type
                if self.dec2(data, flag):
                    return True
        return False

    def dec2(self, data, flag):
        if self.terminal_check('='):
            dtype = Type()
            Type.primitive_type = False
            if self.dec3(dtype, flag):
                if dtype.Type not in Type.primitive_types:
                    mt_row = MainTable.lookup(dtype.Type)
                    if dtype.Type != Type.data_type:
                        if Type.data_type not in mt_row.mro:
                            raise TypeError('Cannot create variable with incompatible type.')
                elif data.Type != dtype.Type:
                    raise TypeError('Cannot create variable with incompatible type.')
                data.assigned = True
                return True
        elif self.match_all([';']):
            if data.const == True:
                raise ConstantError('Constants must be declared')
            return True
        return False


    def dec3(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', '(', '!', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'PM', 'make', 'inc_dec']):
            if self.assign1(dtype, flag):
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
        elif self.match_all(['[', ':']):
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
        if self.match_all(['ID', 'self', 'grand', '(', '!', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'PM', 'make']):
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
                    if self.var():
                        return True
        elif self.terminal_check('.'):
            if self.var():
                return True
        return False

    def var3(self):
        if self.terminal_check('.'):
            if self.var():
                return True
        elif self.match_all(['[']):
            if self.array_index():
                if self.var2():
                    return True
        return False

    def operand(self, dtype, flag):
        if self.terminal_check('ID'):
            Type.name = self.tokens.value_part_p()
            if self.operand1(dtype, flag):
                return True
        elif self.match_all(['self', 'grand']):
            if self.this_super():
                if self.terminal_check('ID'):
                    if self.operand1():
                        return True
        elif self.match_all(['int_const', 'float_const', 'char_const', 'str_const', 'bool_const']):
            if self.const(dtype):
                return True
        elif self.terminal_check('inc_dec'):
            if self.var():
                return True
        return False

    def operand1(self, dtype, flag):
        if self.match_all(['[']):
            if self.array_index():
                if self.operand2(dtype, flag):
                    return True
        elif self.match_all(['.', 'inc_dec', 'as', '^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            if self.operand2(dtype, flag):
                return True
        elif self.match_all(['(']):
            if self.args():
                if self.operand3():
                    return True
        return False

    def operand2(self, dtype, flag):
        if self.terminal_check('.'):
            check_variable_nested(dtype, flag)
            Type.first_pass = False
            if self.operand4(dtype, flag):
                return True
        elif self.terminal_check('inc_dec'):
            return True
        elif self.terminal_check('as'):
            if self.type():
                return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def operand3(self, dtype, flag):
        if self.terminal_check('.'):
            check_variable_nested(dtype, flag)
            Type.first_pass = False
            if self.operand4(dtype, flag):
                return True
        elif self.match_all(['[']):
            if self.array_index():
                if self.operand2():
                    return True
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def operand4(self, dtype, flag):
        if self.terminal_check('ID'):
            Type.name = self.tokens.value_part_p()
            if self.operand1(dtype, flag):
                return True
        return False

    def OE(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.AE(dtype, flag):
                if self.OE1(dtype, flag):
                    return True
        return False

    def OE1(self, dtype, flag):
        if self.terminal_check('||'):
            dtype2 = Type()
            Type.operator = self.tokens.class_part_p()
            if self.AE(dtype2, flag):
                compatibility(dtype, dtype2, Type.operator)
                if self.OE1(dtype, flag):
                    return True
        elif self.match_all([':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def AE(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.RE(dtype, flag):
                if self.AE1(dtype, flag):
                    return True
        return False

    def AE1(self, dtype, flag):
        if self.terminal_check('&&'):
            dtype2 = Type()
            Type.operator = self.tokens.class_part_p()
            if self.RE(dtype2, flag):
                compatibility(dtype, dtype2, Type.operator)
                if self.AE1(dtype, flag):
                    return True
        elif self.match_all(['||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def RE(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.E(dtype, flag):
                if self.RE1(dtype, flag):
                    return True
        return False

    def RE1(self, dtype, flag):
        if self.terminal_check('relational'):
            dtype2 = Type()
            Type.operator = self.tokens.class_part_p()
            if self.E(dtype2, flag):
                compatibility(dtype, dtype2, Type.operator)
                if self.RE1(dtype, flag):
                    return True
        elif self.match_all(['&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def E(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.T(dtype, flag):
                if self.E1(dtype, flag):
                    return True
        return False

    def E1(self, dtype, flag):
        if self.terminal_check('PM'):
            dtype2 = Type()
            Type.operator = self.tokens.class_part_p()
            if self.T(dtype2, flag):
                compatibility(dtype, dtype2, Type.operator)
                if self.E1(dtype, flag):
                    return True
        elif self.match_all(['relational', '&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def T(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.P(dtype, flag):
                if self.T1(dtype, flag):
                    return True
        return False

    def T1(self, dtype, flag):
        if self.terminal_check('MDM'):
            dtype2 = Type()
            Type.operator = self.tokens.class_part_p()
            if self.P(dtype2, flag):
                compatibility(dtype, dtype2, Type.operator)
                if self.T1(dtype, flag):
                    return True
        elif self.match_all(['PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False

    def P(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.F(dtype, flag):
                check_variable(dtype, flag)
                Type.first_pass = True
                if self.P1(dtype, flag):
                    return True
        return False

    def P1(self, dtype, flag):
        if self.terminal_check('^'):
            dtype2 = Type()
            Type.operator = self.tokens.class_part_p()
            if self.F(dtype2, flag):
                compatibility(dtype, dtype2, Type.operator)
                if self.P1(dtype, flag):
                    return True
        elif self.match_all(['MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', '}', 'range']):
            return True
        return False


    def F(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec']):
            if self.operand(dtype, flag):
                return True
        elif self.match_all(['(']):
            if self.B(dtype, flag):
                return True
        elif self.terminal_check('!'):
            if self.F(dtype, flag):
                return True
        elif self.terminal_check('PM'):
            if self.F(dtype, flag):
                return True
        return False

    def B(self, dtype, flag):
        if self.terminal_check('('):
            if self.exp(dtype, flag):
                if self.terminal_check(')'):
                    return True
        return False

    def exp(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.OE(dtype, flag):
                return True
        elif self.match_all(['make']):
            if self.obj_dec(dtype, flag):
                return True
        return False

    def unpacked(self, dtype, flag):
        if self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ';']):
            check_variable(dtype, flag)
            Type.first_pass = True
            if self.P1(dtype, flag):
                if self.T1(dtype, flag):
                    if self.E1(dtype, flag):
                        if self.RE1(dtype, flag):
                            if self.AE1(dtype, flag):
                                if self.OE1(dtype, flag):
                                    return True
        return False

    def obj_dec(self, dtype, flag):
        if self.terminal_check('make'):
            if self.obj_dec1(dtype, flag):
                return True
        return False

    def obj_dec1(self, dtype, flag):
        if self.terminal_check('str'):
            if self.obj_dec2(dtype, flag):
                return True
        elif self.terminal_check('ID'):
            dtype.Type = self.tokens.value_part_p()
            mt_row = MainTable.lookup(dtype.Type)
            if not mt_row:
                raise TypeError('Type is not declared.')
            if self.obj_dec2(mt_row, dtype, flag):
                return True
        elif self.terminal_check('primitive_type'):
            if self.array_ref():
                return True
        return False

    def obj_dec2(self, mt_row, dtype, flag):
        if self.match_all(['(']):
            Type.name = 'constructor['
            dtype2 = Type()
            if self.args(dtype2, flag):
                ct_row = mt_row.lookup_CT(Type.name)
                if not ct_row:
                    raise UndeclaredError('Constructor with these parameters is not declared.')
                elif ct_row.AM != 'social':
                    raise ObjectCreationError('Cannot create object because constructor is private.')
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
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', 'make']):
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
        elif self.match_all([':', ';', ',', '->', ']', ')', 'range']):
            return True
        return False


    def array_ref_exp(self):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', 'make']):
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
        elif self.match_all([':', ';', ',', '->', ']', ')', 'range']):
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
        elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', ':', ';', ',', '->', ']', ')', 'range', '.', 'inc_dec', '=', 'compound_assignment', 'as']):
            return True
        return False


    def args(self, dtype, flag):
        if self.terminal_check('('):
            if self.args1(dtype, flag):
                return True
        return False

    def args1(self, dtype, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            if self.exp(dtype, flag):
                Type.name += dtype.Type
                if self.args2(dtype, flag):
                    return True
        elif self.terminal_check(')'):
            Type.name += ']'
            return True
        return False

    def args2(self, dtype, flag):
        if self.terminal_check(','):
            Type.name += ','
            if self.exp(dtype, flag):
                Type.name += dtype.Type
                if self.args2(dtype, flag):
                    return True
        elif self.terminal_check(')'):
            Type.name += ']'
            return True
        return False

    def type(self, data, scope_data=None):
        if scope_data is None:
            if self.terminal_check('str'):
                data.Type = self.tokens.value_part_p()
                if self.dim(data):
                    return True
            elif self.terminal_check('primitive_type'):
                data.Type = self.tokens.value_part_p()
                if self.dim(data):
                    return True
            elif self.terminal_check('ID'):
                data.Type = self.tokens.value_part_p()
                if not MainTable.lookup(data.Type):
                    raise UndeclaredError('Undeclared type')
                if self.dim(data):
                    return True
            return False
        elif isinstance(scope_data, FunctionTable):
            if self.terminal_check('str'):
                type(data).name += self.tokens.value_part_p()
                scope_data.Type = self.tokens.value_part_p()
                if self.dim(data, scope_data):
                    return True
            elif self.terminal_check('primitive_type'):
                type(data).name += self.tokens.value_part_p()
                scope_data.Type = self.tokens.value_part_p()
                if self.dim(data, scope_data):
                    return True
            elif self.terminal_check('ID'):
                type(data).name += self.tokens.value_part_p()
                scope_data.Type = self.tokens.value_part_p()
                if self.dim(data, scope_data):
                    return True
            return False

    def dim(self, data, scope_data=None):
        if scope_data is None:
            if self.terminal_check('['):
                data.Type += self.tokens.value_part_p()
                if self.terminal_check(']'):
                    data.Type += self.tokens.value_part_p()
                    if self.dim(data):
                        return True
            elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', '=', 'in', 'range', ',', ')', '{', ';']):
                return True
            return False
        elif isinstance(scope_data, FunctionTable):
            if self.terminal_check('['):
                type(data).name += self.tokens.value_part_p()
                scope_data.Type += self.tokens.value_part_p()
                if self.terminal_check(']'):
                    type(data).name += self.tokens.value_part_p()
                    scope_data.Type += self.tokens.value_part_p()
                    if self.dim(data, scope_data):
                        return True
            elif self.match_all(['^', 'MDM', 'PM', 'relational', '&&', '||', '=', 'in', 'range', ',', ')', '{', ';']):
                return True
            return False


    def body(self):
        if self.terminal_check(';'):
            return True
        elif self.match_all(['ID', 'const', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[']):
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
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', '[', 'make']):
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
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM', 'make']):
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
            if self.body():
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
        elif self.match_all(['finally', 'ID', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[', '}', 'else']):
            return True
        return False


    def finally_pd(self):
        if self.terminal_check('finally'):
            if self.terminal_check('{'):
                if self.MST():
                    if self.terminal_check('}'):
                        return True
        elif self.match_all(['ID', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[', '}', 'else']):
            return True
        return False


    def const(self, dtype):
        Type.primitive_type = True
        if self.terminal_check('int_const'):
            dtype.Type = 'int'
            return True
        elif self.terminal_check('float_const'):
            dtype.Type = 'float'
            return True
        elif self.terminal_check('char_const'):
            dtype.Type = 'char'
            return True
        elif self.terminal_check('str_const'):
            dtype.Type = 'str'
            return True
        elif self.terminal_check('bool_const'):
            dtype.Type = 'bool'
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
        elif self.match_all(['ID', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[', '}', 'else']):
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

    def func_dec(self, data, flag):
        if self.terminal_check('func'):
            if self.func_dec1(data, flag):
                return True
        return False

    def func_dec1(self, data, flag):
        Type.return_flag = False
        if self.terminal_check('ID'):
            type(data).name = self.tokens.value_part_p()
            if self.terminal_check('('):
                type(data).name += '['
                scope_data = FunctionTable()
                FunctionTable.append()
                if self.params(data, scope_data):
                    if self.terminal_check('->'):
                        if self.type_void(data):
                            if data.Type == 'void':
                                Type.return_flag = True
                            Type.return_type = data.Type
                            if flag == 6:
                                if GlobalTable.lookup(GlobalTable.name):
                                    raise RedeclarationError('Redeclaration')
                                else:
                                    GlobalTable.insert(data)
                            else:
                                mt_data = ClassTable.main_table_row
                                if mt_data.lookup_CT(ClassTable.name):
                                    raise RedeclarationError('Redeclaration')
                                if ClassTable.name not in 'constructor':
                                    mro_data = lookup_mro(ClassTable.name, mt_data.mro, 1)
                                    if mro_data and mro_data.AM in ['social', 'secure']:
                                        if data.Type != mro_data.Type:
                                            raise OverridingError('Cannot override method with different return type.')
                                        elif mro_data.passive:
                                            raise OverridingError('Cannot override a passive method.')
                                        elif mro_data.const:
                                            raise OverridingError('Cannot override a constant method.')
                                    mt_data.insert_CT(data)
                            if self.terminal_check('{'):
                                if self.MST(flag):
                                    if self.terminal_check('}'):
                                        FunctionTable.pop()
                                        return True
        return False

    def params(self, data, scope_data):
        if self.terminal_check('ID'):
            FunctionTable.name = self.tokens.value_part_p()
            if FunctionTable.lookup(FunctionTable.name):
                raise RedeclarationError('Redeclaration')
            elif MainTable.lookup(FunctionTable.name):
                raise NameError('Variable name cannot be same as Type')
            if self.terminal_check(':'):
                if self.type(data, scope_data):
                    FunctionTable.insert(scope_data)
                    if self.params1(data, scope_data):
                        return True
        elif self.terminal_check(')'):
            type(data).name += ']'
            return True
        return False

    def params1(self, data, scope_data):
        if self.terminal_check(','):
            type(data).name += self.tokens.value_part_p()
            if self.terminal_check('ID'):
                FunctionTable.name = self.tokens.value_part_p()
                if FunctionTable.lookup(FunctionTable.name):
                    raise RedeclarationError('Redeclaration')
                elif MainTable.lookup(FunctionTable.name):
                    raise NameError('Variable name cannot be same as Type')
                if self.terminal_check(':'):
                    if self.type(data, scope_data):
                        FunctionTable.insert(scope_data)
                        if self.params1(data, scope_data):
                            return True
        elif self.terminal_check(')'):
            type(data).name += ']'
            return True
        return False

    def type_void(self, data):
        if self.match_all(['str', 'primitive_type', 'ID']):
            if self.type(data):
                return True
        elif self.terminal_check('void'):
            data.Type = self.tokens.value_part_p()
            return True
        return False

    def inc_dec_st(self):
        if self.terminal_check('inc_dec'):
            if self.var():
                if self.terminal_check(';'):
                    return True
        return False

    def SST(self, flag):
        if self.terminal_check('ID'):
            scope_data = FunctionTable()
            FunctionTable.name = self.tokens.value_part_p()
            if FunctionTable.lookup(FunctionTable.name):
                raise RedeclarationError('Redeclaration')
            elif MainTable.lookup(FunctionTable.name):
                raise NameError('Variable name cannot be same as Type')
            if self.SST1(scope_data, flag):
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
            if self.return_st(flag):
                return True
        elif self.terminal_check('continue_break'):
            if self.terminal_check(';'):
                return True
        elif self.match_all(['[']):
            if self.des_dec_assign():
                return True
        return False

    def SST1(self, scope_data, flag):
        if self.match_all([':']):
            if self.dec1(scope_data, flag):
                FunctionTable.insert(scope_data)
                if self.terminal_check(';'):
                    return True
        elif self.match_all(['[', '.', 'inc_dec', '=', '(']):
            if self.var_fn_assign1():
                if self.terminal_check(';'):
                    return True
        return False

    def SST2(self):
        if self.terminal_check('ID'):
            if self.dec1():
                if self.terminal_check(';'):
                    return True
        elif self.match_all(['ID']):
            if self.des_dec_assign():
                return True
        return False

    def MST(self, flag):
        if self.match_all(['ID', 'const', 'self', 'grand', 'inc_dec', 'if', 'match', 'while', 'for', 'try', 'return', 'continue_break', '[']):
            if self.SST(flag):
                if self.MST(flag):
                    return True
        elif self.match_all(['}']):
            return True
        return False


    def return_st(self, flag):
        if self.terminal_check('return'):
            if self.return_exp(flag):
                return True
        return False

    def return_exp(self, flag):
        if self.match_all(['ID', 'self', 'grand', 'int_const', 'float_const', 'char_const', 'str_const', 'bool_const', 'inc_dec', '(', '!', 'PM']):
            rtype = Type()
            if self.exp(rtype, flag):
                if rtype.Type not in Type.primitive_types:
                    mt_row = MainTable.lookup(rtype.Type)
                    if rtype.Type != Type.return_type:
                        if Type.data_type not in mt_row.mro:
                            raise TypeError('Cannot create function with incompatible type.')
                elif Type.return_type != rtype.Type:
                    raise TypeError('Cannot create function with incompatible type.')
                Type.return_flag = True
                if self.terminal_check(';'):
                    return True
        elif self.terminal_check(';'):
            return True
        return False

    def class_def(self, data):
        ClassTable.constructor_present = False
        if self.terminal_check('type'):
            if self.terminal_check('ID'):
                MainTable.name = self.tokens.value_part_p()
                if MainTable.lookup(MainTable.name):
                    raise RedeclarationError(f'{MainTable.name} already declared')
                MainTable.insert(data)
                enhances = Enhances()
                data.enhances = enhances
                if self.enhance(enhances):
                    if MainTable.name in data.enhances.enhances:
                        raise DuplicationError('Cannot enhance current class')
                    data.mro = MRO(MainTable.name)
                    data.mro.merge(*data.enhances.mros)
                    data.enhances = data.enhances.to_list()
                    if self.terminal_check('{'):
                        if self.class_body(data):
                            if not ClassTable.constructor_present:
                                init_data = ClassTable()
                                init_data.Type = 'void'
                                ClassTable.name = 'constructor[]'
                                data.insert_CT(init_data)
                            if self.terminal_check('}'):
                                return True
        return False

    def enhance(self, enhances):
        if self.terminal_check('enhances'):
            if self.terminal_check('ID'):
                name = self.tokens.value_part_p()
                e_data = MainTable.lookup(name)
                if not e_data:
                    raise UndeclaredError(f'Class {name} does not exist')
                elif e_data.const == True:
                    raise ConstantError('Constant class cannot be enhancible')
                else:
                    enhances.insert(name, e_data.mro)
                if self.enhance1(enhances):
                    return True
        elif self.match_all(['{']):
            return True
        return False


    def enhance1(self, enhances):
        if self.terminal_check(','):
            if self.terminal_check('ID'):
                name = self.tokens.value_part_p()
                e_data = MainTable.lookup(name)
                if not e_data:
                    raise UndeclaredError(f'Class {name} does not exist')
                elif e_data.const == True:
                    raise ConstantError('Constant class cannot be enhancible')
                else:
                    enhances.insert(name, e_data.mro)
                if self.enhance1(enhances):
                    return True
        elif self.match_all(['{']):
            return True
        return False


    def class_body(self, data):
        if self.match_all(['access_modifier', 'passive', 'const', 'ID', 'func', '[']):
            class_table_row = ClassTable()
            ClassTable.main_table_row = data
            if self.cb_am_ps_cn(class_table_row):
                if self.class_body(data):
                    return True
        elif self.match_all(['}']):
            return True
        return False


    def cb_am_ps_cn(self, data):
        if self.terminal_check('access_modifier'):
            data.AM = self.tokens.value_part_p()
            if self.cb_am_ps_cn1(data):
                return True
        elif self.terminal_check('passive'):
            data.passive = True
            if self.am_cn(data):
                if self.adecs(data):
                    return True
        elif self.terminal_check('const'):
            data.const = True
            if self.am_ps(data):
                if self.adecs(data):
                    return True
        elif self.match_all(['ID', 'func', '[']):
            if self.cdecs(data):
                return True
        return False

    def cb_am_ps_cn1(self, data):
        if self.match_all(['ID', 'func', '[']):
            if self.cdecs(data):
                return True
        elif self.terminal_check('passive'):
            data.passive = True
            if self.cn(data):
                if self.adecs(data):
                    return True
        elif self.terminal_check('const'):
            data.const = True
            if self.ps(data):
                if self.adecs(data):
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
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def ps_cn(self, data):
        if self.terminal_check('passive'):
            data.passive = True
            if self.cn(data):
                return True
        elif self.terminal_check('const'):
            data.const = True
            if self.ps(data):
                return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def am_cn(self, data):
        if self.terminal_check('access_modifier'):
            data.AM = self.tokens.value_part_p()
            if self.cn(data):
                return True
        elif self.terminal_check('const'):
            data.const = True
            if self.am(data):
                return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def am_ps(self, data):
        if self.terminal_check('access_modifier'):
            data.AM = self.tokens.value_part_p()
            if self.ps(data):
                return True
        elif self.terminal_check('passive'):
            data.passive = True
            if self.am(data):
                return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def cdecs(self, data):
        if self.match_all(['ID']):
            if self.dec(data, 1):
                ClassTable.main_table_row.insert_CT(data)
                if self.terminal_check(';'):
                    return True
        elif self.terminal_check('func'):
            if self.fn_init_dec(data, 1):
                return True
        elif self.match_all(['[']):
            if self.des_dec():
                return True
        return False

    def fn_init_dec(self, data, flag):
        if self.match_all(['ID']):
            if self.func_dec1(data, 2):
                return True
        elif self.terminal_check('constructor'):
            ClassTable.constructor_present = True
            ClassTable.name = self.tokens.value_part_p()
            scope_data = FunctionTable()
            FunctionTable.append()
            if self.terminal_check('('):
                ClassTable.name += '['
                if self.params(data, scope_data):
                    data.Type = 'void'
                    mt_data = ClassTable.main_table_row
                    if mt_data.lookup_CT(ClassTable.name):
                        raise RedeclarationError('Redeclaration')
                    mt_data.insert_CT(data)
                    if self.terminal_check('{'):
                        if self.MST(2):
                            if self.terminal_check('}'):
                                FunctionTable.pop()
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

    def cn(self, data):
        if self.terminal_check('const'):
            data.const = True
            return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def am(self, data):
        if self.terminal_check('access_modifier'):
            data.AM = True
            return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def ps(self, data):
        if self.terminal_check('passive'):
            data.passive = True
            return True
        elif self.match_all(['ID', 'func', '[']):
            return True
        return False


    def abstract_class_def(self, data):
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
        elif self.match_all(['access_modifier', 'passive', 'const', 'ID', 'func', '[']):
            if self.am_ps_cn():
                if self.adecs():
                    if self.abstract_body():
                        return True
        elif self.match_all(['}']):
            return True
        return False


    def adecs(self, data):
        if self.match_all(['ID']):
            if self.dec(data, 1):
                ClassTable.main_table_row.insert_CT(data)
                if self.terminal_check(';'):
                    return True
        elif self.match_all(['func']):
            if self.func_dec(data, 1):
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
        if self.match_all(['import', 'const', 'type', 'abstract', 'ID', 'func', '[', '$']):
            if self.imports():
                if self.defs1():
                    return True
        return False

    def defs(self):
        data = MainTable()
        if self.match_all(['type']):
            if self.class_def(data):
                return True
        elif self.match_all(['abstract']):
            data.abstract = True
            if self.abstract_class_def(data):
                return True
        elif self.terminal_check('const'):
            if self.defs3(True):
                return True
        elif self.match_all(['ID']):
            global_data = GlobalTable()
            if self.dec(global_data, 0):
                if GlobalTable.lookup(GlobalTable.name):
                    raise RedeclarationError('redeclaration')
                else:
                    GlobalTable.insert(global_data)
                if self.terminal_check(';'):
                    return True
        elif self.match_all(['[']):
            if self.des_dec():
                return True
        return False

    def defs3(self, const):
        if self.match_all(['type']):
            data = MainTable()
            data.const = const
            if self.class_def():
                return True
        elif self.match_all(['ID']):
            global_data = GlobalTable()
            global_data.const = const
            if self.dec(global_data, 0):
                GlobalTable.insert(global_data)
                if self.terminal_check(';'):
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
            if self.func_dec(6):
                if self.defs2():
                    return True
        elif self.match_all(['$']):
            return True
        return False


    def lang1(self):
        if self.match_all(['ID']):
            global_data = GlobalTable()
            if self.func_dec1(global_data, 6):
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
            if self.terminal_check('ID'):
                if self.terminal_check('from'):
                    if self.terminal_check('str_const'):
                        if self.terminal_check(';'):
                            return True
        return False

