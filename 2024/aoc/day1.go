package aoc

import (
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

func getArr(file string) ([]int, []int) {
	dat, err := os.ReadFile(file)
	check(err)
	lines := strings.Split(string(dat), "\n")
	numLines := len(lines)
	arr1 := make([]int, numLines)
	arr2 := make([]int, numLines)
	var splitLine []string
	for idx, line := range lines {
		splitLine = strings.Split(line, "   ")
		n1, err := strconv.Atoi(splitLine[0])
		check(err)
		n2, err := strconv.Atoi(splitLine[1])
		check(err)
		arr1[idx] = n1
		arr2[idx] = n2
	}
	return arr1, arr2
}

func part1() {
	arr1, arr2 := getArr("./day1-input.txt")
	slices.Sort(arr1)
	slices.Sort(arr2)
	dist := 0
	i := 0
	for i < len(arr1) {
		dist += int(math.Abs(float64(arr1[i] - arr2[i])))
		i++
	}
	fmt.Println(dist)
}

func part2() {
	arr1, arr2 := getArr("./day1-input.txt")
	m := make(map[int]int)
	for _, val := range arr1 {
		m[val] = 0
	}
	for _, val := range arr2 {
		_, exists := m[val]
		if exists {
			m[val] += 1
		}
	}
	dist := 0
	for key, value := range m {
		dist += key * value
	}
	fmt.Println(dist)
}

func Day1() {
	part1()
	part2()
}
