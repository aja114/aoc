package main

import (
	"aoc/aoc"
	"fmt"
	"os"
	"runtime/pprof"
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

	// Create a CPU profile file
	f, err := os.Create("cpu.pprof")
	if err != nil {
		fmt.Println("could not create CPU profile: ", err)
		return
	}
	defer f.Close()

	// Start CPU profiling
	if err := pprof.StartCPUProfile(f); err != nil {
		fmt.Println("could not start CPU profile: ", err)
		return
	}
	defer pprof.StopCPUProfile()

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
		case 3:
			d = aoc.Day3{}
		case 4:
			d = aoc.Day4{}
		case 5:
			d = aoc.Day5{}
		case 6:
			d = aoc.Day6{}
		case 7:
			d = aoc.Day7{}
		case 8:
			d = aoc.Day8{}
		case 9:
			d = aoc.Day9{}
		case 10:
			d = aoc.Day10{}
		case 11:
			d = aoc.Day11{}
		case 12:
			d = aoc.Day12{}
		case 13:
			d = aoc.Day13{}
		case 14:
			d = aoc.Day14{}
		case 15:
			d = aoc.Day15{}
		case 16:
			d = aoc.Day16{}
		case 17:
			d = aoc.Day17{}
		case 18:
			d = aoc.Day18{}
		case 19:
			d = aoc.Day19{}
		case 20:
			d = aoc.Day20{}
		default:
			panic("Day does not exist.")
		}
		d.Part1(aoc.GetInputFile(day))
		d.Part2(aoc.GetInputFile(day))
	}
}
