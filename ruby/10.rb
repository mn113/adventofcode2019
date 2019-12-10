$data = File.open("../inputs/input10.txt", "r").each_line.map(&:chars)

$height = $data.length
$width = $data[0].length

asteroids = []
(0...$height).each do |y|
    (0...$width).each do |x|
        if $data[y][x] == '#'
            asteroids.push({ x: x, y: y, c: Complex(x,y), sees: []})
        end
    end
end

asteroids.each do |a|
    asteroids.each do |b|
        next if a[:x] == b[:x] && a[:y] == b[:y]
        diff = (b[:c] - a[:c]) * Complex(0,-1) # flip Y
        angle = diff.arg
        angle += 2 * Math::PI if angle < 0
        a[:sees].push([angle, b[:x], b[:y]])
    end
end

p asteroids.map{ |a| a[:sees].uniq{ |a| a[0] }.size }.max # part 1 = 292

p asteroids.select{ |a| a[:sees].uniq{ |a| a[0].arg }.size == 292 } # [20, 20]

origin =  asteroids.select{ |a| a[:x] == 20 && a[:y] == 20 }.first

origin[:sees]
    .uniq{ |a| a[0] } # assume only one asteroid will be hit on each angle
    .sort_by{ |a| a[0] }
    .each {|a| puts a.inspect }

p [:part2, [3,17]] # fucked up angles, had to solve manually
