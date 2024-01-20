from match_re import Match_re

non_terminal = '<\w*>'
arrow = ' *-> *'
terminal = '[^< \n|]+ ?'
null = 'Ïµ'
all = f'{null}|{non_terminal}|{terminal}'

file_path = 'cfg.txt'

def reconstruct():
    cfg_ds = {}
    with open(file_path, 'r') as cfg_text:
        matcher = Match_re()
        # i = 0
        for cfg_line in cfg_text:
            matcher.match(non_terminal, cfg_line)
            matcher.dispatch_pattern()
            key = matcher.fragment

            matcher.change_pattern(arrow)
            matcher.dispatch_pattern()
            
            value = []
            rule = []
            matcher.change_pattern(all)
            while matcher.index != len(cfg_line) - 1:
                matcher.dispatch_pattern()
                rule.append(matcher.fragment.strip())
                if matcher.compare('|'):
                    matcher.index += 1
                    value.append(rule)
                    rule = []
            value.append(rule)
            cfg_ds[key] = value

    cfg_ds['<OE1>'][0][0] = '||'
    return cfg_ds

def print_dict(dict_name):
    for key, value in dict_name.items():
        print(key, value)

__all__ = [null, reconstruct, non_terminal, print_dict]