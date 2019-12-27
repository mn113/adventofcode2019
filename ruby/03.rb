# The input represents 2 wires
# Each wire is a list of instructions e.g. U50 = up 50 from origin
@wires = File.open("../inputs/input03.txt", "r").each_line.map{|line| line.split(",")}

@compass = {'U' => [0,1], 'D' => [0,-1], 'L' => [-1,0], 'R' => [1,0]}

# Follow wire instructions, building up hash of all traversed points and their number of steps
def track_wire(instructions)
    pt = [0,0]
    points = {}
    moves = 0
    instructions.each do |str|
        direction = str[0]
        steps = str.slice(/\d+/).to_i
        while steps > 0 do
            moves += 1
            pt[0] += @compass[direction][0]
            pt[1] += @compass[direction][1]
            # add first crossing only (lowest steps wins)
            if !points.has_key? pt
                points[pt.dup] = moves
            end
            steps -= 1
        end
        # break if moves > 5000
    end
    points
end

# Return Manhattan dist of point from origin
def sortManhattan(point)
    return point[0].abs + point[1].abs
end

track1 = track_wire(@wires[0])
track2 = track_wire(@wires[1])

# Calculate all crossing points of wire 1 and wire 2
crosses = track1.keys & track2.keys

# part 1 - find the crossing nearest to the origin
p crosses.sort{|a,b| sortManhattan(a) - sortManhattan(b)}.first

# part 2 - find the cross with the smallest combined number of steps
p crosses.map{|x| track1[x] + track2[x] }.sort.first
