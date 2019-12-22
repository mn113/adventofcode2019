@maze = File.open("../inputs/input20.txt", "r").each_line.map{|r| r.chomp.gsub(' ', '#').chars}

# p @maze

@portals = {
    # key => [y,x]
    "outer" => {
        'GG' => [0,45],
        'DK' => [0,53],
        'MA' => [0,57],
        'NQ' => [0,65],
        'VR' => [0,73],
        'LL' => [0,85],
        'DR' => [45,0],
        'GZ' => [51,0],
        'BI' => [63,0],
        'RG' => [69,0],
        'QX' => [75,0],
        'JE' => [81,0],
        'HQ' => [41,128],
        'IN' => [45,128],
        'CL' => [59,128],
        'TO' => [63,128],
        'JQ' => [69,128],
        'YN' => [81,128],
        'QY' => [89,128],
        'KP' => [128,39],
        'JT' => [128,47],
        'IT' => [128,53],
        'IK' => [128,67],
        'AF' => [128,73],
        'QP' => [128,81],
        'NY' => [128,83],
        'VE' => [128,87]
    },
    "inner" => {
        'GG' => [41,94],
        'DK' => [34,77],
        'MA' => [94,55],
        'NQ' => [73,34],
        'VR' => [71,94],
        'LL' => [94,75],
        'DR' => [61,94],
        'GZ' => [34,63],
        'BI' => [53,34],
        'RG' => [94,79],
        'QX' => [57,94],
        'JE' => [47,34],
        'HQ' => [77,94],
        'IN' => [85,94],
        'CL' => [94,43],
        'TO' => [34,65],
        'JQ' => [34,47],
        'YN' => [87,34],
        'QY' => [94,77],
        'KP' => [34,83],
        'JT' => [49,94],
        'IT' => [94,67],
        'IK' => [94,87],
        'AF' => [94,49],
        'QP' => [59,34],
        'NY' => [34,53],
        'VE' => [69,34]
    }
}

@level = 0

def neighbs(current)
    current_yx = current.slice(0,2)
    depth = current[2]
    neighbs = []
    @portals["outer"].each do |key, outer_coords|
        inner_coords = @portals["inner"][key]
        # wire up 2-way teleportation
        if current_yx == outer_coords
            # depth decreases
            neighbs.push(inner_coords.dup.push(depth - 1)) if depth > 0 # limit levels
        elsif current_yx == inner_coords
            # depth increases
            neighbs.push(outer_coords.dup.push(depth + 1)) if depth < 20
        end
    end

    up    = [current[0] - 1, current[1], depth]
    down  = [current[0] + 1, current[1], depth]
    left  = [current[0], current[1] - 1, depth]
    right = [current[0], current[1] + 1, depth]

    neighbs.concat(
        [up, down, left, right]
        .reject{|p| p[0] < 0 || p[0] > 128 || p[1] < 0 || p[1] > 128}
        .reject{|p| @maze[p[0]][p[1]] == '#'}
    )
end

# dimensions represented by [y,x,depth]
start = [0,63,0]
finish = [53,128,0]

# memoiztion
@routes = Hash.new(0)
def store(start, goal, steps)
    @routes[[start.take(2), goal.take(2)]] = steps
    @routes[[goal.take(2), start.take(2)]] = steps
end

@visited = []
@dists = {}
@came_from = {}

def dijkstra(start, goal)
    # memoized?
    memo = @routes[[start.take(2), goal.take(2)]]
    return memo if memo > 0

    # @came_from = {}
    @dists[start] = 0
    # @visited = []
    to_visit = Queue.new
    to_visit.push(start)
    while to_visit.length > 0 do
        cell = to_visit.deq
        # upper limit
        next if @dists[cell] > 2500
        # second half meets first
        if @visited.include? cell
            p "REVISIT"
            return traceback(@came_from, start, goal)
        end
        # visit a cell
        @visited.push(cell)
        # finish?
        if cell == goal
            p "#{cell} has distance #{@dists[cell]} and is your GOAL"
            return traceback(@came_from, start, goal)
        end
        # analyse neighbours
        nbs = neighbs(cell)
        for nb in nbs do
            if !@visited.include? nb
                # unvisited neighbs: compute dist and add to to_visit
                @came_from[nb] = cell
                @dists[nb] = @dists[cell] + 1
                p "#{nb} has distance #{@dists[nb]}"
                to_visit.enq(nb)
            else
                # visited neighbs: recompute dist & parent
                newdist = @dists[cell] + 1
                if newdist < @dists[nb]
                    p "#{nb} has new, lower, distance #{@dists[nb]}"
                    @came_from[nb] = cell
                    @dists[nb] = newdist
                end
            end
        end
    end
    p "Out of nodes"
end

def traceback(came_from, start, goal)
    cur = goal
    steps = 0
    while cur != start do
        # @maze[cur[0]][cur[1]] = 'O'
        cur = came_from[cur]
        steps += 1
        p [steps, cur]
    end
    # memoize
    store(start, goal, steps)
    steps
end

total = 0
total += dijkstra(start, finish) # 674 in part 1
p total
total += dijkstra(finish, start)
p total

# @portals["outer"].each do |key, outer_coords|
#     @portals["inner"].each do |key, inner_coords|
#         dist = bfs(outer_coords, inner_coords)
#         store(outer_coords, inner_coords, dist)
#     end
# end
# p @routes

# dist_table
# printf @maze.map(&:join).join("\n")
