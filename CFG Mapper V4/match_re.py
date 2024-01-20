import re

class Match_re:
    def __init__(self, pattern=None, string=None):
        self.pattern: str = pattern
        self.string: str = string
        self.fragment: str = None
        self.index: int = 0

    def dispatch_pattern(self):
        re_compile = re.compile(self.pattern)
        re_match = re_compile.match(self.string, self.index)
        if re_match:
            self.fragment = self.string[re_match.start():re_match.end()]
            self.index = re_match.end()
        return re_match
    
    def match(self, pattern, string):
        self.pattern = pattern
        self.string = string
        self.index = 0
    
    def change_pattern(self, pattern):
        self.pattern = pattern
    
    def compare(self, token):
        return self.string[self.index] == token