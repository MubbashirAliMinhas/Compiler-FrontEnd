class MainTable:
    main_table = {}
    name = None

    def __init__(self):
        self.const = False
        self.abstract = False
        self.enhances = []
        self.mro = None
        self.CTR = {}
        # self.ACTR = {}
    
    @classmethod
    def insert(cls, mt_obj):
        MainTable.main_table[MainTable.name] = mt_obj
    
    def insert_CT(self, ct_obj):
        self.CTR[ClassTable.name] = ct_obj

    # def insert_ACT(self, act_obj):
    #     self.ACTR[AbstractClassTable.name] = act_obj

    @classmethod
    def lookup(cls, name):
        if name in cls.main_table:
            return cls.main_table[name]
        return False
    
    def lookup_CT(self, name):
        if name in self.CTR:
            return self.CTR[name]
        return False
    
    def lookup_enhanced(self, name):
        for x in range(len(self.enhances)):
            pass

    def __repr__(self):
        return f'({self.const}, {self.abstract}, {self.enhances}, {self.mro}, {self.CTR})'


def lookup_mro(name, mro, start=0):
    for x in range(start, len(mro)):
        if name in MainTable.main_table[mro[x]].CTR:
            return MainTable.main_table[mro[x]].CTR[name]
    return False


class ClassTable:
    name = None
    main_table_row = None
    constructor_present = False

    def __init__(self):
        self.Type = None
        self.AM = 'social'
        self.const = False
        self.passive = False
        self.assigned = False

    def __repr__(self) -> str:
        return f'({self.Type}, {self.AM}, {self.const}, {self.passive}, {self.assigned})'


class AbstractClassTable:
    name = None

    def __init__(self):
        self.Type = None
    
    def __repr__(self):
        return f'({self.Type})'


class GlobalTable:
    global_table = {}
    name = None
    main_table_row = None

    def __init__(self):
        self.Type = None
        self.const = False
        self.assigned = False
    
    @classmethod
    def insert(cls, gt_obj):
        cls.global_table[cls.name] = gt_obj
    
    @classmethod
    def lookup(cls, signature):
        if signature in cls.global_table:
            return cls.global_table[signature]
        return False

    def __repr__(self) -> str:
        return f'({self.Type}, {self.const}, {self.assigned})'

class FunctionTable:
    function_table = {}
    scope_stack = []
    scope = 0
    name = None

    def __init__(self):
        self.Type = None
        self.const = False
        self.assigned = False
    
    @classmethod
    def append(cls):
        cls.scope += 1
        cls.scope_stack.append(cls.scope)

    @classmethod
    def insert(cls, ft_obj):
        cls.function_table[f'{cls.scope}:{cls.name}'] = ft_obj
    
    @classmethod
    def pop(cls):
        cls.scope_stack.pop()
    
    @classmethod
    def lookup(cls, signature):
        for scope in cls.scope_stack:
            scoped_signature = f'{scope}:{signature}'
            if scoped_signature in cls.function_table:
                return cls.function_table[scoped_signature]
        return False

    def __repr__(self) -> str:
        return f'{self.Type}, {self.const}, {self.assigned}'


class Type:
    primitive_type = False
    name = None
    operator = None
    data_type = None
    return_flag = False
    return_type = None
    passive_flag = 1
    first_pass = True
    primitive_types = {'int', 'float', 'char', 'bool', 'str'}

    def __init__(self) -> None:
        self.Type = None
    
    def __repr__(self) -> str:
        return f'{self.Type}'


def compatibility(type1, type2, operator):
    if type1.Type == 'int' and type2.Type == 'int':
        if operator in ['||', '&&', 'relational']:
            type1.Type = 'bool'
        else:
            type1.Type = 'int'
    elif type1.Type in ['int', 'float'] and type2.Type in ['int', 'float']:
        if operator in ['||', '&&', 'relational']:
            type1.Type = 'bool'
        else:
            type1.Type = 'float'
    elif type1.Type == 'str' and type2.Type == 'str':
        if operator == '+':
            type1.Type = 'str'
        else:
            raise TypeError('Cannot use other operators with strings other than + for concatenation')
    else:
        raise TypeError('Cannot use given operators with these types.')


