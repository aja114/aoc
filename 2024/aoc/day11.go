package aoc

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Day11 struct{}

type State struct {
	s     string
	depth int
}

func StoneRules(s string, depth int, memo map[State]int) int {
	if depth == 0 {
		return 1
	}
	state := State{s: s, depth: depth}
	if val, exists := memo[state]; exists {
		return val
	}
	var res int
	if s == "0" {
		res = StoneRules("1", depth-1, memo)
	} else if len(s)%2 == 0 {
		// strip leading 0s
		head, err := strconv.Atoi(s[:len(s)/2])
		check(err)
		tail, err := strconv.Atoi(s[len(s)/2:])
		check(err)
		res = StoneRules(strconv.Itoa(head), depth-1, memo) + StoneRules(strconv.Itoa(tail), depth-1, memo)
	} else {
		i, err := strconv.Atoi(s)
		check(err)
		res = StoneRules(strconv.Itoa(i*2024), depth-1, memo)
	}
	memo[state] = res
	return res
}

func runDay(path string, depth int) {
	f, err := os.ReadFile(path)
	check(err)
	res := 0
	memo := make(map[State]int)
	for _, s := range strings.Split(string(f), " ") {
		res += StoneRules(s, depth, memo)
	}
	fmt.Println(res)
}

func (d Day11) Part1(path string) {
	runDay(path, 25)
}

func (d Day11) Part2(path string) {
	runDay(path, 75)
}
