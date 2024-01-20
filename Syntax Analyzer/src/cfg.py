from string_to_list import string_to_list

def selection():
    selection_set = {}

    with open('selection_set.txt', 'r') as file:
        while True:
            line = file.readline()
            if line == '':
                break
            line = line.strip()
            line = line.split('#')
            non_terminal = line[0]
            for x in range(len(line) - 1):
                line[x] = string_to_list(line[x + 1])
            line.pop()
            selection_set[non_terminal] = line

    return selection_set

selection_set = selection()

for key, value in selection_set.items():
    print(key, value)