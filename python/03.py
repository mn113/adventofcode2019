def read_input():
    with open('../inputs/input03.txt') as fp:
        lines = fp.readlines()
        line1 = lines[0].split(',')
        line2 = lines[1].split(',')
        return (line1, line2)

compass = {'U': (0,1), 'D': (0,-1), 'L': (-1,0), 'R': (1,0)}

def track_wire(instructions):
    p = (0,0)
    points = {}
    moves = 0
    for i in instructions:
        direction = i[0]
        steps = int(i[1:])
        while steps:
            moves += 1
            p = (p[0] + compass[direction][0], p[1] + compass[direction][1])
            # add first one only (lowest steps wins)
            if p not in points:
                points[p] = moves
            steps -= 1
    return points

def sortManhattan(tup):
    if tup == 0:
        return False
    return abs(tup[0]) + abs(tup[1])

def part1():
    crosses.sort(key = sortManhattan)
    print(crosses[0])

def part2():
    cross_dists = [track1[c] + track2[c] for c in crosses]
    cross_dists.sort()
    print(cross_dists[0])

wires = read_input()
track1 = track_wire(wires[0])
track2 = track_wire(wires[1])
crosses = list(set(dict.keys(track1)) & set(dict.keys(track2)))

part1()
part2()
