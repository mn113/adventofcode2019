$data = File.open("../inputs/input10.txt", "r").each_line.map(&:chars)

# $data = ".#..#..###
# ####.###.#
# ....###.#.
# ..###.##.#
# ##.##.#.#.
# ....###..#
# ..#.#..#.#
# #..#.#.###
# .##...##.#
# .....#.#..".each_line.map(&:chars)

$height = $data.length
$width = $data[0].length

p [$height, $width]

asteroids = []
(0...$height).each do |y|
    (0...$width).each do |x|
        if $data[y][x] == '#'
            asteroids.push({ x: x, y: y, c: Complex(x,y), sees: []})
        end
    end
end

p asteroids.length #348

asteroids.each do |a|
    asteroids.each do |b|
        next if a[:x] == b[:x] && a[:y] == b[:y]
        diff = (b[:c] - a[:c])
        a[:sees].push(diff)
    end
end

#p asteroids.map{ |a| a[:sees].uniq.size }.max

#p asteroids.select{ |a| a[:sees].uniq.size == 292 } # [20, 20]

origin =  asteroids.select{ |a| a[:x] == 20 && a[:y] == 20 }.first
#p origin[:sees].sort_by{ |a| a.arg }.map{ |a| a.polar }

p Complex(0,1).arg #pi/2
p Complex(1,0).arg #0
p Complex(0,-1).arg #-pi/2
p Complex(-1,0.001).arg #pi
p Complex(-1,-0.001).arg #-pi
p Complex.polar(18.973665961010276, -2.819842099193151).rect