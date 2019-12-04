def is_increasing(n):
    s = str(n)
    return s[1] >= s[0] and s[2] >= s[1] and s[3] >= s[2] and s[4] >= s[3] and s[5] >= s[4]

def has_double(n):
    s = str(n)
    return s[1] == s[0] or s[2] == s[1] or s[3] == s[2] or s[4] == s[3] or s[5] == s[4]

def has_isolated_double(n):
    s = str(n)
    return (s[0] == s[1] and s[1] != s[2]) \
        or (s[1] == s[2] and s[0] != s[1] and s[2] != s[3]) \
        or (s[2] == s[3] and s[1] != s[2] and s[3] != s[4]) \
        or (s[3] == s[4] and s[2] != s[3] and s[4] != s[5]) \
        or (s[4] == s[5] and s[3] != s[4])

def is_valid(n):
    return is_increasing(n) and has_double(n)

def is_strictly_valid(n):
    return is_increasing(n) and has_isolated_double(n)

def part1():
    valid = [c for c in range(start, end) if is_valid(c)]
    print(len(valid))

def part2():
    valid = [c for c in range(start, end) if is_strictly_valid(c)]
    print(len(valid))

start = 134792
end = 675810
part1()
part2()