class Enhances:
    def __init__(self):
        self.enhances = {}
        self.mros = []

    def insert(self, name, mro):
        if name in self.enhances:
            print('Class duplication error')
        else:
            self.enhances[name] = 0
            self.mros.append(mro)

    def to_list(self):
        return list(self.enhances.keys())

class MRO:
    def __init__(self, name):
        if isinstance(name, list):
            self.MRO = name
        else:
            self.MRO = [name]
    
    def __getitem__(self, index):
        return self.MRO[index]

    def __len__(self):
        return len(self.MRO)
    
    def __iter__(self):
        for Type in self.MRO:
            yield Type

    def __contains__(self, name):
        if name in self.MRO:
            return True
        return False

    def merge(self, *others):
        self_i = 1
        offsets = [0 for x in range(len(others))]
        states = [None for x in range(len(others))]
        if len(others) > 1:
            iter_mros = others
            others = [{key: value for key, value in zip(other.MRO, range(len(other.MRO)))} for other in others]
            first_mro = iter_mros[0]
            first_i = 1
            key = first_mro[offsets[0]]
            while True:
                try:
                    for x in range(first_i, len(iter_mros)):
                        if key in others[x]:
                            if others[x][key] - offsets[x] == 0:
                                states[x] = True
                            else:
                                states[x] = False
                        else:
                            states[x] = None
                    
                    states[first_i - 1] = False
                    for x in range(first_i, len(iter_mros)):
                        if states[x] == False:
                            states[first_i - 1] = None
                            break
                    if states[first_i - 1] is not None:
                        for x in range(first_i, len(iter_mros)):
                            if states[x] == True:
                                states[first_i - 1] = True
                                break
                    
                    if states[first_i - 1] is None:
                        for x in range(1, len(iter_mros)):
                            if states[x] == False:
                                new_offset = others[x][key]
                                for _ in range(new_offset):
                                    self.MRO.append(iter_mros[x][offsets[x]])
                                    offsets[x] += 1
                    elif states[first_i - 1] == True:
                        for x in range(len(iter_mros)):
                            if states[x] == True:
                                offsets[x] += 1
                        self.MRO.append(key)
                        while offsets[first_i - 1] == len(first_mro):
                            first_mro = iter_mros[first_i]
                            first_i += 1
                        key = first_mro[offsets[first_i - 1]]  
                    else:
                        self.MRO.append(key)
                        if offsets[first_i - 1] < len(first_mro) - 1:
                            offsets[first_i - 1] += 1
                        else:
                            # states[first_i - 1] = 0
                            first_mro = iter_mros[first_i]
                            first_i += 1
                        key = first_mro[offsets[first_i - 1]]
                except IndexError:
                    break
        elif len(others) == 1:
            iter_mro = others[0].MRO
            self_i = 1
            for key in iter_mro:
                self.MRO.append(key)
                self_i += 1

    def __repr__(self) -> str:
        self.next_mro = iter(self.MRO)
        string = f'MRO({next(self.next_mro)}'
        for key in self.next_mro:
            string += f', {key}'
        string += ')'
        return string


from errors import *


