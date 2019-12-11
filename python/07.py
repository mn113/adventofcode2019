import itertools

def read_input():
    with open('../inputs/input07.txt') as fp:
        lines = fp.readlines()[0].split(',')
        # lines = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(',')
        return [int(n) for n in lines]

class Amp:
    def __init__(self, phase):
        self.phase = phase
        self.mem = read_input()
        self.ptr = 0

    def run_program(self, inp):
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
                if self.phase:
                    self.mem[self.mem[i+1]] = self.phase
                else:
                    self.mem[self.mem[i+1]] = inp
                return i + 2

            elif opcode == '04':
                # Return output
                return [True, p1]

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

def part1():
    perms = list(itertools.permutations([0,1,2,3,4]))
    best_signal = 0
    best_perm = None
    for perm in perms:
        amps = [Amp(phase) for phase in list(perm)]
        signal = (
            amps[4].run_program(
                amps[3].run_program(
                    amps[2].run_program(
                        amps[1].run_program(
                            amps[0].run_program(0)
                        )
                    )
                )
            )
        )
        if signal > best_signal:
            best_signal = signal
            best_perm = perm
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

part1()