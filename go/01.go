package main

import (
	"fmt"
	"os"
)

func main() {
	sum := 0
	for i := 0; i < 10; i++ {
		sum += i
	}
	fmt.Println(sum)
}

fp, err := os.Open("../inputs/input01.txt")
modules = fp.read().split("\n").map_to_int

scanner := bufio.NewScanner(file)
scanner.Split(bufio.ScanLines)
var lines []string

for scanner.Scan() {
	lines = append(lines, scanner.Text())
}

file.Close()

func calc_fuel(mass) {
	floor(mass / 3) - 2
}

func part1() {
	modules.map().sum()
}

part1();
