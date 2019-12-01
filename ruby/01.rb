$modules = File.open("../inputs/input01.txt", "r").each_line.map(&:to_i)

def calc_fuel(mass)
    mass / 3 - 2
end

def calc_fuel_recursive(mass, accum_fuel)
    fuel = calc_fuel(mass)
    if fuel > 0
        return calc_fuel_recursive(fuel, accum_fuel + fuel)
    else
        return accum_fuel
    end
end

def part1
    $modules.map{ |m| calc_fuel(m) }.reduce(:+)
end

def part2
    $modules.map{ |m| calc_fuel_recursive(m, 0) }.reduce(:+)
end

p 'Part 1:', part1
p 'Part 2:', part2
