def read_file():
    with open('../inputs/input11.txt') as fp:
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
        setMem(i+1, modes[0], get_input())
        return i + 2

    elif opcode == '04':
        # Print output
        print("-->", p1, "<---")
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


class Ship:
    def __init__(self, size):
        # Ship grid setup
        # 2D grid, top left is (0,0)
        self.grid = [[0] * size for _ in range(size)] # don't do bug of accidental list copies!
        self.width = size
        self.height = size


class Robot:
    compass = ['N', 'E', 'S', 'W']
    vectors = { 'N': (0,-1), 'E': (1,0), 'S': (0,1), 'W': (-1,0) }

    @classmethod
    def get_compass(cls):
        return cls.compass

    @classmethod
    def get_vectors(cls):
        return cls.vectors

    def __init__(self, initial_coords, initial_dir, surface):
        self.x = initial_coords[0]
        self.y = initial_coords[1]
        self.dir = initial_dir
        self.surface = surface
        self.paint_mode = True

    def toggle_mode(self):
        self.paint_mode = not self.paint_mode

    # Set a value at my coords
    def paint(self, val):
        self.surface.grid[self.y][self.x] = val

    # Get a value at my coords
    def read_color(self):
        return self.surface.grid[self.y][self.x]

    # Set a new direction
    def turn(self, way):
        compass_index = self.get_compass().index(self.dir)
        if way == 1:
            compass_index += 1
        else:
            compass_index -= 1
        self.dir = self.get_compass()[compass_index % 4]

    # Move 1 step in my direction
    def move(self):
        vects = self.get_vectors()
        self.x += vects[self.dir][0]
        self.y += vects[self.dir][1]
        print("at", (self.x, self.y))


def handle_output(val):
    if robot.paint_mode:
        print("Painting", colors[val])
        robot.paint(val)
        painted.add((robot.x, robot.y))
    else:
        print("Turning", turns[val])
        robot.turn(val)
        print("Moving", robot.dir)
        robot.move()
    robot.toggle_mode()

def get_input():
    current_color = robot.read_color()
    print("Robot is on color", colors[current_color])
    return current_color

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

ship = Ship(100)
robot = Robot((50,50), 'N', ship)

# part 2: start on whyte panel
# ship.grid[50][50] = 1

painted = set()
colors = ["bleck", "whyte"]
turns = ["left", "right"]
mem = read_file()
mem += [0] * 100000
rbase = 0

run_program()

output = ""
for y in range(len(ship.grid)):
    for x in range(len(ship.grid[y])):
        if ship.grid[y][x] == 1:
            output += "#"
        else:
            output += "."
    output += "\n"

print(output)
print(len(painted)) # 1709 correct for part 1
