input = File.open("../inputs/input16.txt", "r").each_line.first.chars.map(&:to_i)
# p input.length # 650
input2 = input.dup

def base_pattern(i)
    [0,1,0,-1].map{|d| (0..i).to_a.fill(d)}.flatten.rotate(1)
end

def fft(inp)
    inp.each_with_index.map{ |_,i|
        # multiply digit-wise by repeated pattern
        pat = base_pattern(i)
        pat += pat while pat.length < inp.length
        pat = pat.take(inp.length)
        result = inp.each_with_index.map { |n,j|
            val = n * pat[j]
        }.reduce(&:+).abs % 10
    }
end

def second_half_sum(inp)
    output = inp.dup.fill(0)
    # calculates last 50% only
    lastsum = 0
    1.upto (inp.length / 2) do |i|
        lastsum += inp[-i]
        output[-i] = lastsum % 10
    end
    output
end

# Part 1: run 100 phases
100.times do
    input = fft(input)
end
p input.take(8).join.to_i # 63794407


# Part 2: input repeated 10000 times!
input3 = input2 * 10000
offset = 5_971_751
p "length #{input3.length}"
100.times do |i|
    input3 = second_half_sum(input3)
    p [i, input3[offset, 8]] if i % 10 == 0
end
p input3.drop(offset).take(8).join.to_i # 77247538
