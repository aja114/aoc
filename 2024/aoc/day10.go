package aoc

import "fmt"

type Day10 struct{}

func reachableLevels(pos Pos, arr []string, targets map[Pos]int) {
	if arr[pos.x][pos.y] == '9' {
		targets[pos] += 1
	}
	target := int(arr[pos.x][pos.y]) + 1
	adjacents := getAdjacent(pos, arr)
	for _, adjacent := range adjacents {
		if int(arr[adjacent.x][adjacent.y]) == target {
			reachableLevels(adjacent, arr, targets)
		}
	}
}

func (d Day10) Part1(path string) {
	arr := getMap(path)
	startPos := getAllPos(arr, '0')
	res := 0
	for _, p := range startPos {
		targets := make(map[Pos]int)
		reachableLevels(p, arr, targets)
		res += len(targets)
	}
	fmt.Println(res)
}

func (d Day10) Part2(path string) {
	arr := getMap(path)
	startPos := getAllPos(arr, '0')
	res := 0
	for _, p := range startPos {
		targets := make(map[Pos]int)
		reachableLevels(p, arr, targets)
		for _, v := range targets {
			res += v
		}
	}
	fmt.Println(res)
}
