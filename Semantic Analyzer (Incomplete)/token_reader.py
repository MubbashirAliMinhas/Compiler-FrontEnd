class TokenReader:
    def __init__(self):
        self.token_file = open('tokens.txt', 'r')
        self.token_file = self.token_file.readlines()
        self.index = 0
        self.token = None
    
    @property
    def class_part(self):
        return self.token[0]
    
    @property
    def value_part(self):
        return self.token[1]
    
    @property
    def line_no(self):
        return self.token[2]

    def next_line(self):
        self.token = self.token_file[self.index].split('#')
        self.index += 1
    
    def value_part_p(self, prev=2):
        return self.token_file[self.index - prev].split('#')[1]
    
    def class_part_p(self, prev=2):
        return self.token_file[self.index - prev].split('#')[0]