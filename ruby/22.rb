instructions = File.open("../inputs/input22.txt", "r").each_line.map do |line|
    /(?<text>[\w\s]+)\s(?<num>-?[\d]+)$/ =~ line.chomp
    instr = "cut" if /cut/.match(text)
    instr = "incr" if /increment/.match(text)

    /(?<text>[\w\s]+)/ =~ line.chomp
    instr = "stack" if /stack/.match(text)

    [instr, num.to_i]
end

# p instructions

def stack(cards)
    p "stack"
    cards.reverse
end

def cut(cards, num)
    p "cut #{num}"
    cards.rotate(num)
end

def incr(cards, num)
    p "incr #{num}"
    newcards = cards.dup.fill{|_| nil}
    ptr = 0
    cards.each do |card|
        ptr2 = ptr
        while !newcards[ptr2].nil? do ptr2 += 1 end
        newcards[ptr2] = card
        ptr = (ptr + num) % cards.length
    end
    newcards
end

cards = (0...10007).to_a

instructions.each do |instr|
    num = instr[1]
    case(instr[0])
    when "stack"
        cards = stack(cards)
    when "cut"
        cards = cut(cards, num)
    when "incr"
        cards = incr(cards, num)
    end
end
p cards.length
p cards.index(2019) # 2241 low
