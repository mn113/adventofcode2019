import numpy

def read_input():
    with open('../inputs/input09.txt') as fp:
        lines = fp.readlines()[0].split(',')
        #lines = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(',')
        return [int(n) for n in lines]

def run_program():
    global mem
    global inp
    rbase = 0
    i = 0
    while 1:
        if mem[i] == 99:
            print("HALT")
            break
        operator = str(mem[i])
        param_modes, opcode = operator[:-2], operator[-2:]
        if not param_modes:
            param_modes = '000'
        i = run_instruction(i, param_modes[::-1], opcode, rbase)

def run_instruction(i, modes, opcode, rbase):
    global mem
    global inp

    mode1 = modes[0]
    if len(modes) > 1:
        mode2 = modes[1]
    else:
        mode2 = '0'
    if len(modes) > 2:
        mode3 = modes[2]
    else:
        mode3 = '0'

    if len(opcode) == 1:
        opcode = '0' + opcode

    if opcode in ['01', '02', '04', '05', '06', '07', '08', '09']:
        p1 = get_param(mode1, i+1, rbase)

    if opcode in ['01', '02', '05', '06', '07', '08']:
        p2 = get_param(mode2, i+2, rbase)

    j = i

    if opcode == '01':
        # Add
        if mode3 == '2':
            j = i + rbase
        mem[mem[j+3]] = p1 + p2
        return i + 4

    elif opcode == '02':
        # Multiply
        if mode3 == '2':
            j = i + rbase
        mem[mem[j+3]] = p1 * p2
        return i + 4

    elif opcode == '03':
        # Take input
        if mode1 == '2':
            j = i + rbase
        mem[mem[j+1]] = inp
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
        if mode3 == '2':
            j = i + rbase
        if p1 < p2:
            mem[mem[j+3]] = 1
        else:
            mem[mem[j+3]] = 0
        return i + 4

    elif opcode == '08':
        # Equals
        if mode3 == '2':
            j = i + rbase
        if p1 == p2:
            mem[mem[j+3]] = 1
        else:
            mem[mem[j+3]] = 0
        return i + 4

    elif opcode == '09':
        # Adjust rbase
        rbase += p1
        return i + 2

def get_param(mode, j, rbase):
    global mem
    if mode == '0':
        # address mode - values refer to mem addresses
        return mem[mem[j]]
    elif mode == '1':
        # immediate mode - values used directly
        return mem[j]
    elif mode == '2':
        # relative mode - value + rbase
        return mem[mem[j]] + rbase
    return False

mem = read_input()
mem += [0] * 100000
inp = 1
run_program()
