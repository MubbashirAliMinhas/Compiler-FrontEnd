from first_follow import first_set, follow_set, gen_first_set, gen_follow_set, cfg_ds
from reconstruct_cfg import null, print_dict

gen_first_set()
gen_follow_set()

selection_locations_temp = {}
for key, value in cfg_ds.items():
    lc = []
    for x in range(len(value)):
        if value[x][0][0] == '<' or value[x][0] == null:
            lc.append(x)
    selection_locations_temp[key] = lc

selection_locations = {}
for key, value in selection_locations_temp.items():
    if value:
        selection_locations[key] = value
selection_locations_temp.clear()

def gen_selection_set():
    selection_set = {}
    for key, value in selection_locations.items():
        key_p = key.strip('<>')
        selection_set[key_p] = []
        for lc in value:
            sel_set = set()
            sel_set.update(first_set[key][lc])
            if null in sel_set:
                sel_set.remove(null)
                sel_set.update(follow_set[key])
            sel_set = list(sel_set)
            selection_set[key_p].append(sel_set)
    return selection_set

__all__ = [gen_selection_set]