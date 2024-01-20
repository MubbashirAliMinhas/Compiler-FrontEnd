class TokenReader:
    def __init__(self):
        self.token_file = open('tokens.txt', 'r')
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
        self.token = self.token_file.readline().split('#')