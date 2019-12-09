def read_input():
    with open('../inputs/input06.txt') as fp:
        lines = fp.readlines()
        return [line.strip().split(")") for line in lines]

def count_traversal(graph):
    dists = { 'COM': 0 }
    to_visit = ['COM']
    while len(to_visit):
        current, to_visit = to_visit[0], to_visit[1:]
        print(current)
        for nxt in graph[current]:
            if nxt in graph:
                to_visit.append(nxt)
            else:
                dists[nxt] = dist

def parent(val, graph):
    found = [p for p in graph if val in graph[p]]
    if len(found):
        return found[0]
    return None

def parent_chain(val, graph):
    global total_orbits
    global you_chain
    global san_chain

    initial = val
    chain = []
    while 1:
        val = parent(val, graph)
        if val == None:
            break;
        chain.append(val)
        if val == 'COM':
            break

    if initial == 'YOU':
        you_chain = chain
    elif initial == 'SAN':
        san_chain = chain

    total_orbits += len(chain)

def part1():
    global total_orbits
    orbits = read_input()
    nodes = set()
    graph = {}
    for o in orbits:
        key = o[0]
        val = o[1]
        nodes.add(val)
        if key not in graph:
            graph[key] = [val]
        else:
            graph[key].append(val)

    for t in nodes:
        parent_chain(t, graph)

    print("total orbits", total_orbits)

def part2():
    global you_chain
    global san_chain
    i = 0
    while 1:
        n = you_chain[i]
        if n in san_chain:
            print(n, i, san_chain.index(n))
            break
        i += 1

total_orbits = 0

part1()
part2()
