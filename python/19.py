import sys

def read_input():
    with open('../inputs/input19.txt') as fp:
        numbers = fp.readlines()[0].split(',')
        return [int(n) for n in numbers]

droid_states = {
    0: 'STOPPED',
    1: 'RUNNING',
    2: 'PAUSED_FOR_INPUT',
    3: 'HALTED'
}

class Droid:
    def __init__(self, x, y):
        self.id = str(x) + '_' + str(y)
        self.x = x
        self.y = y
        self.got_x = False
        self.phase = None
        self.mem = read_input()
        self.mem += [0] * 100000
        self.rbase = 0
        self.ptr = 0
        self.state = 0

    def __str__(self):
        global droid_states
        return f"Droid id {self.id}, phase {self.phase}, ptr {self.ptr}, {droid_states[self.state]}\n"

    def put_output(self, val):
        print("Droid", self.id, "output", val)
        handle_output(self.id, val, self.x, self.y)

    def get_input(self):
        if not self.got_x:
            self.got_x = True
            return self.x
        return self.y

    def run_program(self):
        global igen
        print("Droid", self.id, "started to run")
        self.state = 1
        def run_instruction(i, modes, opcode):
            def getMem(ptr, mode):
                if mode == '0':
                    return self.mem[self.mem[ptr]]
                elif mode == '1':
                    return self.mem[ptr]
                elif mode == '2':
                    return self.mem[self.mem[ptr] + self.rbase]
                else:
                    raise TypeError("Bad mode: " + mode)

            def setMem(ptr, mode, val):
                if mode == '0':
                    self.mem[self.mem[ptr]] = val
                elif mode == '2':
                    self.mem[self.mem[ptr] + self.rbase] = val
                else:
                    raise TypeError("Bad mode: " + mode)

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

            # print(opcode, i, self.mem[i:i+4], modes)

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
                inp = self.get_input()
                setMem(i+1, modes[0], inp)
                return i + 2

            elif opcode == '04':
                # Print output
                self.put_output(p1)
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
                self.rbase += p1
                return i + 2

        while 1:
            if self.mem[self.ptr] == 99:
                print("HALT")
                self.state = 3
                return None
            operator = str(self.mem[self.ptr])
            param_modes, opcode = operator[:-2], operator[-2:]
            if not param_modes:
                param_modes = '000'
            self.ptr = run_instruction(self.ptr, param_modes[::-1], opcode)
            if self.ptr is None:
                return None
            if type(self.ptr) is not int:
                if len(self.ptr) > 1:
                    return self.ptr[1]

space = [[0] * 1500 for _ in range(1500)]

def handle_output(id, val, x, y):
    global space
    space[y][x] = val

def display(miny = 0, maxy = 50, minx = 0, maxx = 50):
    print("\n".join(["".join([str(n) for n in row[minx:maxx]]) for row in space[miny:maxy+1] if len(set(row)) > 1]))

# Part 1:
for y in range(50):
    for x in range(50):
        droid = Droid(x,y)
        droid.run_program()
display()

# Part 2:
# Linear search revealed approx location of 100x100:
x, y = 840, 1085
for y in range(y-3,y+1):
    for x in range(x-3, x+1):
        d1 = Droid(x,y+99)
        d2 = Droid(x+99,y)
        d1.run_program()
        d2.run_program()
        print("=====")

# Droid 838_1181 output 1
# Droid 937_1082 output 1