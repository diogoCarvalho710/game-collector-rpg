listaNum = [4, 3, 2, 10]
print(max(listaNum), max(listaNum) + 1, len(listaNum))

listIds = []


def idGenerator():
    if len(listIds) == 0:
        id = 1
    else:
        id = max(listIds) + 1
    listIds.append(id)
    return id
