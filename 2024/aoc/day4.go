package aoc

import (
	"fmt"
)

type Day4 struct{}

var PATTERN = "XMAS"

func getNextChars(x int, y int, arr []string) []string {
	// HZ = Horizontal
	// VT = Vertical
	// DGLR = Diagonal bottom left to top right /
	// DGRL = Diagonal top left to bottm right /
	// FW = Forward
	// BW = Backward
	var matches = map[string]string{
		"HZ-FW":   "",
		"HZ-BW":   "",
		"VT-FW":   "",
		"VT-BW":   "",
		"DGLR-FW": "",
		"DGLR-BW": "",
		"DGRL-FW": "",
		"DGRL-BW": "",
	}
	h := len(arr)
	w := len(arr[0])
	for i := range len(PATTERN) {
		if x+i < h {
			matches["HZ-FW"] += string(arr[x+i][y])
		}
		if x-i >= 0 {
			matches["HZ-BW"] += string(arr[x-i][y])
		}
		if y+i < w {
			matches["VT-FW"] += string(arr[x][y+i])
		}
		if y-i >= 0 {
			matches["VT-BW"] += string(arr[x][y-i])
		}
		if x+i < h && y+i < w {
			matches["DGLR-FW"] += string(arr[x+i][y+i])
		}
		if x+i < h && y-i >= 0 {
			matches["DGLR-BW"] += string(arr[x+i][y-i])
		}
		if x-i >= 0 && y-i >= 0 {
			matches["DGRL-FW"] += string(arr[x-i][y-i])
		}
		if x-i >= 0 && y+i < w {
			matches["DGRL-BW"] += string(arr[x-i][y+i])
		}
	}
	var matchesArr []string
	for _, value := range matches {
		matchesArr = append(matchesArr, value)
	}
	return matchesArr
}

func isXMAS(x int, y int, arr []string) bool {
	if x <= 0 || x >= len(arr)-1 || y <= 0 || y >= len(arr[0])-1 {
		return false
	}
	if arr[x][y] != 'A' {
		return false
	}
	if arr[x-1][y-1] == 'M' &&
		arr[x-1][y+1] == 'M' &&
		arr[x+1][y-1] == 'S' &&
		arr[x+1][y+1] == 'S' {
		return true
	}
	if arr[x-1][y-1] == 'S' &&
		arr[x-1][y+1] == 'M' &&
		arr[x+1][y-1] == 'S' &&
		arr[x+1][y+1] == 'M' {
		return true
	}
	if arr[x-1][y-1] == 'S' &&
		arr[x-1][y+1] == 'S' &&
		arr[x+1][y-1] == 'M' &&
		arr[x+1][y+1] == 'M' {
		return true
	}
	if arr[x-1][y-1] == 'M' &&
		arr[x-1][y+1] == 'S' &&
		arr[x+1][y-1] == 'M' &&
		arr[x+1][y+1] == 'S' {
		return true
	}
	return false
}

func getOccurencesP1(x int, y int, arr []string) int {
	res := 0
	for _, match := range getNextChars(x, y, arr) {
		if match == PATTERN {
			res += 1
		}
	}
	return res
}

func (d Day4) Part1(path string) {
	arr := getMap(path)
	h := len(arr)
	w := len(arr[0])
	res := 0
	for i := 0; i < h; i++ {
		for j := 0; j < w; j++ {
			if arr[i][j] == PATTERN[0] {
				res += getOccurencesP1(i, j, arr)
			}
		}
	}
	fmt.Println(res)
}

func (d Day4) Part2(path string) {
	arr := getMap(path)
	h := len(arr)
	w := len(arr[0])
	res := 0
	for i := 0; i < h; i++ {
		for j := 0; j < w; j++ {
			if isXMAS(i, j, arr) {
				res += 1
			}
		}
	}
	fmt.Println(res)
}
