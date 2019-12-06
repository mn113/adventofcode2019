def read_input():
    with open('../inputs/input06b.txt') as fp:
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

    print("counted", steps)

def parent(val, graph):
    found = [p for p in graph if val in graph[p]]
    print('f', found, 'for', val)
    if len(found):
        return found[0]
    return None

def parent_chain(val, graph):
    initial = val
    chain = []
    while 1:
        val = parent(val, graph)
        if val == None:
            break;
        chain.append(val)
        if val == 'COM':
            break
    print(initial, chain, len(chain))

def part1():
    orbits = read_input()
    nodes = []
    graph = {}
    for o in orbits:
        key = o[0]
        val = o[1]
        nodes.append(val)
        if key not in graph:
            graph[key] = [val]
        else:
            graph[key].append(val)
    print(graph)

    tails = [n for n in nodes if n not in graph]
    print(tails)
    for t in tails:
        parent_chain(t, graph)

def part2():
    pass

part1()
part2()
