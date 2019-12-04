$start = 134792
$finish = 675810

def is_increasing s
    x = s.split(//)
    x == x.sort()
end

def has_double s
    /(\d)\1/.match(s)
end

def has_isolated_double s
    (s[0] == s[1]  &&  s[1] != s[2]) ||
    (s[1] == s[2]  &&  s[0] != s[1]  &&  s[2] != s[3]) ||
    (s[2] == s[3]  &&  s[1] != s[2]  &&  s[3] != s[4]) ||
    (s[3] == s[4]  &&  s[2] != s[3]  &&  s[4] != s[5]) ||
    (s[4] == s[5]  &&  s[3] != s[4])
end

def is_valid s
    is_increasing(s) && has_double(s)
end

def is_strictly_valid s
    is_increasing(s) && has_isolated_double(s)
end

def part1
    ($start..$finish).to_a.map(&:to_s).select{|s| is_valid(s)}.size
end

def part2
    ($start..$finish).to_a.map(&:to_s).select{|s| is_strictly_valid(s)}.size
end

p 'Part 1:', part1
p 'Part 2:', part2
