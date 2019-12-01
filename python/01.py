from math import floor

def read_input():
    with open('../inputs/input01.txt') as fp:
        lines = fp.readlines()
        return [int(line) for line in lines]

def calc_fuel(mass):
    return floor(mass / 3) - 2

def calc_fuel_recursive(mass, accum_fuel):
    fuel = calc_fuel(mass)
    if fuel > 0:
        return calc_fuel_recursive(fuel, accum_fuel + fuel)
    else:
        return accum_fuel

def part1():
    ans = sum([calc_fuel(m) for m in modules])
    print(ans)

def part2():
    ans = sum([calc_fuel_recursive(m, 0) for m in modules])
    print(ans)

modules = read_input()

part1() # 3347838
part2() # 5018888