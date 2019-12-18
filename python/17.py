import sys

def read_file():
    with open('../inputs/input17.txt') as fp:
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
    global igen

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
        #print(chr(p1))
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

class Robot:
    def __init__(self, grid, initial_coords):
        self.grid = grid
        self.x = initial_coords[0]
        self.y = initial_coords[1]
        self.lastmove = None
        self.moves = 0

    # Move 1 step in given direction
    def move(self, dir):
        vectors = { 'N': (0,-1), 'E': (1,0), 'S': (0,1), 'W': (-1,0) }
        self.x += vectors[dir][0]
        self.y += vectors[dir][1]
        self.lastmove = dir
        self.moves += 1
        print("at", (self.x, self.y))

    # Revert my last move
    def retreat(self):
        dirs = ['N','E','S','W']
        i = dirs.index(self.lastmove)
        j = (i + 2) % 4
        self.move(dirs[j])

    # Write a value at my coords
    def write(self, val):
        self.grid[self.y][self.x] = val

    # Get a value at my coords
    def read(self):
        return self.grid[self.y][self.x]

    # Look in 4 directions, return those without known walls
    def get_options(self):
        neighbs = {
            'W': self.grid[self.y][self.x - 1],
            'E': self.grid[self.y][self.x + 1],
            'S': self.grid[self.y + 1][self.x],
            'N': self.grid[self.y - 1][self.x]
        }
        unknown = [key for key in neighbs.keys() if neighbs[key] is None]
        empty = [key for key in neighbs.keys() if neighbs[key] in ['.','O']]
        if len(unknown) + len(empty) == 1:
            self.write('/') # represents dead end, don't return here
        return unknown + empty

    # Print grid
    def snapshot(self):
        display = ""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if y == self.y and x == self.x:
                    display += 'r'
                elif self.grid[y][x]:
                    display += self.grid[y][x]
                else:
                    display += " "
            display += "\n"
        print(display)

output_buffer = ""
def handle_output(val):
    global output_buffer
    output_buffer += chr(val)
    if val > 255:
        print(val, chr(val)) # part 2: 752491


# line lengths:
# A {L6,R12,L4,L6},     abcd
# B (R6,L6,R12),        efg
# B (R6,L6,R12),        hij
# C [L6,L10,L10,R6],    klmn
# A {L6,R12,L4,L6},     opqr
# B (R6,L6,R12),        stu
# C [L6,L10,L10,R6],    vwxy
# A {L6,R12,L4,L6},     zabc
# B (R6,L6,R12),        def
# C [L6,L10,L10,R6]     ghij


def gen_input():
    # compose ASCII input
    main_routine = [c for c in 'A,B,B,C,A,B,C,A,B,C' + chr(10)]
    a_routine = [c for c in 'L,6,R,12,L,4,L,6' + chr(10)]
    b_routine = [c for c in 'R,6,L,6,R,12' + chr(10)]
    c_routine = [c for c in 'L,6,L,10,L,10,R,6' + chr(10)]
    video_on = [c for c in 'y' + chr(10)]
    video_off = [c for c in 'n' + chr(10)]

    codes = main_routine + a_routine + b_routine + c_routine + video_off

    for c in codes:
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
mem += [0] * 100000
rbase = 0

grid = [[None] * 60 for _ in range(60)]
robot = Robot(grid, (30,30))

crosses = [(6,10), (30,10), (34,10), (10,12), (28,12), (12,16), (28,16), (34,16), (16,18), (26,20), (22,22), (16,26), (20,26), (18,36), (22,38)]
print(sum([p[0] * p[1] for p in crosses])) # part1: 6052

run_program()
print(output_buffer)
