def read_input():
    with open('../inputs/input05.txt') as fp:
        lines = fp.readlines()[0].split(',')
        return [int(n) for n in lines]

def run_program():
    global mem
    global inp
    i = 0
    while 1:
        if mem[i] == 99:
            break
        operator = str(mem[i])
        param_modes, opcode = operator[:-2], operator[-2:]
        #print(i, mem[i], "\n-", param_modes, "\n--", opcode)
        i = run_instruction(i, param_modes[::-1], opcode)

def run_instruction(i, param_modes, opcode):
    global mem
    global inp

    print(i, mem[i:i+4])

    # LHS cannot depend on mode - always refers to mem address
    if len(opcode) == 1:
        opcode = '0' + opcode

    # address mode - values refer to mem addresses
    p1 = mem[mem[i+1]]
    if opcode == '01' or opcode == '02':
        p2 = mem[mem[i+2]]

    # immediate mode - values used directly
    if len(param_modes) > 0 and param_modes[0] == '1':
        p1 = mem[i+1]
    if len(param_modes) > 1 and param_modes[1] == '1' and opcode == '01' or opcode == '02':
        p2 = mem[i+2]

    if (opcode == '01'):
        mem[mem[i+3]] = p1 + p2
        return i + 4
    elif (opcode == '02'):
        mem[mem[i+3]] = p1 * p2
        return i + 4
    elif (opcode == '03'):
        mem[mem[i+1]] = inp
        return i + 2
    elif (opcode == '04'):
        print("-->", p1, "<---")
        return i + 2

def part1():
    run_program()
    print(mem)

def part2():
    pass

mem = read_input()
inp = 1
part1()
part2()
