package aoc

import (
	"fmt"
)

type Day12 struct{}

func computeGarden(p Pos, arr []string, target byte, seen map[Pos]string) (int, int) {
	if _, exists := seen[p]; exists {
		return 0, 0
	}
	if arr[p.x][p.y] != target {
		return 0, 0
	}
	seen[p] = string(arr[p.x][p.y])
	area := 1
	fences := 4
	for _, adj := range p.GetAdjacent(arr) {
		if arr[adj.x][adj.y] == target {
			fences -= 1
			adjArea, adjFences := computeGarden(adj, arr, target, seen)
			area += adjArea
			fences += adjFences
		}
	}
	return area, fences
}

func (d Day12) Part1(path string) {
	arr := getMap(path)
	seen := make(map[Pos]string)
	res := 0
	for i := 0; i < len(arr); i++ {
		for j := 0; j < len(arr[0]); j++ {
			p := Pos{x: i, y: j}
			if _, exists := seen[p]; exists {
				continue
			} else {
				a, f := computeGarden(p, arr, arr[i][j], seen)
				res += a * f
			}
		}
	}
	fmt.Println(res)
}

func computeFences(p Pos, arr []string, target byte, seen map[Pos]int, fences map[Pos]bool, idx int) int {
	if _, exists := seen[p]; exists {
		return 0
	}
	if arr[p.x][p.y] != target {
		return 0
	}
	seen[p] = idx
	area := 1
	neighbours := 0
	for _, adj := range p.GetAdjacent(arr) {
		if arr[adj.x][adj.y] == target {
			adjArea := computeFences(adj, arr, target, seen, fences, idx)
			area += adjArea
			neighbours += 1
		}
	}
	if neighbours < 4 {
		fences[p] = true
	}
	return area
}

func (d Day12) Part2(path string) {
	arr := getMap(path)
	seen := make(map[Pos]int)
	areas := make(map[int]int)
	fences := make(map[int]int)
	idx := 0
	for i := 0; i < len(arr); i++ {
		for j := 0; j < len(arr[0]); j++ {
			p := Pos{x: i, y: j}
			if _, exists := seen[p]; exists {
				continue
			} else {
				fences := make(map[Pos]bool)
				a := computeFences(p, arr, arr[i][j], seen, fences, idx)
				areas[idx] = a
				idx += 1
			}
		}
	}
	// Iterate over rows
	for i := 0; i < len(arr); i++ {
		prevBefore := byte('#')
		prevAfter := byte('#')
		for j := 0; j < len(arr[0]); j++ {
			currentGroup := seen[Pos{x: i, y: j}]
			if arr[i][j] != prevBefore && (i == 0 || arr[i][j] != arr[i-1][j]) {
				fences[currentGroup] += 1
				prevBefore = arr[i][j]
			} else if i > 0 && arr[i][j] == arr[i-1][j] {
				prevBefore = byte('#')
			}
			if arr[i][j] != prevAfter && (i == len(arr)-1 || arr[i][j] != arr[i+1][j]) {
				fences[currentGroup] += 1
				prevAfter = arr[i][j]
			} else if i < len(arr)-1 && arr[i][j] == arr[i+1][j] {
				prevAfter = byte('#')
			}
		}
	}
	// iterate over columns
	for j := 0; j < len(arr[0]); j++ {
		prevTop := byte('#')
		prevBottom := byte('#')
		for i := 0; i < len(arr); i++ {
			currentGroup := seen[Pos{x: i, y: j}]
			if arr[i][j] != prevTop && (j == 0 || arr[i][j] != arr[i][j-1]) {
				fences[currentGroup] += 1
				prevTop = arr[i][j]
			} else if j > 0 && arr[i][j] == arr[i][j-1] {
				prevTop = byte('#')
			}
			if arr[i][j] != prevBottom && (j == len(arr[0])-1 || arr[i][j] != arr[i][j+1]) {
				fences[currentGroup] += 1
				prevBottom = arr[i][j]
			} else if j < len(arr[0])-1 && arr[i][j] == arr[i][j+1] {
				prevBottom = byte('#')
			}
		}
	}

	res := 0
	for k := range areas {
		res += areas[k] * fences[k]
	}
	fmt.Println(res)
}
