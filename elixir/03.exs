defmodule Day03 do
    defp read_input do
        # File.read!(Path.expand("../inputs/input03.txt"))
        # |> String.split("\n")
        # ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
        ["R7,D3,R8,U8", "U6"]
        |> Enum.map(fn line -> String.split(line, ",") end)
        |> IO.inspect
    end

    @compass %{U: {0,1}, D: {0,-1}, L: {-1,0}, R: {1,0}}

    defp track_wire(instructions) do
        pt = [0,0]
        points = %{}
        moves = 0
        total = Enum.count(instructions, fn _ -> true end)

        Enum.each(1..total, fn i ->
            { direction, steps} = instructions |> Enum.at(i-1) |> String.split_at(1)
            direction = direction |> String.to_atom
            steps = String.to_integer(steps)
            Enum.each(1..steps, fn _ ->
                moves = moves + 1
                pt = List.replace_at(pt, 0, Enum.at(pt, 0) + elem(Map.get(@compass, direction), 0))
                pt = List.replace_at(pt, 1, Enum.at(pt, 1) + elem(Map.get(@compass, direction), 1))
                IO.inspect(pt)
                # add first one only (lowest steps wins)
                Map.put_new(points, pt, moves)
            end)
        end)

        points
        |> IO.inspect
    end

    defp manhattan_dist(pt) do
        pt
        |> Enum.map(&abs/1)
        |> Enum.sum
    end

    def part1 do
        wires = read_input()
        track1 = wires |> Enum.at(0) |> track_wire |> IO.inspect
        #track2 = track_wire(elem(wires, 1))

    end

    def part2 do
        read_input()
    end
end

Day03.part1
Day03.part2
