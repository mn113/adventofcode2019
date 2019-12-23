require 'set'

# ingest map to 2D array
@maze = File.open("../inputs/input18.txt", "r").each_line.map(&:strip).map(&:chars)
printf @maze.map(&:join).join("\n") + "\n"
# p @maze[40][40]
# p @maze[31][47]
maze_size = 81
origin = [40,40]

lowercase = 'a'...'z'
uppercase = 'A'...'Z'
@keymap = {}
@doormap = {}

# locate 26 keys & 26 doors
lowercase.each do |k|
    y = @maze.find_index{|row| row.include?(k)}
    x = @maze[y].find_index(k)
    @keymap[k] = [y,x]
end
uppercase.each do |d|
    y = @maze.find_index{|row| row.include?(d)}
    x = @maze[y].find_index(d)
    @doormap[d] = [y,x]
end
p @keymap
p @doormap

# pathfind start to every key, collecting blocking doors
# manually adjust key order as waypoints

def isHall(node)
    @maze[node[0]][node[1]] != '#' && \
    @maze[node[0]][node[1]] != '/'
end

def neighbours(coords)
    y = coords[0]
    x = coords[1]
    up    = [x, [y-1, 0].max]
    down  = [x, [y+1, 80].min]
    left  = [[x-1, 0].max, y]
    right = [[x+1, 80].min, y]
    # Only return Halls, never Walls:
    [up, down,left, right].select{|nb| isHall(nb)}
end

def manhattan_dist(a,b)
    (a[0] - b[0]).abs + (a[1] - b[1]).abs
end

# Main algo:
def bfs(start, goal)
    dist_to = Hash.new(0)    # measures steps to each node
    visited = Set.new()
    to_visit = [start]
    came_from = {start: nil}   # traces the path taken
    limit = manhattan_dist(start,goal)
    i = 0;

    while to_visit.length > 0 do
        i += 1
        current = to_visit.pop
        visited.add(current)

        if current == goal
            p 'GOAL!'
            break
        end

        # if i > 1 && manhattan_dist(current, start) == 0
        #     next # Don't turn back over start
        # end

        neighbs = neighbours(current)
        if neighbs.length == 1 and visited.include? neighbs[0]
            @maze[current[0]][current[1]] = '/'
            next # Dead end
        end

        neighbs.each do |nextNode|
            # nextNode unseen:
            if !visited.include? nextNode
                # Add to queue:
                to_visit.push(nextNode)
                # Next node will cost 1 more step than this node did:
                dist_to[nextNode] = dist_to[current] + 1
                came_from[nextNode] = current
            # nextNode seen before:
            else
                if dist_to[nextNode] > dist_to[current] + 1
                    # Via current, we have found a new, shorter path to this known nextNode:
                    dist_to[nextNode] = dist_to[current] + 1
                    came_from[nextNode] = current
                end
            end
        end
    end

    # Finished seeing nodes now
    if came_from.keys.include? goal
        traceback(goal, came_from)
    else
        "No path found"
    end
end

# Traceback function:
def traceback(goal, came_from)
    parent = came_from[goal]
    steps = 0
    # p "Traceback from goal #{goal}"
    until parent.nil? do
        #p [parent, steps]
        parent = came_from[parent]
        p @doormap.select{|k,v| v == parent } if @doormap.values.include? parent
        steps = steps + 1
    end
    steps
end

# Full node graph:
# edges = {}
# keymap.keys.each do |a|
#     keymap.keys.each do |b|
#         if b > a
#             edges[[a,b]] = bfs(keymap[a], keymap[b])
#             p [edges[[a,b]], "from", a, "to", b]
#         end
#     end
# end

@keymap.each do |k,v|
    p ["start to key #{k}:", bfs(origin, v)]
end

keys_seq = 'abcde'.chars
total = 0
keys_seq.each_cons(2) do |m,n|
    p dist = [m, n, bfs(@keymap[m], @keymap[n])]
    total += dist
end

# def sum_edges(sequence):
#     total = 0
#     for i in range(len(sequence) - 1):
#         a, b = sequence[i], sequence[i+1]
#         total = total + edges[(min(a,b),max(a,b))]
#     return total