def check_variable_nested(dtype, flag):
    if not Type.primitive_type:
        state = True
        state2 = True
        mro_state = True
        this_state = False
        row = None
        if not Type.first_pass:
            flag = 3
        if Type.passive_flag == 1:
            row = MainTable.lookup(Type.name)
            if row:
                Type.passive_flag = 2
                state = False
                state2 = False
                dtype.Type = Type.name
        if flag == 6 and state:
            mro_state = False
        elif flag == 5 and state:
            pass
        elif flag == 4 and state:
            this_state = True
        elif flag == 3 and state:
            mt_row = MainTable.lookup(dtype.Type)
            row = mt_row.lookup_CT(Type.name)
            passive_check = True
            if Type.passive_flag == 2:
                Type.passive_flag = 0
                passive_check = False
            if row:
                if row.passive == passive_check:
                    raise AccessError('Cannot access type attribute/method from object.')
                else:
                    state = False
            else:
                row = lookup_mro(Type.name, mt_row.mro, 1)
                if row:
                    if row.passive == passive_check:
                        raise AccessError('Cannot access type attribute/method from object.')
                    elif row.AM in ['secret', 'secure']:
                        raise AccessError('Cannot access secret attribute/method.')
                    else:
                        state = False
                else:
                    raise UndeclaredError('Undeclared.')
        if flag >= 2 and state and not this_state:
            row = FunctionTable.lookup(Type.name)
            if row:
                state = False
        if flag >= 1 and state and mro_state:
            mt_row = ClassTable.main_table_row
            row = mt_row.lookup_CT(Type.name)
            if row:
                if row.passive:
                    raise AccessError('Cannot access type attribute/method from object.')
                else:
                    state = False
            else:
                row = lookup_mro(Type.name, mt_row.mro, 1)
                if row:
                    if row.passive:
                        raise AccessError('Cannot access type attribute/method from object.')
                    elif row.AM == 'secret':
                        raise AccessError('Cannot access secret attribute/method.')
                    else:
                        state = False
                elif this_state:
                    raise UndeclaredError('Undeclared')
        if flag >= 0 and state:
            row = GlobalTable.lookup(Type.name)
            if not row:
                raise UndeclaredError('Undeclared.')
        if state2 and not row.assigned:
            raise ValueError('Variable is not assigned.')
        if state2:
            dtype.Type = row.Type


def check_variable(dtype, flag):
    if not Type.primitive_type:
        if MainTable.lookup(Type.name):
            raise ObjectCreationError('Cannot directly call type to create an object.')
        state = True
        mro_state = True
        this_state = False
        row = None
        if not Type.first_pass:
            flag = 3
        if flag == 6:
            mro_state = False
        elif flag == 5:
            pass
        elif flag == 4:
            this_state = True
        elif flag == 3:
            mt_row = MainTable.lookup(dtype.Type)
            row = mt_row.lookup_CT(Type.name)
            passive_check = True
            if Type.passive_flag == 2:
                passive_check = False
            if row:
                if row.passive == passive_check:
                    raise AccessError('Cannot access type attribute/method from object.')
                else:
                    state = False
            else:
                row = lookup_mro(Type.name, mt_row.mro, 1)
                if row:
                    if row.passive == passive_check:
                        raise AccessError('Cannot access type attribute/method from object.')
                    elif row.AM == 'secret':
                        raise AccessError('Cannot access secret attribute/method.')
                    else:
                        state = False
                else:
                    raise UndeclaredError('Undeclared.')
        if flag >= 2 and state and not this_state:
            row = FunctionTable.lookup(Type.name)
            if row:
                state = False
        if flag >= 1 and state and mro_state:
            mt_row = ClassTable.main_table_row
            row = mt_row.lookup_CT(Type.name)
            if row:
                if row.passive:
                    raise AccessError('Cannot access type attribute/method from object.')
                else:
                    state = False
            else:
                row = lookup_mro(Type.name, mt_row.mro, 1)
                if row:
                    if row.passive:
                        raise AccessError('Cannot access type attribute/method from object.')
                    elif row.AM == 'secret':
                        raise AccessError('Cannot access secret attribute/method.')
                    else:
                        state = False
                elif this_state:
                    raise UndeclaredError('Undeclared')
        if flag >= 0 and state:
            row = GlobalTable.lookup(Type.name)
            if not row:
                raise UndeclaredError('Undeclared.')
        if not row.assigned:
            raise ValueError('Variable is not assigned.')
        dtype.Type = row.Type


if __name__ == '__main__':
    # mro1 = MRO(['D', 'E', 'G', 'H', 'F'])
    # mro2 = MRO(['B', 'C', 'E', 'G', 'H'])
    # mro3 = MRO(['E', 'G'])
    mro1 = MRO(['B', 'C', 'D'])
    mro2 = MRO(['E', 'F', 'G'])
    mro3 = MRO(['H', 'I', 'J'])
    # mro1 = MRO({'E': 0, 'G': 1, 'H': 2})
    # mro2 = MRO({'H': 0})
    mro4 = MRO('A')

    mro4.merge(mro1)
    print(mro4.MRO)