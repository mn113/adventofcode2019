@tiles = "##.#.
##.#.
##.##
.####
.#...".each_line.map(&:chomp).map(&:chars)

def neighbs(current)
    x = current[0]
    y = current[1]
    up    = [x - 1, y]
    down  = [x + 1, y]
    left  = [x, y - 1]
    right = [x, y + 1]

    neighbs = [up, down, left, right]
        .reject{|p| p[0] < 0 || p[0] > 4 || p[1] < 0 || p[1] > 4}
end

def tick
    newtiles = Marshal.load(Marshal.dump(@tiles)) # deep copy by values
    @tiles.each_with_index do |row,y|
        row.each_with_index do |char,x|
            bug_nbs = neighbs([x,y]).map{ |point| @tiles[point[1]][point[0]] }.count('#')
            if char == '#' && bug_nbs != 1
                newtiles[y][x] = '.'
            elsif char == '.' && (bug_nbs == 1 || bug_nbs == 2)
                newtiles[y][x] = '#'
            else
                newtiles[y][x] = char
            end
        end
    end
    @tiles = newtiles
end

def render(tiles)
    printf tiles.map{|row| row.join}.join("\n") + "\n\n"
end

def biodiversity(tiles)
    mul = 1
    tot = 0
    tiles.flatten.each do |t|
        tot += mul if t == '#'
        mul = mul << 1
    end
    tot
end

render @tiles
all_states = [biodiversity(@tiles)]
while true do
    tick()
    current = @tiles.to_s
    all_states.push(current)
    if all_states.count(current) == 2
        render @tiles
        p biodiversity(@tiles)
        break
    end
end
