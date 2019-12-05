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
            print("HALT")
            break
        operator = str(mem[i])
        param_modes, opcode = operator[:-2], operator[-2:]
        if not param_modes:
            param_modes = '000'
        i = run_instruction(i, param_modes[::-1], opcode)

def run_instruction(i, modes, opcode):
    global mem
    global inp

    mode1 = modes[0]
    if len(modes) > 1:
        mode2 = modes[1]
    else:
        mode2 = '0'

    # LHS cannot depend on mode - always refers to mem address
    if len(opcode) == 1:
        opcode = '0' + opcode

    if opcode in ['01', '02', '04', '05', '06', '07', '08']:
        p1 = get_param(mode1, i+1)

    if opcode in ['01', '02', '05', '06', '07', '08']:
        p2 = get_param(mode2, i+2)

    if opcode == '01':
        # Add
        mem[mem[i+3]] = p1 + p2
        return i + 4

    elif opcode == '02':
        # Multiply
        mem[mem[i+3]] = p1 * p2
        return i + 4

    elif opcode == '03':
        # Take input
        mem[mem[i+1]] = inp
        return i + 2

    elif opcode == '04':
        # Print output
        print("-->", p1, "<---")
        return i + 2

    elif opcode == '05':
        # Jump if non-zero
        if p1 != 0:
            return p2
        return i + 3

    elif opcode == '06':
        # Jump if zero
        if p1 == 0:
            return p2
        return i + 3

    elif opcode == '07':
        # Less than
        if p1 < p2:
            mem[mem[i+3]] = 1
        else:
            mem[mem[i+3]] = 0
        return i + 4

    elif opcode == '08':
        # Equals
        if p1 == p2:
            mem[mem[i+3]] = 1
        else:
            mem[mem[i+3]] = 0
        return i + 4

def get_param(mode, j):
    global mem
    if mode == '0':
        # address mode - values refer to mem addresses
        return mem[mem[j]]
    elif mode == '1':
        # immediate mode - values used directly
        return mem[j]
    return False

mem = read_input()
inp = 5
run_program()
# 16489636
# 9386583
