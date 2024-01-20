from reconstruct_cfg import reconstruct, null
from production_locations import production_locations

cfg_ds = reconstruct()
pd_locations = production_locations(cfg_ds)

first_set = {}

def merge(pd):
    fs_all = set()
    for fs in first_set[pd]:
        fs_all.update(fs)
    first_set[pd].append(fs_all)

def first(pd):
    if pd in first_set:
        return first_set[pd][-1]
    first_set[pd] = []
    for rule in cfg_ds[pd]:
        fs = set()
        for ntnt in rule:
            if ntnt[0] == '<':
                fs.update(first(ntnt))
                if null in fs:
                    if ntnt == rule[-1]:
                        continue
                    fs.remove(null)
                    continue
            else:
                fs.add(ntnt)
            break
        first_set[pd].append(fs)
    merge(pd)
    return first_set[pd][-1]

def gen_first_set():
    for pd in cfg_ds:
        first(pd)

follow_set = {}
follow_set['<lang>'] = {'$'}
recall_pd = set()
validate_pd = set()

def follow1(pd, bypass=False):
    if pd in follow_set and follow_set[pd]:
        return follow_set[pd]
    follow_set[pd] = set()
    for pd_lc, lc in pd_locations[pd].items():
        for x in range(0, len(lc), 2):
            rule = lc[x]
            pos = lc[x + 1]
            ntnt_ls = cfg_ds[pd_lc][rule]
            if len(ntnt_ls) == pos + 1:
                if pd_lc in follow_set and not follow_set[pd_lc] and not bypass:
                    recall_pd.add(pd_lc)
                    follow_set[pd].update(follow1(pd_lc, True))
                elif pd_lc in follow_set and not follow_set[pd_lc] and bypass:
                    continue
                else:
                    follow_set[pd].update(follow1(pd_lc))
                    if follow_set[pd_lc]:
                        follow_set[pd].update(follow1(pd_lc))
                if pd_lc in recall_pd or pd_lc in validate_pd:
                    if pd_lc in recall_pd and pd_lc in validate_pd:
                        continue
                    validate_pd.add(pd)
            elif ntnt_ls[pos + 1][0] == '<':
                pos += 1
                while ntnt_ls[pos][0] == '<':
                    follow_set[pd].update(first(ntnt_ls[pos]))
                    if null in follow_set[pd]:
                        follow_set[pd].remove(null)
                        if len(ntnt_ls) == pos + 1:
                            follow_set[pd].update(follow1(pd_lc))
                            break
                        pos += 1
                        continue
                    break
            else:
                follow_set[pd].add(ntnt_ls[pos + 1])
    return follow_set[pd]

def follow2(pd):
    if pd not in validate_pd:
        return
    validate_pd.remove(pd)
    for pd_lc, lc in pd_locations[pd].items():
        for x in range(0, len(lc), 2):
            rule = lc[x]
            pos = lc[x + 1]
            ntnt_ls = cfg_ds[pd_lc][rule]
            if len(ntnt_ls) == pos + 1:
                if pd_lc in validate_pd:
                    follow2(pd_lc)
                follow_set[pd].update(follow1(pd_lc))

def validate():
    validate_pd_ls = list(validate_pd)
    for pd in validate_pd_ls:
        follow2(pd)

def gen_follow_set():
    for pd in cfg_ds:
        follow1(pd)
        validate()

__all__ = [first_set, follow_set, gen_first_set, gen_follow_set, cfg_ds]