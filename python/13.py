import sys
import time

def read_file():
    with open('../inputs/input13.txt') as fp:
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

prog_output = []
player_score = 0

snapshots = []

def snapshot():
    global player_score
    block_count = 0
    display = ""
    for y in range(len(screen)):
        for x in range(len(screen[y])):
            if screen[y][x] > 0:
                display += str(screen[y][x])
            else:
                display += " "
            if screen[y][x] == 2:
                block_count += 1
        display += "\n"

    #print(display)
    #print([block_count, player_score])
    snapshots.append(display)

def handle_output(val):
    global prog_output
    prog_output.append(val)
    if len(prog_output) == 3:
        draw()
        prog_output = []

def draw():
    global prog_output
    global screen
    global player_score
    x = prog_output[0]
    y = prog_output[1]
    val = prog_output[2]
    if x == -1 and y == 0:
        player_score = val
    else:
        screen[y][x] = val

def get_input():
    snapshot()
    print("in?")
    # Compare ball (4) position with paddle (3). Try to intercept by returning joystick values
    paddle = 3
    ball = 4
    paddle_y = 22
    paddle_x = screen[paddle_y].index(paddle)
    ball_y = [y for y in range(len(screen)) if ball in screen[y]][0]
    ball_x = screen[ball_y].index(ball)
    print([(paddle_x, paddle_y), (ball_x, ball_y)])

    if ball_y > paddle_y:
        sys.exit("GAME OVER!")
    if paddle_x < ball_x:
        print('joy 1')
        return 1 # move right
    elif paddle_x > ball_x:
        print('joy -1')
        return -1 # move left
    else:
        print('joy 0')
        return 0

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

screen = [[0] * 50 for _ in range(25)]

mem[0] = 2
run_program()

snapshot()

def animate():
    for frame in snapshots:
        print(frame)
        time.sleep(0.01)

animate()