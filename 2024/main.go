package main

import (
	"aoc/aoc"
	"fmt"
	"os"
	"strconv"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	command := os.Args[1]
	dayStr := os.Args[2]
	day, err := strconv.Atoi(dayStr)
	check(err)

	switch command {
	case "prepare":
		fmt.Printf("Preparing day %d\n", day)
		aoc.PrepareDay(day)
	case "run":
		fmt.Printf("Running day %d\n", day)
		var d aoc.Day
		switch day {
		case 1:
			d = aoc.Day1{}
		case 2:
			d = aoc.Day2{}
		default:
			panic("Day does not exist.")
		}
		d.Part1(aoc.GetInputFile(day))
		d.Part2(aoc.GetInputFile(day))
	}
}
