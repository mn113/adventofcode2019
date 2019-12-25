import sys
import itertools

def read_file():
    with open('../inputs/input25.txt') as fp:
        numbers = fp.readlines()[0].split(',')
        return [int(n) for n in numbers]

def getMem(ptr, mode):
    global mem
    global rbase

    if mode == '0':
        return mem[mem[ptr]]
    elif mode == '1':
        return mem[ptr]
    elif mode == '2':
        return mem[mem[ptr] + rbase]
    else:
        raise TypeError("Bad mode: " + mode)

def setMem(ptr, mode, val):
    global mem
    global rbase

    if mode == '0':
        mem[mem[ptr]] = val
    elif mode == '2':
        mem[mem[ptr] + rbase] = val
    else:
        raise TypeError("Bad mode: " + mode)

def run_instruction(i, modes, opcode):
    global mem
    global rbase

    # Fill in modes:
    while len(modes) < 3:
        modes += '0'

    # Zerofill:
    if len(opcode) == 1:
        opcode = '0' + opcode

    # Getting from memory:
    if opcode in ['01', '02', '04', '05', '06', '07', '08', '09']:
        p1 = getMem(i+1, modes[0])

    if opcode in ['01', '02', '05', '06', '07', '08']:
        p2 = getMem(i+2, modes[1])

    # Setting to memory:
    if opcode == '01':
        # Add
        setMem(i+3, modes[2], p1 + p2)
        return i + 4

    elif opcode == '02':
        # Multiply
        setMem(i+3, modes[2], p1 * p2)
        return i + 4

    elif opcode == '03':
        # Take input
        setMem(i+1, modes[0], next(igen))
        return i + 2

    elif opcode == '04':
        # Print output
        handle_output(p1)
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
            setMem(i+3, modes[2], 1)
        else:
            setMem(i+3, modes[2], 0)
        return i + 4

    elif opcode == '08':
        # Equals
        if p1 == p2:
            setMem(i+3, modes[2], 1)
        else:
            setMem(i+3, modes[2], 0)
        return i + 4

    elif opcode == '09':
        # Adjust rbase
        rbase += p1
        return i + 2

output_buffer = []

def handle_output(val):
    global output_buffer
    output_buffer.append(val)
    if chr(val) == '?':
        print("".join([chr(c) for c in output_buffer]))
        output_buffer = []

def gen_input():
    cmds = [
        # Hull Breach
        # 'north\n',  # Corridor
        # 'south\n',  # Hull Breach [n,E]
        'east\n',   # Engineering [E,w]
        'east\n'    # Warp Drive Maintenance [N,E,w]
        'take semiconductor\n',

        'north\n',  # Gift Wrapping [N,s,W]
        'take planetoid\n',
        'north\n',  # Stables [s,W]
        'take antenna\n',
        # 'west\n'    # Navigation [e]
        # 'east\n',
        'south\n',  # Gift Wrapping [n,s,W]
        'west\n',   # Hot Chocolate [N,e,W]
        'take food ration\n',
        'north\n',  # Sick Bay [N,E,s]
        'take space law space brochure\n',

        'north\n',  # Storage [N,s]
        'north\n',  # Kitchen [s]
        'take weather machine\n',
        'south\n',  # Storage [n,s]
        'south\n',  # Sick Bay [n,E,s]

        'east\n',   # Crew Quarters [w]
        'take jam\n',
        'west\n',   # Sick Bay [n,e,s]

        'south\n'   # Hot Chocolate [n,e,W]

        'west\n',   # Observatory [e,W]
        'west\n',   # Arcade [e]
        'take monolith\n',
        'east\n',   # Observatory [e,w]
        'east\n',   # Hot Chocolate [n,e,w]

        'east\n',
        'south\n',
        'east\n',   # Hallway [N,S,w]
        # 'north\n',  # Science Lab [s]
        # 'south\n',
        'south\n'   # Holodeck [n,S]
        'south\n',  # Passages [n,E]
        'east\n',    # Security Checkpoint [E,w]

        'drop space law space brochure\n', # too light on its own, too heavy with any other
        'drop jam\n', # too light on its own, too heavy with food ration
        'drop planetoid\n',
        'drop weather machine\n',
        # keep'food ration\n', # too light
        # keep'antenna\n', # too light
        # keep'monolith\n',
        # keep'semiconductor\n',

        'inv\n',
        'east\n'
    ]
    for c in "".join(cmds):
        yield ord(c)

igen = gen_input()

def run_program():
    global mem
    ptr = 0
    while 1:
        if mem[ptr] == 99:
            print("HALT")
            break
        operator = str(mem[ptr])
        param_modes, opcode = operator[:-2], operator[-2:]
        if not param_modes:
            param_modes = '000'
        ptr = run_instruction(ptr, param_modes[::-1], opcode)

mem = read_file()
mem += [0] * 10000000
rbase = 0

run_program()
