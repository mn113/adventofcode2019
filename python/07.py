import itertools
import time
import threading
import concurrent.futures


def read_input():
    with open('../inputs/input07.txt') as fp:
        lines = fp.readlines()[0].split(',')
        lines = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(',')
        return [int(n) for n in lines]

amp_states = {
    0: 'AMP_STOPPED',
    1: 'AMP_RUNNING',
    2: 'AMP_PAUSED_FOR_INPUT',
    3: 'AMP_HALTED'
}

class Amp:
    def __init__(self, id, phase):
        self.id = id
        self.phase = phase
        self.mem = read_input()
        self.ptr = 0
        self.state = 0

    def __str__(self):
        global amp_states
        return f"Amp id {self.id}, phase {self.phase}, ptr {self.ptr}, {amp_states[self.state]}\n"

    def get_input(self):
        global inputs
        self.state = 2
        #print(f"{self.id} awaits input")
        while inputs[self.id] == None:
            time.sleep(.01)
        val = inputs[self.id]
        inputs[self.id] = None
        print(f"{self.id} got input: {val}")
        self.state = 1
        return val

    def run_program(self):
        print("Amp", self.id, "started to run")
        self.state = 1
        def run_instruction(i, modes, opcode):
            def get_param(mode, j):
                if mode == '0':
                    # address mode - values refer to mem addresses
                    return self.mem[self.mem[j]]
                elif mode == '1':
                    # immediate mode - values used directly
                    return self.mem[j]
                return False

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

            print(opcode, i, self.mem[i:i+4], modes)

            if opcode == '01':
                # Add
                self.mem[self.mem[i+3]] = p1 + p2
                return i + 4

            elif opcode == '02':
                # Multiply
                self.mem[self.mem[i+3]] = p1 * p2
                return i + 4

            elif opcode == '03':
                # Take input
                if type(self.phase) is int:
                    self.mem[self.mem[i+1]] = self.phase
                    self.phase = None
                else:
                    self.mem[self.mem[i+1]] = self.get_input()
                return i + 2

            elif opcode == '04':
                # Return output
                handle_output(self.id, p1)
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
                    self.mem[self.mem[i+3]] = 1
                else:
                    self.mem[self.mem[i+3]] = 0
                return i + 4

            elif opcode == '08':
                # Equals
                if p1 == p2:
                    self.mem[self.mem[i+3]] = 1
                else:
                    self.mem[self.mem[i+3]] = 0
                return i + 4

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

inputs = []
outputs = []

def reset_io():
    global inputs
    global outputs
    inputs = [0] + [None] * 4
    outputs = [None] * 5

best_signal = 0
best_perm = None

def handle_output(id, val):
    global best_signal
    global best_perm
    print("got output on id", id, "=>", val)
    outputs[id] = val
    if id == 4 and outputs[4] > best_signal:
        best_signal = outputs[4]
        best_perm = perm
        print("new best signal:", best_signal, best_perm)
    # queue next input
    inputs[(id + 1) % 5] = val


def part1():
    global best_signal
    global best_perm
    global outputs
    perms = list(itertools.permutations([0,1,2,3,4]))
    for perm in perms:
        print(perm)
        amps = [Amp(id, phase) for id, phase in enumerate(list(perm))]
        reset_io()
        print(amps[0], amps[1])

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for i in range(5):
                executor.submit(amps[i].run_program)
        print("signal:", outputs[4])

    print("perm:", best_perm, "sig:", best_signal)
    print("=====")


def part2():
    #perms = list(itertools.permutations(range(5,10)))
    perm = (9,8,7,6,5)
    amps = [Amp(phase) for phase in list(perm)]
    n = 0
    inp = 0
    while 1:
        inp = amp(inp, perm[n % 5])
        perm[n % 5] = False # unset phase after initial usage
        n += 1
        if (n == 30):
            break
    print("signal:", inp, "n:", n)

    # current_index = 0
    # signal = 0
    # while 1:
    #     signal = amps[current_index].run_program(signal)
    #     current_index += 1

# part1()
reset_io()
amp0 = Amp(0, 1)
amp0.run_program()