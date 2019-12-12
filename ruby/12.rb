input = File.open("../inputs/input12.txt", "r")
@moons = input.each_line.map do |line|
    /x=(?<px>-?\d+), y=(?<py>-?\d+), z=(?<pz>-?\d+)/ =~ line.chomp

    {:p => [px,py,pz].map(&:to_i),
     :v => [0,0,0]}
end

p "#{@moons.size} moons loaded"

@origmoons = Marshal.load(Marshal.dump(@moons))

def step_moons
    # Treat moons pairwise:
	@moons.combination(2).to_a.each do |m1, m2|
        # Apply gravity to set velocities based on relative positions in 3D:
        [0,1,2].each do |c|
            m1[:v][c] += m2[:p][c] <=> m1[:p][c]
            m2[:v][c] -= m2[:p][c] <=> m1[:p][c]
        end
    end
    @moons.each do |moon|
        # Adjust position of moon based on new velocity:
        [0,1,2].each do |c|
            moon[:p][c] += moon[:v][c]
        end
    end
end


# Part 1: total energy
t = 0
until t == 1000 do
    step_moons
    t += 1
end

pe = @moons.map{ |m| m[:p].map{ |c| c.abs }.reduce(&:+) }
ke = @moons.map{ |m| m[:v].map{ |c| c.abs }.reduce(&:+) }
p 'Energy: ' + pe.zip(ke).map{ |p| p.reduce(&:*) }.reduce(&:+).to_s


# Part 2: find repeated state
@moons = Marshal.load(Marshal.dump(@origmoons))
t = 0
# Find period of each axis:
periods = {}
while periods.size < 3 do
    step_moons
    t += 1

    [0,1,2].each do |c| # x,y,z
        # All moons' x-positions and x-velocities should match original state
        if @moons[0][:p][c] == @origmoons[0][:p][c] \
        && @moons[1][:p][c] == @origmoons[1][:p][c] \
        && @moons[2][:p][c] == @origmoons[2][:p][c] \
        && @moons[3][:p][c] == @origmoons[3][:p][c] \
        && @moons[0][:v][c] == @origmoons[0][:v][c] \
        && @moons[1][:v][c] == @origmoons[1][:v][c] \
        && @moons[2][:v][c] == @origmoons[2][:v][c] \
        && @moons[3][:v][c] == @origmoons[3][:v][c]
            p ["period of axis", c, "is", t]
            periods[c] = t
            break
        end
    end
end
p [periods]
# {2=>116328, 0=>167624, 1=>231614}
#p 167624.lcm(231614).lcm(116328) # 282270365571288
p periods.values.reduce(&:lcm)
