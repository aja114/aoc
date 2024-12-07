package aoc

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Day2 struct{}

func GetArr(path string) [][]int {
	file, err := os.Open(path)
	check(err)
	var arr [][]int = make([][]int, 0)

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		strLine := strings.Split(line, " ")
		newLine := make([]int, len(strLine))
		for i, strEl := range strLine {
			el, err := strconv.Atoi(strEl)
			check(err)
			newLine[i] = el
		}
		arr = append(arr, newLine)
	}

	return arr
}

func SubArr(arr []int, idx int) []int {
	if idx == 0 {
		return arr[1:]
	} else if idx == len(arr) {
		return arr[:len(arr)-2]
	} else {
		return slices.Concat(nil, arr[:idx], arr[idx+1:])
	}
}

func isSafe(arr []int, ascencding bool, tol bool) bool {
	for i := 0; i < len(arr)-1; i++ {
		diff := math.Abs(float64(arr[i] - arr[i+1]))
		ascendingPair := bool(arr[i]-arr[i+1] < 0)
		if diff < 1 || diff > 3 {
			if tol {
				return isSafe(SubArr(arr, i), ascencding, false) || isSafe(SubArr(arr, i+1), ascencding, false)
			}
			return false
		}
		if (ascencding || ascendingPair) && !(ascencding && ascendingPair) {
			if tol {
				return isSafe(SubArr(arr, i), ascencding, false) || isSafe(SubArr(arr, i+1), ascencding, false)
			}
			return false
		}
	}
	return true
}

func (d Day2) Part1(path string) {
	arr := GetArr(path)
	dist := 0
	for _, l := range arr {
		if isSafe(l, bool(l[0] < l[1]), false) {
			dist += 1
		}
	}
	fmt.Println(dist)
}

func (d Day2) Part2(path string) {
	arr := GetArr(path)
	dist := 0
	for _, l := range arr {
		if isSafe(l, true, true) || isSafe(l, false, true) {
			dist += 1
		}
	}
	fmt.Println(dist)
}
