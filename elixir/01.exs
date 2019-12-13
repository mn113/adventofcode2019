defmodule Fuel do
    defp read_input do
        File.read!(Path.expand("../inputs/input01.txt"))
        |> String.split("\n")
        |> Enum.map(fn line -> line |> Integer.parse end)
        |> Enum.map(fn {num, _} -> num end)
    end

    defp calc_fuel(mass) do
        div(mass, 3) - 2
    end

    defp calc_fuel(mass, accum_fuel \\ 0) do
        f = calc_fuel(mass)
        cond do
            f > 0 -> calc_fuel(f, accum_fuel + f)
            true  -> accum_fuel
        end
    end

    def part1 do
        read_input()
        |> Enum.map(&calc_fuel/1)
        |> Enum.sum
    end

    def part2 do
        read_input()
        |> Enum.map(&(calc_fuel(&1, 0)))
        |> Enum.sum
    end
end