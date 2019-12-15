input = File.open("../inputs/input14.txt", "r")

# convert "175 ORE" into {:sym => :ORE, :amt => 175}
def reformat str
    tmp = str.split(/\s/).reverse
    { :sym => tmp[0].to_sym, :amt => tmp[1].to_i}
end

data = Hash.new
input.each_line.map do |line|
    bits = line.split(/,|=>/).map(&:strip)
    key = reformat bits[-1]
    vals = bits[0...-1].map{ |s| reformat s }
    data[key] = vals
end

# p data
p data.to_s.scan(:FUEL.to_s)

needed = [{:sym => :FUEL, :amt => 1}]
ores = 0
waste = {}

[2,3,4].each do |maxcount|
    100.times do
        current = needed.shift
        next if !current
        count = data.to_s.scan(current[:sym].to_s).length
        p "----"
        p "cur #{current} (#{count} : #{maxcount})"
        required_kv = data.select{ |k,_| k[:sym] == current[:sym] }
        p "found #{required_kv}"
        if count > maxcount && current[:sym] != :FUEL
            needed.push(current)
            p "requeue it"
            next
        elsif required_kv.length == 0
            next
        end
        key = required_kv.keys.first

        # use up waste
        if waste.has_key? key[:sym]
            usable = [waste[key[:sym]], current[:amt]].min
            current[:amt] -= usable
            waste[key[:sym]] -= usable
            p "used #{usable} waste of #{current[:sym]}, still need #{current[:amt]}"
        end
        next if current[:amt] == 0

        # calculate key scale
        if current[:amt] == key[:amt]
            scale = 1
        else
            scale = (current[:amt] / key[:amt].to_f).ceil # 1
        end
        tmp_waste = scale * key[:amt] - current[:amt] # 3
        p "scale #{scale} * #{key[:amt]} #{key[:sym]} fulfils #{current[:amt]} #{current[:sym]} with #{tmp_waste} waste"
        # store that waste
        if waste.has_key?(key[:sym])
            waste[key[:sym]] += tmp_waste # increment count
        else
            waste[key[:sym]] = tmp_waste # begin count
        end

        # scale values
        required_kv.values.first.each do |res|
            #p "-res #{res}"
            res[:amt] *= scale
            if res[:sym] == :ORE
                p "adding #{res[:amt]} ORE"
                ores += res[:amt]
            else
                p "queueing #{res}"
                existing = needed.index{ |need| need[:sym] == res[:sym] }
                if existing.nil?
                    needed.push(res)
                else
                    needed[existing][:amt] += res[:amt]
                end
            end
        end
        data.delete key
        p "need #{needed}"
    end
end
p "ORE: #{ores}"
