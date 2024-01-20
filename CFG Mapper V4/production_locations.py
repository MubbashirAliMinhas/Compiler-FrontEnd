import re
from reconstruct_cfg import non_terminal

def production_locations(cfg_ds):
    pd_locations = {}

    for pd, rule in cfg_ds.items():
        for x in range(len(rule)):
            for y in range(len(rule[x])):
                if re.match(non_terminal, rule[x][y]):
                    nt = rule[x][y]
                    if nt not in pd_locations:
                        pd_locations[nt] = {}
                    if pd not in pd_locations[nt]:
                        pd_locations[nt][pd] = []
                    pd_locations[nt][pd].extend([x, y])
    return pd_locations