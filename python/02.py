def read_input():
    with open('../inputs/input02.txt') as fp:
        lines = fp.readlines()[0].split(',')
        return [int(n) for n in lines]


def run_program(mem):
    i = 0
    while 1:
        if mem[i] == 99:
            break
        operator = mem[i]
        if (operator == 1):
            mem[mem[i+3]] = mem[mem[i+1]] + mem[mem[i+2]]
        elif (operator == 2):
            mem[mem[i+3]] = mem[mem[i+1]] * mem[mem[i+2]]
        i += 4
    return mem[0]


def solve_input(noun, verb):
    mem = read_input()
    mem[1] = noun
    mem[2] = verb
    return run_program(mem)


def part1():
    mem = read_input()
    ans = run_program(mem)
    print(ans)


def part2():
    goal = 19690720
    for n in range(140):
        for v in range(140):
            ans = solve_input(n,v)
            if (ans == goal):
                print(ans,n,v)
                return True
    return False


part1() # 5866714
part2() # 5208
