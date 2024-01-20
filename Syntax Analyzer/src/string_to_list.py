def string_to_list(string):
    stringList = []

    token = ''
    i = 0
    if string[i] == ',':
        stringList.append(string[i])
        i += 1
    while i < len(string):
        if string[i] == ' ':
            i += 1
            if string[i] == ',':
                stringList.append(string[i])
                i += 1
        elif string[i] == ',':
            if token:
                stringList.append(token)
            i += 1
            token = ''
        else:
            token += string[i]
            i += 1

    if token:
        stringList.append(token)
    return stringList