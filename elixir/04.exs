defmodule Day04 do
    @start 134792
    @finish 675810

    defp is_increasing(s) do
        x = String.split(s, "", trim: true)
        x == Enum.sort(x)
    end

    defp has_double(s) do
        Regex.match?(~r/(\d)\1/, s)
    end

    defp has_isolated_double(s) do
        [a,b,c,d,e,f] = String.split(s, "", trim: true)
        # Return true if 2 (and not more) adjacent chars match
        (a == b  &&  b != c) ||
        (b == c  &&  a != b  &&  c != d) ||
        (c == d  &&  b != c  &&  d != e) ||
        (d == e  &&  c != d  &&  e != f) ||
        (e == f  &&  d != e)
    end

    defp is_valid(s) do
        is_increasing(s) && has_double(s)
    end

    defp is_strictly_valid(s) do
        is_increasing(s) && has_isolated_double(s)
    end

    def part1 do
        @start..@finish
        |> Enum.map(fn n -> Integer.to_string(n) end)
        |> Enum.filter(&is_valid/1)
        |> length
    end

    def part2 do
        @start..@finish
        |> Enum.map(fn n -> Integer.to_string(n) end)
        |> Enum.filter(&is_strictly_valid/1)
        |> length
    end
end