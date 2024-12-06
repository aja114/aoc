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
		switch day {
		case 1:
			aoc.Day1()
		case 2:
			aoc.Day2()
		}
	}
}
